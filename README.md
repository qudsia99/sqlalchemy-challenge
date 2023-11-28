# sqlalchemy-challenge : Analysis and Observation of Hawaii's Climate + Designing a Climate App using Flask

### Part 1: Climate Analysis from .sqlite and CSV files

In this jupiter notebook file, with over 19,500 rows of observed data of Hawaii's climate in different regions, of percipitation and temperature changes with date stamps, I run a precipitation analysis and plot the findings via a bar graph, which highlights the highest and lowest periods of percipitation in a year for Hawaii. Then I design another query to find the temperature distribution by station distribution in Hawaii, plotted in a histogram form. 

### Part 2: FLASK API using queries from part 1

For this python file (app.py), I build a mini API app to access JSON routes, converting API data into Jsonified response objects.

#### Libraries used:

```
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from dateutil.relativedelta import relativedelta
```

### Preview of climate_starter.ipynb

#Find the most recent date in the data set.
newest = session.query(Measurement).order_by(Measurement.date.desc()).first()
print(newest.date)

#Design a query to retrieve the last 12 months of precipitation data and plot the results. 
#Starting from the most recent data point in the database. 

#Import a new date time module to extract data past weeks span
#as dt.timedelta only works for smaller ranges of time
from dateutil.relativedelta import relativedelta

#Calculate the date one year from the last date in data set.

query_date = dt.date(2017, 8, 23) - relativedelta(months=12)
print("Query Date: ", query_date)

#Perform a query to retrieve the data and precipitation scores
unique_precip_data = session.query(Measurement).filter(Measurement.date > '2016-08-23').all()

#Save the query results as a Pandas DataFrame. 
#Explicitly set the column names
precipitation_df = pd.DataFrame([{'date' : x.date, 'precipitation':x.prcp} for x in unique_precip_data])
precipitation_df.head()

#Sort the dataframe by date
precipitation_df.sort_values(by = 'date' ,ascending = True )

#Use Pandas Plotting with Matplotlib to plot the data
precipitation_df.plot.bar()
#precipitation_df.set_index('date', inplace=True)
indices = range(0, len(precipitation_df['date']), len(precipitation_df['date']) // 8)

#Get the corresponding dates based on the indices
selected_dates = [precipitation_df['date'][i] for i in indices]

#### Preview of app.py

@app.route("/api/v1.0/tobs")
def tobs():

    #Since we already found the most recent year in the data from our calculations earlier, we can utilize that
    query_date = dt.date(2017, 8, 23) - relativedelta(months=12)


    #perform query to find date and temperature readings again, but for previous year
    temp_and_year=session.query(measurements.date, measurements.tobs).filter(measurements.station=='USC00519281').\
                                            filter(measurements.date >= query_date).all()
    #Convert the query into a dictionary
    temperature_di = [{'Date': date, 'Temperature': temp} for date, temp in temp_and_year]

    #Close the session
    session.close()

    #return Json file
    return jsonify(temperature_di)
