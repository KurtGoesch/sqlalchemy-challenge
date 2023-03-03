import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Stations = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/START<br/>"
        f"/api/v1.0/START/END<br/>"
        f"Date format is MMDDYYYY"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).where(Measurement.date > '2016-08-23')

    session.close()

    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Stations.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).where(Measurement.station == 'USC00519281', Measurement.date > '2016-08-23')

    session.close()

    tobs_data = []
    for date, tobs in results:
        prcp_dict = {}
        prcp_dict[date] = tobs
        tobs_data.append(prcp_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start_only(start):
    start_date = dt.datetime.strptime(start, "%m%d%Y")

    session = Session(engine)

    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    temps = list(np.ravel(results))

    start_stats = []
    start_stats.append(temps)
    
    return jsonify(start_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_date = dt.datetime.strptime(start, "%m%d%Y")
    end_date = dt.datetime.strptime(end, "%m%d%Y")

    session = Session(engine)

    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    session.close()

    temps = list(np.ravel(results))

    start_end_stats = []
    start_end_stats.append(temps)
    
    return jsonify(start_end_stats)

if __name__ == '__main__':
    app.run(debug=True)