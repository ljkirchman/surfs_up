# import dependencies
import datetime as dt
import numpy as np
# import pandas as pd

# import dependencies from sqlalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import dependencies from flask
from flask import Flask, jsonify

# access SQLlite db
engine = create_engine("sqlite:////Users/ljkirchman/Desktop/DataVis/Classwork/surfs_up/hawaii.sqlite")


# reflect the database in our classes
Base = automap_base()

# reflect the database
Base.prepare(engine, reflect=True)

# save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# define our Flask app
app = Flask(__name__)


# Create welcome routes
@app.route("/")

def welcome():
	return(
    '''
      Welcome to the Climate Analysis API!
      <h1>Available Routes:</h1>
      <ul>
            <li><a href='/api/v1.0/precipitation'>Precipitation</a></li>
            <li><a href='/api/v1.0/stations'>Stations</a></li>
            <li><a href='/api/v1.0/tobs'>Temperature Obs.</a></li>
            <li><a href='/api/v1.0/temp/2017-06-01/2017-06-31'>Modify dates</a></li>
      </ul>
    ''')

# Create route for precipitation analysis
@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 5, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Create a route for stations
@app.route("/api/v1.0/stations")

def stations():
   results = session.query(Station.station).all()
   stations = list(np.ravel(results))
   return jsonify(stations)

# Create a route for monthly temperature
@app.route("/api/v1.0/tobs")

def temp_monthly():
   prev_year = dt.date(2017, 5, 23) - dt.timedelta(days=365)
	   
   results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
   temps = list(np.ravel(results))
   return jsonify(temps)

# Create a statistics route
#@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
   sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

   if not end: 
     results = session.query(*sel).\
         filter(Measurement.date >= start).all()
     temp = list(np.ravel(results))
     return jsonify(temp)

   results = session.query(*sel).\
        filter(Measurement.date >= start).\
      filter(Measurement.date <= end).all()
   temps = list(np.ravel(results))
   print(temps)
   return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)