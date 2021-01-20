#import modules
from flask import Flask,jsonify
from sqlalchemy import create_engine,func
from sqlalchemy.orm import Session
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
import datetime as dt


app=Flask(__name__)

def confg():

    Base= automap_base()
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base.prepare(engine, reflect=True)
    Station=Base.classes.station
    Measurement=Base.classes.measurement
    Station=Base.classes.station

    session = Session(engine)

    last_day = session.query(Measurement).order_by(Measurement.date.desc()).first().date
    last_12months=dt.datetime.strptime(last_day, '%Y-%m-%d') - dt.timedelta(days=365)
    
    return Measurement,Station,session,last_12months


@app.route("/")
def home():

    return (
        f"Welcome to the climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    Measurement,Station,session,last_12months = confg()
    
    precip_date_query=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >last_12months).order_by(Measurement.date).all()

    result_dict={}
    for row in precip_date_query:
        result_dict[row[0]]=row[1]
    date_percip=[result_dict]
    print(type(date_percip))
    session.close()
    return jsonify(date_percip)

@app.route("/api/v1.0/stations")
def stations():

    Measurement,Station,session,last_12months = confg()
    station=session.query(Station.station).all()
    session.close()
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():

    Measurement,Station,session,last_12months = confg()

    date_tobs_query=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > last_12months).filter(Measurement.station =='USC00519281').order_by(Measurement.tobs.desc()).all()

    tobs_dict={}
    for row in date_tobs_query:
        tobs_dict[row[0]]=row[1]
    tobs_date=[tobs_dict]
    session.close()
    return jsonify(tobs_date)


@app.route("/api/v1.0/<start>")
def start(start=None):

    Measurement,Station,session,last_12months = confg()

    start_tobs_query=session.query(*[func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)]).filter(Measurement.date >= start).all()
    session.close()
    return jsonify(start_tobs_query)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None,end=None):

    Measurement,Station,session,last_12months = confg()

    start_end_query=session.query(*[func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)]).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return jsonify(start_end_query)
    

if __name__ == "__main__":
    app.run(debug=True)

