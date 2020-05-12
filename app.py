import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Vacation = Base.classes.hawaii

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
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        #f""
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    results = session.query(Vacation.station,Vacation.date, Vacation.prcp).all()

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
    results = session.query(Vacation.station).all()

    session.close()

    # show list
       # Convert list of tuples into normal list
    station_info = list(np.ravel(results))

    return jsonify(station_info)


if __name__ == '__main__':
    app.run(debug=True)
