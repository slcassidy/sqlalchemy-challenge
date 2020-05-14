import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from dateutil.relativedelta import relativedelta
from datetime import datetime

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/[Enter Start Date]  <br/>"
        f"/api/v1.0/[Enter Start Date]/[Enter End Date]"
        #f""
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    results = session.query(Measurement.station,Measurement.date, Measurement.prcp).all()

    session.close()

    precip_all = []
    for station, date, prcp in results:
        precip_dict = {}
        precip_dict["station"] = station
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_all.append(precip_dict)

    return jsonify(precip_all)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Return a JSON list of stations
    results = session.query(Station.station).all()

    session.close()

    # show list
       # Convert list of tuples into normal list
    station_info = list(np.ravel(results))

    return jsonify(station_info)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
        # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    print(last_date)
    #Unpacking the lastdate so it does not have the () around it
    last_date_strip = datetime.strptime(str(last_date[0]), "%Y-%m-%d")
    print(last_date_strip)
    #Identify a year ago
    query_date = last_date_strip - dt.timedelta(days=365)
    print(f"Query Date is {query_date}")
    #str(last_date)
    """Return a list of TOBs"""
    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    results = tw_month_measure = session.query(Measurement.date, Measurement.tobs\
                                        ).filter(Measurement.date >= query_date).all()

    session.close()

    precip_tobs_all = []
    for date, tobs in results:
        precip_tobs_dict = {}
#        precip_tobs_dict["station"] = station
        precip_tobs_dict["date"] = date
        precip_tobs_dict["tobs"] = tobs
        precip_tobs_all.append(precip_tobs_dict)

    return jsonify(precip_tobs_all)

@app.route("/api/v1.0/<start>")
def calc_temps_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #start='2012-02-28'
    #end='2012-03-05'

    station_cal = [func.min(Measurement.prcp), 
       func.max(Measurement.prcp), 
       func.avg(Measurement.prcp)] 

    results = session.query(*station_cal).filter(Measurement.date >= start).all()  

    session.close()

    precip_start = []
    for min_prcp, avg_prcp, max_prcp in results:
        precip_dates = {}
        precip_dates["min_prec"] = min_prcp
        precip_dates["avg_prec"] = avg_prcp
        precip_dates["max_prec"] = max_prcp
        precip_start.append(precip_dates)

    return jsonify(precip_start)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #start='2012-02-28'
    #end='2012-03-05'

    station_cal = [func.min(Measurement.prcp), 
       func.max(Measurement.prcp), 
       func.avg(Measurement.prcp)] 

    results = session.query(*station_cal).filter(Measurement.date >= start)\
                            .filter(Measurement.date <= end).all()  

    session.close()

    precip_SE_date = []
    for min_prcp, avg_prcp, max_prcp in results:
        precip_dates = {}
        precip_dates["min_prec"] = min_prcp
        precip_dates["avg_prec"] = avg_prcp
        precip_dates["max_prec"] = max_prcp
        precip_SE_date.append(precip_dates)

    return jsonify(precip_SE_date)



if __name__ == '__main__':
    app.run(debug=True)
