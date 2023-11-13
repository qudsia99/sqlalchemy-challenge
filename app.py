# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchem
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)

# Save references to each table

measurements = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB

session= Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """ Welcome page, with access links listed. """
    return (
        f"Welcome to the Hawaii Climate Page!"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
        f"/api/v1.0/start_date/2014-08-03<br/>"
        f"Please enter the date in the following format: YYYY-MM-DD between 2010-01-01 and 2017-08-23<br/>"
        f"/api/v1.0/start_date/2013-06-08/end_date/2017-01-28<br/>"
        f"Please enter the date in the following format: YYYY-MM-DD between 2010-01-01 and 2017-08-23"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Finding the specific date value from the last date in data set.
    query_date = dt.date(2017, 8, 23) - relativedelta(months=12)

    # Performing a query to gather the precipitation scores
    query = session.query(measurements.date, measurements.prcp).\
        filter(measurements.date >= query_date).all()

    # Convert the query into a dictionary
    climate_percipi = [{'Date': date, 'precipitation': prcp} for date, prcp in query]

    # Close the session
    session.close()

    #return Json file
    return jsonify(climate_percipi)


@app.route("/api/v1.0/stations")
def stations():
    # query to find stations
    query_station= session.query(measurements.station).group_by(measurements.station).all()

    # Convert the query into a dictionary, using a for loop 
    stations_dictionary = []
    for station in query_station:
        station_dict = {'station': station[0]}
        stations_dictionary.append(station_dict)

    # Close the session
    session.close()

    #return Json file of stations
    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():

    # Since we already found the most recent year in the data from our calculations earlier, we can utilize that
    query_date = dt.date(2017, 8, 23) - relativedelta(months=12)


    #perform query to find date and temperature readings again, but for previous year
    temp_and_year=session.query(measurements.date, measurements.tobs).filter(measurements.station=='USC00519281').\
                                            filter(measurements.date >= query_date).all()
    # Convert the query into a dictionary
    temperature_di = [{'Date': date, 'Temperature': temp} for date, temp in temp_and_year]

    # Close the session
    session.close()

    #return Json file
    return jsonify(temperature_di)


@app.route("/api/v1.0/start_date/<start>")
def temp_data(start):

    # Declare the start variables
    start_date=start

    # performing the query to find the MAX, MIN and AVERAGE temperatures
    station_temp=session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).filter(measurements.date >= start_date).all()
    
    # convert the query into a dictionary
    unique_tem_dict = [{'Min Temperature': min, 'Max Temperature': max, 'Average Temperature': avg} for min, max, avg in station_temp]
    
    # Close the session
    session.close()
    
    # return Json file
    return jsonify(unique_tem_dict)


@app.route("/api/v1.0/start_date/<start>/end_date/<end>")
def range_temp(start,end):

    # Declare the starting variables again
    start_date=start
    end_date=end

    #  performing the query to find the MAX, MIN and AVERAGE temperatures
    new_temp_ranges=session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).filter(Measurement.date >= start_date).filter(measurements.date <= end_date).all()

    # Convert the query into dictionary
    range_temps = [{'Min Temperature': min, 'Max Temperature': max, 'Average Temperature': avg} for min, max, avg in new_temp_ranges]
    
    # return Json file
    return jsonify(range_temps)


if __name__ == "__main__":
    app.run(debug=True)
