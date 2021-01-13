from flask import Flask,jsonify
from sqlalchemy import create_engine,func
from sqlalchemy.orm import Session
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
import datetime as dt

Base= automap_base()


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base.prepare(engine, reflect=True)
Station=Base.classes.station
Measurement=Base.classes.measurement
session = Session(engine)

last_day = session.query(Measurement).order_by(Measurement.date.desc()).first().date

last_12months=dt.datetime.strptime(last_day, '%Y-%m-%d') - dt.timedelta(days=365)

precip_date_query=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >last_12months).order_by(Measurement.date).all()

result_dict={}

for row in precip_date_query:
    result_dict[row[0]]=row[1]

date_percip=[result_dict]

tobs_dict={}
date_tobs_query=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > last_12months).filter(Measurement.station =='USC00519281').order_by(Measurement.tobs.desc()).all()
for row in date_tobs_query:
    tobs_dict[row[0]]=row[1]
tobs_date=[tobs_dict]

station=session.query(Measurement.station).filter(Measurement.date >last_12months).all()

app=Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(date_percip)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(tobs_date)

# if __name__ == "__main__":
#     app.run(debug=True)
