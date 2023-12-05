# -*- coding: utf-8 -*-
"""
Code to join data from separate CSV files, pre-process and aggregate
"""

# Imports
import pandas as pd
import os
from datetime import datetime
import numpy as np


# Script parameters
# -----------------

data_dir = "./data/dublinbikes_data"

columns = ["TIME", "BIKE STANDS", "AVAILABLE BIKE STANDS", 
           "STATUS", "ADDRESS", "LATITUDE", "LONGITUDE"]

pandemic_start = datetime.strptime("2020-03-12 00:00:00", '%Y-%m-%d %H:%M:%S')
pandemic_end = datetime.strptime("2022-03-31 23:59:59", '%Y-%m-%d %H:%M:%S')


# Join dublinbikes data into single dataframe
# -------------------------------------------

df_bikes = pd.DataFrame(columns=["station", "lat", "lon", "bike_usage", "timestamp", "pandemic"])
for filename in os.listdir(data_dir):
    print(filename)
    df = pd.read_csv(data_dir + "/" + filename)
    
    # Rename columns so that data directly downloadad from website and data collected using API are compatible
    df = df.rename(columns={"harvest_time" : "TIME",
                            "available_bike_stands" : "AVAILABLE BIKE STANDS",
                            "bike_stands" : "BIKE STANDS",
                            "status" : "STATUS",
                            "address" : "ADDRESS",
                            "latitude" : "LATITUDE",
                            "longitude" : "LONGITUDE",})
    
    # Filter out closed stations
    df = df[(df["STATUS"] == "Open") | (df["STATUS"] == "OPEN")]
    
    # Format station data
    df["timestamp"] = df["TIME"].astype('datetime64[ns]')
    df["station"] = df["ADDRESS"].astype("string")
    df["lon"] = df["LONGITUDE"]
    df["lat"] = df["LATITUDE"]
    df["capacity"] = df["BIKE STANDS"]
    df["bike_usage"] = df["AVAILABLE BIKE STANDS"] / df["BIKE STANDS"] * 100
    
    df["pandemic"] = np.where(df["timestamp"] < pandemic_start, 'pre-pandemic', 
                              np.where(df["timestamp"] > pandemic_end, 'post-pandemic', 'pandemic'))
    
    # Select columns
    df = df[["station", "lat", "lon", "bike_usage", "timestamp", "pandemic"]]
    
    df_bikes = pd.concat([df_bikes, df], ignore_index=True)

# Drop any duplicates
df_bikes = df_bikes.drop_duplicates(subset=['timestamp', 'station'])

# Cast column types
df_bikes['timestamp'] = df_bikes['timestamp'].astype('datetime64[ns]')
df_bikes['station'] = df_bikes['station'].astype('string')
df_bikes['pandemic'] = df_bikes['pandemic'].astype('string')
df_bikes['date'] = df_bikes["timestamp"].dt.date.astype('datetime64[ns]')


# Aggregate and save
# ------------------

# Aggregate by date for comparison with temperature data
df_agg = df_bikes[["date", "pandemic", "bike_usage"]]
df_agg = df_agg.groupby(["date", "pandemic"]).agg(['mean', 'std', 'sem']).reset_index()
df_agg.columns = ["date", "pandemic", 'average_bike_usage', 'std_bike_usage', 'sem_bike_usage']
df_agg["day_of_week"] = pd.to_datetime({'year':1970, 'month':1, 'day':5+df_agg['date'].dt.dayofweek}) # 01-01-1970 was a Thursday so the first Monday was on the 5th
df_agg["day"] = pd.to_datetime({'year':1970, 'month':1, 'day':df_agg['date'].dt.day})
df_agg["month"] = pd.to_datetime({'year':1970, 'month':df_agg['date'].dt.month, 'day':1})
df_agg.to_csv("./data/dublinbikes_data_agg-date.csv")

# Aggregate by station and time period to plot on map
df_agg = df_bikes[["station", "lat", "lon", "pandemic", "bike_usage"]]
df_agg = df_agg.groupby(["station", "lat", "lon", "pandemic"]).agg(['mean', 'std', 'sem']).reset_index()
df_agg.columns = ["station", "lat", "lon", "pandemic", 'average_bike_usage', 'std_bike_usage','sem_bike_usage']
df_agg.to_csv("./data/dublinbikes_data_agg-station.csv")

# Aggregate by station and hour for daily trends
df_agg = df_bikes[["date", "timestamp", "pandemic", "bike_usage"]]
df_agg["hour"] = pd.to_datetime({'year':1970, 'month':1, 'day':1, 'hour':df_bikes['timestamp'].dt.hour})
df_agg = df_agg.drop(columns=["timestamp"])
df_agg = df_agg.groupby(["date", "hour", "pandemic"]).agg(['mean', 'std', 'sem']).reset_index()
df_agg.columns = ["date", "hour", "pandemic", 'average_bike_usage', 'std_bike_usage','sem_bike_usage']
df_agg.to_csv("./data/dublinbikes_data_agg-hour.csv")
