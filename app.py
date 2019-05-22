#################################################
# Import Libraries
#################################################
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"<br/>"
        f"**Date Format for start & end: YYYY-MM-DD<br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    """Return a list of all precipitation date/value pairs"""
    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Measurement.station).distinct().all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all tobs for the last year"""
    # Calculate date 1 year from last observation
    last = dt.date.fromisoformat(session.query(Measurement.date).\
                             order_by(Measurement.date.desc()).\
                             first()._asdict()['date']) - dt.timedelta(days=365)

    # Query all tobs for the last year
    results = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date > last).all()

    # Convert list of tuples into normal list
    tobs_year = list(np.ravel(results))

    return jsonify(tobs_year)


@app.route("/api/v1.0/<start>")
def date_start(start):
    """Return min / avg / max temperatures for all dates >= start"""
    # Query min / avg / max temperatures for all dates >= start
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    temps = list(np.ravel(results))

    return jsonify(temps)


@app.route("/api/v1.0/<start>/<end>")
def date_start_end(start, end):
    """Return min / avg / max temperatures for all dates (start, end)"""
    # Query min / avg / max temperatures for all dates (start, end)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    # Convert list of tuples into normal list
    temps = list(np.ravel(results))

    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)
