
# Dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

# create engine - maintain the same connection per thread
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temp/'start date'<br/>"
        f"/api/v1.0/temps/'start date'/'end date'<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all dates and precip"""
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()  
    precip_list = list(np.ravel(results))
    return jsonify(precip_list)   
# Attempt to use dictionary with names
#    precip_list = []
#    for result in results:
#        precip_dict = {}
#        precip_dict["date"] = Measurement.date
#        precip_dict["prcp"] = Measurement.prcp
#        precip_list.append(precip_dict)
#    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    results = session.query(Measurement.station).group_by(Measurement.station).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23', Measurement.station == 'USC00519281').order_by(Measurement.date).all()
    all_tobs = list(np.ravel(results))
    return jsonify(all_tobs)

@app.route("/api/v1.0/temp/<start>")
def temp(start):
    """calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    after_start = list(np.ravel(results))
    return jsonify(after_start)

@app.route("/api/v1.0/temps/<start>/<end>")
def temps(start, end):
    """calculate `TMIN`, `TAVG`, and `TMAX` for date range"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    start_to_end = list(np.ravel(results))
    return jsonify(start_to_end)

# define main behavior
if __name__ == '__main__':
    app.run(debug=True, port=5000)

# export FLASK_APP=app2.py
# python -m flask run