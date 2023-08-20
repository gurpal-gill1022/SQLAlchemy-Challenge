#################################################
# Import the dependencies.
#################################################
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
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Home Page Route
@app.route("/")
def welcome():
    """List all available api routes."""
    api_list = ["Welcome to my API!", "Available Routes<br/>", "/api/v1.0/precipitation", "/api/v1.0/station", "/api/v1.0/tobs", "/api/v1.0/<start>", "/api/v1.0/<start>/<end>"]

    return jsonify(api_list)


# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value."""
    #Calculate the date one year from the last date in the data set
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #Perform query to retrieve the date and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > one_year_ago).\
        order_by(Measurement.date).all()
    
    session.close()

    """Return the JSON representation of your dictionary."""
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


# Stations Route
@app.route("/api/v1.0/station")
def stations():
    #Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    #Perform query to retrieve the data of all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


# TOBS Route
@app.route("/api/v1.0/tobs")
def tobs():
    #Create our session(link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most-active station for the previous year of data."""
    #Calculate the date one year from the last date in the data set
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #Perform query to retrieve the date and TOBS scores
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > one_year_ago,
               Measurement.station == "USC00519281").\
        order_by(Measurement.date).all()
    
    session.close()
    
    """Return a JSON list of temperature observations for the previous year."""
    all_TOBS = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_TOBS.append(tobs_dict)

    return jsonify(all_TOBS)


# Start Route
@app.route("/api/v1.0/<start>")
def start_route(start):
    #Create our session(link) from Python to the DB
    session = Session(engine)
    
    #Perform query to retrieve the minimum temperature, the average temperature, and the maximum temperature
    start = '2017-08-23'

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()

    #Create a JSON list
    start_list = [{"MIN": results[0][0]},
                  {"AVG": results[0][1]},
                  {"MAX": results[0][2]}]
    
    return jsonify(start_list)


#Start and End Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_route(start, end):
    #Create our session(link) from Python to the DB
    session = Session(engine)
    
    #Perform query to retrieve the minimum temperature, the average temperature, and the maximum temperature
    start = '2017-08-23'
    end = '2016-08-23'

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date <= start).\
        filter(Measurement.date >= end).all()

    session.close()

    #Create a JSON list
    start_end_list =  [{"MIN": results[0][0]},
                  {"AVG": results[0][1]},
                  {"MAX": results[0][2]}]

    return jsonify(start_end_list)


if __name__ == '__main__':
    app.run(debug=True)