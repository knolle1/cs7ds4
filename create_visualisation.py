# -*- coding: utf-8 -*-
"""
Data for creating visualisation to investigate effects of 
Covid-19 of public bike usage in Dublin.
"""

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Default public token
mapbox_access_token = "pk.eyJ1Ijoia25vbGxlMiIsImEiOiJjbHBsbzdxc2MwMXlrMmlwNjZncnFlNTYwIn0.oAe9EU2tXkl10y3UJn65xg"

BLUE = '#636EFA'
RED = '#EF553B'
GREEN = '#00CC96'

fig = make_subplots(
    rows=3, cols=3,
    specs=[[{'type': 'xy'}, {'type': 'mapbox'}, {'type': 'xy'}], 
           [{'type': 'xy'}, {'type': 'mapbox'}, {'type': 'xy'}], 
           [{'type': 'xy'}, {'type': 'mapbox'}, {'type': 'xy'}],],
    subplot_titles=["<b>Average Daily Bike Usage and Weather</b>",
                    "<b>Average Bike Usage Before/During/After Pandemic</b>",
                    "<b>Seasonal Trends in Bike Usage</b>",
                    None, None, None,
                    None, None, None],
    
    horizontal_spacing=0.06,
    vertical_spacing=0.05,
    shared_xaxes=True,
    )

# Update xaxis properties
fig.update_xaxes(title_text="Date", row=3, col=1, title_font=dict(size=12), title_standoff= 0)
fig.update_xaxes(title_text="Time", row=3, col=3, title_font=dict(size=12), title_standoff= 0)

# Update yaxis properties
fig.update_yaxes(title_text="Daily Average<br>Bike Usage [%]", row=1, col=1, title_font=dict(size=12), title_standoff= 0)
fig.update_yaxes(title_text="Temperature [°C]", row=2, col=1, title_font=dict(size=12), title_standoff= 0)
fig.update_yaxes(title_text="Rainfall [mm]", row=3, col=1, title_font=dict(size=12), title_standoff= 0)

fig.update_yaxes(title_text="Hourly/Daily<br>Average Bike Usage [%]", row=1, col=3, title_font=dict(size=12), title_standoff= 0)
fig.update_yaxes(title_text="Hourly/Daily<br>Average Bike Usage [%]", row=2, col=3, title_font=dict(size=12), title_standoff= 0)
fig.update_yaxes(title_text="Hourly/Daily<br>Average Bike Usage [%]", row=3, col=3, title_font=dict(size=12), title_standoff= 0)


###############################################################################
# Plot first column - bike usage and weather
###############################################################################

# Load dublinbikes data
df_bikes = pd.read_csv("./data/dublinbikes_data_agg-date.csv")
df_bikes['date'] = df_bikes['date'].astype('datetime64[ns]')
df_bikes['pandemic'] = df_bikes['pandemic'].astype('string')
df_bikes['average_bike_usage'] = df_bikes['average_bike_usage'].astype('float')
df_bikes['std_bike_usage'] = df_bikes['std_bike_usage'].astype('float')


#  Plot average bike usage over time
# -----------------------------------

df = df_bikes[df_bikes["pandemic"] == "pre-pandemic"]
fig.add_trace(go.Scatter(x=df["date"], 
                         y=df["average_bike_usage"], 
                         mode='lines', 
                         line=dict(color = BLUE),
                         name='Pre-pandemic',
                         hoverinfo='text+name',
                         text = ("Date: " + df['date'].dt.strftime('%Y-%m-%d') + 
                                 "<br>Average bike usage: " + df['average_bike_usage'].round(2).astype('string') + ' %' +
                                 "<br>Std. dev.: " + df['std_bike_usage'].round(2).astype('string') + ' %'),
                         showlegend=True),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df["date"], 
                         y=df["average_bike_usage"]+df["std_bike_usage"], 
                         mode='lines', 
                         line=dict(color = BLUE, width=0),
                         name='Pre-pandemic',
                         hoverinfo='skip',
                         showlegend=False),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df["date"], 
                         y=df["average_bike_usage"]-df["std_bike_usage"], 
                         mode='lines', 
                         line=dict(color = BLUE, width=0),
                         fill='tonexty',
                         name='Pre-pandemic',
                         hoverinfo='skip',
                         showlegend=False),
              row=1, col=1)

df = df_bikes[df_bikes["pandemic"] == "pandemic"]
fig.add_trace(go.Scatter(x=df["date"], 
                         y=df["average_bike_usage"], 
                         mode='lines', 
                         line=dict(color = RED),
                         name='Pandemic',
                         hoverinfo='text+name',
                         text = ("Date: " + df['date'].dt.strftime('%Y-%m-%d') + 
                                 "<br>Average bike usage: " + df['average_bike_usage'].round(2).astype('string') + ' %' +
                                 "<br>Std. dev.: " + df['std_bike_usage'].round(2).astype('string') + ' %'),
                         showlegend=True),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df["date"], 
                         y=df["average_bike_usage"]+df["std_bike_usage"], 
                         mode='lines', 
                         line=dict(color = RED, width=0),
                         name='Pre-pandemic',
                         hoverinfo='skip',
                         showlegend=False),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df["date"], 
                         y=df["average_bike_usage"]-df["std_bike_usage"], 
                         mode='lines', 
                         line=dict(color = RED, width=0),
                         fill='tonexty',
                         name='Pre-pandemic',
                         hoverinfo='skip',
                         showlegend=False),
              row=1, col=1)

df = df_bikes[df_bikes["pandemic"] == "post-pandemic"]
fig.add_trace(go.Scatter(x=df["date"], 
                         y=df["average_bike_usage"], 
                         mode='lines', 
                         line=dict(color = GREEN),
                         name='Post-pandemic',
                         hoverinfo='text+name',
                         text = ("Date: " + df['date'].dt.strftime('%Y-%m-%d') + 
                                 "<br>Average bike usage: " + df['average_bike_usage'].round(2).astype('string') + ' %' +
                                 "<br>Std. dev.: " + df['std_bike_usage'].round(2).astype('string') + ' %'),
                         showlegend=True),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df["date"], 
                         y=df["average_bike_usage"]+df["std_bike_usage"], 
                         mode='lines', 
                         line=dict(color = GREEN, width=0),
                         name='Pre-pandemic',
                         hoverinfo='skip',
                         showlegend=False),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df["date"], 
                         y=df["average_bike_usage"]-df["std_bike_usage"], 
                         mode='lines', 
                         line=dict(color = GREEN, width=0),
                         fill='tonexty',
                         name='Pre-pandemic',
                         hoverinfo='skip',
                         showlegend=False),
              row=1, col=1)


#  Plot temperature and rainfall data
# ------------------------------------

# Load weather data
df_temp = pd.read_csv("./data/meteo_data.csv", skiprows=12)
df_temp['date'] = df_temp['date'].astype('datetime64[ns]')
df_temp['mint'] = pd.to_numeric(df_temp['mint'], errors='coerce')
df_temp['maxt'] = pd.to_numeric(df_temp['maxt'], errors='coerce')
df_temp = df_temp[(df_temp['date'] >= np.min(df_bikes['date'])) & (df_temp['date'] <= np.max(df_bikes['date']))]

fig.add_trace(go.Scatter(x=df_temp["date"], 
                         y=df_temp["mint"], 
                         mode='lines', 
                         line=dict(color = 'darkslateblue'),
                         hoverinfo='text',
                         text = ("Date: " + df_temp['date'].dt.strftime('%Y-%m-%d') + 
                                 "<br>Min. temperature: " + df_temp["mint"].astype('string') + "°C"),
                         showlegend=False),
              row=2, col=1)

fig.add_trace(go.Scatter(x=df_temp["date"], 
                         y=df_temp["maxt"], 
                         mode='lines', 
                         line=dict(color = 'darkslateblue'),
                         hoverinfo='text',
                         text = ("Date: " + df_temp['date'].dt.strftime('%Y-%m-%d') + 
                                 "<br>Max. temperature: " + df_temp["maxt"].astype('string') + "°C"),
                         fill='tonexty',
                         showlegend=False),
              row=2, col=1)

fig.add_trace(go.Scatter(x=df_temp["date"], 
                         y=df_temp["rain"], 
                         mode='lines', 
                         line=dict(color = 'darkslateblue'),
                         hoverinfo='text',
                         text = ("Date: " + df_temp['date'].dt.strftime('%Y-%m-%d') + 
                                 "<br>Rainfall: " + df_temp["rain"].astype('string') + "mm"),
                         showlegend=False),
              row=3, col=1)

###############################################################################
# Plot second column - maps
###############################################################################

# Load dublinbikes data
df_bikes = pd.read_csv("./data/dublinbikes_data_agg-station.csv")
df_bikes['station'] = df_bikes['station'].astype('string')
df_bikes['lat'] = df_bikes['lat'].astype('float')
df_bikes['lon'] = df_bikes['lon'].astype('float')
df_bikes['pandemic'] = df_bikes['pandemic'].astype('string')
df_bikes['average_bike_usage'] = df_bikes['average_bike_usage'].astype('float')

#  Plot average bike usage and geo data
# -------------------------------------

df = df_bikes[df_bikes["pandemic"] == "pre-pandemic"]
fig.add_trace(go.Scattermapbox(lat = df['lat'],
                               lon = df['lon'],
                               mode = 'markers',
                               marker = go.scattermapbox.Marker(color = BLUE,
                                                                sizeref = 10,
                                                                size = df['average_bike_usage']),
                               text = (df['station'] + "<br>Average bike usage: " 
                                       + df['average_bike_usage'].round(2).astype('string') + ' %'),
                               name='Pre-pandemic',
                               showlegend=False
                              ),
              row=1, col=2)

df = df_bikes[df_bikes["pandemic"] == "pandemic"]
fig.add_trace(go.Scattermapbox(lat = df['lat'],
                               lon = df['lon'],
                               mode = 'markers',
                               marker = go.scattermapbox.Marker(color = RED,
                                                                sizeref = 10,
                                                                size = df['average_bike_usage']),
                               text = (df['station'] + "<br>Average bike usage: " 
                                       + df['average_bike_usage'].round(2).astype('string') + ' %'),
                               name='Pandemic',
                               showlegend=False
                              ),
              row=2, col=2)

df = df_bikes[df_bikes["pandemic"] == "post-pandemic"]
fig.add_trace(go.Scattermapbox(lat = df['lat'],
                               lon = df['lon'],
                               mode = 'markers',
                               marker = go.scattermapbox.Marker(color = GREEN,
                                                                sizeref = 10,
                                                                size = df['average_bike_usage']),
                               text = (df['station'] + "<br>Average bike usage: " 
                                       + df['average_bike_usage'].round(2).astype('string') + ' %'),
                               name='Post-pandemic',
                               showlegend=False
                              ),
              row=3, col=2)


###############################################################################
# Plot third column - seasonal trends
###############################################################################

#  Plot data for daily trends
# ---------------------------

# Load dublinbikes data
df_bikes = pd.read_csv("./data/dublinbikes_data_agg-hour.csv")
df_bikes['hour'] = df_bikes['hour'].astype('datetime64[ns]')
df_bikes['pandemic'] = df_bikes['pandemic'].astype('string')
df_bikes['average_bike_usage'] = df_bikes['average_bike_usage'].astype('float')

df = df_bikes[df_bikes["pandemic"] == "pre-pandemic"]
fig.add_trace(go.Box(x=df["hour"], 
                     y=df["average_bike_usage"], 
                     #mode='markers', 
                     line=dict(color = BLUE),
                     name='Pre-pandemic',
                     showlegend=False, ),
              row=1, col=3)

df = df_bikes[df_bikes["pandemic"] == "pandemic"]
fig.add_trace(go.Box(x=df["hour"], 
                     y=df["average_bike_usage"], 
                     #mode='markers', 
                     line=dict(color = RED),
                     name='Pandemic',
                     showlegend=False),
              row=2, col=3)

df = df_bikes[df_bikes["pandemic"] == "post-pandemic"]
fig.add_trace(go.Box(x=df["hour"], 
                     y=df["average_bike_usage"],
                     #mode='markers', 
                     line=dict(color = GREEN),
                     name='Post-pandemic',
                     showlegend=False),
              row=3, col=3)

fig.update_xaxes(tickformat="%H:%S", row=1, col=3)
fig.update_xaxes(tickformat="%H:%S", row=2, col=3)
fig.update_xaxes(tickformat="%H:%S", row=3, col=3)


#  Plot data for weekly trends
# ----------------------------

# Load dublinbikes data
df_bikes = pd.read_csv("./data/dublinbikes_data_agg-date.csv")
df_bikes['day_of_week'] = df_bikes['day_of_week'].astype('datetime64[ns]')
df_bikes['day'] = df_bikes['day'].astype('datetime64[ns]')
df_bikes['month'] = df_bikes['month'].astype('datetime64[ns]')
df_bikes['pandemic'] = df_bikes['pandemic'].astype('string')
df_bikes['average_bike_usage'] = df_bikes['average_bike_usage'].astype('float')

df = df_bikes[df_bikes["pandemic"] == "pre-pandemic"]
fig.add_trace(go.Box(x=df["day_of_week"], 
                     y=df["average_bike_usage"], 
                     #mode='markers', 
                     line=dict(color = BLUE),
                     name='Pre-pandemic',
                     showlegend=False,
                     visible=False),
              row=1, col=3)

df = df_bikes[df_bikes["pandemic"] == "pandemic"]
fig.add_trace(go.Box(x=df["day_of_week"], 
                     y=df["average_bike_usage"], 
                     #mode='markers', 
                     line=dict(color = RED),
                     name='Pandemic',
                     showlegend=False,
                     visible=False),
              row=2, col=3)

df = df_bikes[df_bikes["pandemic"] == "post-pandemic"]
fig.add_trace(go.Box(x=df["day_of_week"], 
                     y=df["average_bike_usage"], 
                     #mode='markers', 
                     line=dict(color = GREEN),
                     name='Post-pandemic',
                     showlegend=False,
                     visible=False),
              row=3, col=3)


#  Plot data for monthly trends
# -----------------------------

df = df_bikes[df_bikes["pandemic"] == "pre-pandemic"]
fig.add_trace(go.Box(x=df["day"], 
                     y=df["average_bike_usage"], 
                     #mode='markers', 
                     line=dict(color = BLUE),
                     name='Pre-pandemic',
                     showlegend=False,
                     visible=False),
              row=1, col=3)

df = df_bikes[df_bikes["pandemic"] == "pandemic"]
fig.add_trace(go.Box(x=df["day"], 
                     y=df["average_bike_usage"], 
                     #mode='markers', 
                     line=dict(color = RED),
                     name='Pandemic',
                     showlegend=False,
                     visible=False),
              row=2, col=3)

df = df_bikes[df_bikes["pandemic"] == "post-pandemic"]
fig.add_trace(go.Box(x=df["day"], 
                     y=df["average_bike_usage"], 
                     #mode='markers', 
                     line=dict(color = GREEN),
                     name='Post-pandemic',
                     showlegend=False,
                     visible=False),
              row=3, col=3)


#  Plot data for annual trends
# ----------------------------

df = df_bikes[df_bikes["pandemic"] == "pre-pandemic"]
fig.add_trace(go.Box(x=df["month"], 
                     y=df["average_bike_usage"], 
                     #mode='markers', 
                     line=dict(color = BLUE),
                     name='Pre-pandemic',
                     showlegend=False, 
                     visible=False),
              row=1, col=3)

df = df_bikes[df_bikes["pandemic"] == "pandemic"]
fig.add_trace(go.Box(x=df["month"], 
                     y=df["average_bike_usage"], 
                     #mode='markers', 
                     line=dict(color = RED),
                     name='Pandemic',
                     showlegend=False,
                     visible=False),
              row=2, col=3)

df = df_bikes[df_bikes["pandemic"] == "post-pandemic"]
fig.add_trace(go.Box(x=df["month"], 
                     y=df["average_bike_usage"],
                     #mode='markers', 
                     line=dict(color = GREEN),
                     name='Post-pandemic',
                     showlegend=False,
                     visible=False),
              row=3, col=3)

###############################################################################
# Create dropdown menu
###############################################################################

updatemenus = list([
    dict(active=0,
         yanchor="top",
         y=0.85,
         xanchor='left',
         x=1.01,
         buttons=list([   
            dict(label = 'Daily trends',
                 method = 'update',
                 args = [{'visible': [True]*15+[True]*3+[False]*3+[False]*3+[False]*3},
                         {'xaxis2.tickformat':'%H:%S',
                          'xaxis4.tickformat':'%H:%S',
                          'xaxis6.tickformat':'%H:%S',
                          'xaxis6.title':'Time'}
                         ]),
            dict(label = 'Weekly trends',
                 method = 'update',
                 args = [{'visible': [True]*15+[False]*3+[True]*3+[False]*3+[False]*3},
                         {'xaxis2.tickformat':'%a',
                          'xaxis4.tickformat':'%a',
                          'xaxis6.tickformat':'%a',
                          'xaxis6.title':'Day of the Week'}
                         ]),
            dict(label = 'Monthly trends',
                 method = 'update',
                 args = [{'visible': [True]*15+[False]*3+[False]*3+[True]*3+[False]*3},
                         {'xaxis2.tickformat':'%d',
                          'xaxis4.tickformat':'%d',
                          'xaxis6.tickformat':'%d',
                          'xaxis6.title':'Day of the Month'}
                         ]),
            dict(label = 'Annual trends',
                 method = 'update',
                 args = [{'visible': [True]*15+[False]*3+[False]*3+[False]*3+[True]*3},
                         {'xaxis2.tickformat':'%b',
                          'xaxis4.tickformat':'%b',
                          'xaxis6.tickformat':'%b',
                          'xaxis6.title':'Month'}
                         ]),
        ]),
    )
])

###############################################################################
# Update layouts
###############################################################################

fig.update_layout(title_text = 'Effects of Covid-19 on Public Bike Use in Dublin<br><span style="font-size: 12px">Bike usage defined as percentage of bike stands of a station that are available (i.e. not occupied by a bike).<br>Covid-19 pandemic defined as time period during which regulations and protective measures were in place (2020-03-12 to 2022-03-31).<br>Data sources: <a href="https://data.gov.ie/dataset/dublinbikes-api">data.gov.ie (Dublinbikes API)</a>, <a href="https://www.met.ie/climate/available-data/historical-data">www.met.ie</a> and <a href="https://www.citizensinformation.ie/en/health/covid19/public-health-measures-for-covid19/">www.citizensinformation.ie</a></span>',
                  title_x=0.5,
                  margin = dict(t = 150),
                  title_y=0.95,
                  #title_pad_b=64,
                  hovermode='closest',
                  
                  legend=dict(yanchor="top",
                              y=1,
                              xanchor="left",
                              x=1.01),
                  
                  updatemenus=updatemenus,
                  
                  mapbox=dict(accesstoken=mapbox_access_token,
                              bearing=0,
                              center=go.layout.mapbox.Center(lat=53.345,lon=-6.27),
                              pitch=0,
                              zoom=10.8
                             ),
                  mapbox2=dict(accesstoken=mapbox_access_token,
                               bearing=0,
                               center=go.layout.mapbox.Center(lat=53.345,lon=-6.27),
                               pitch=0,
                               zoom=10.8
                               ),
                  mapbox3=dict(accesstoken=mapbox_access_token,
                               bearing=0,
                               center=go.layout.mapbox.Center(lat=53.345,lon=-6.27),
                               pitch=0,
                               zoom=10.8
                               ),
                  height=750,
                  
                  yaxis = dict(tickfont = dict(size=10)),
                  yaxis2 = dict(tickfont = dict(size=10)),
                  yaxis3 = dict(tickfont = dict(size=10)),
                  yaxis4 = dict(tickfont = dict(size=10)),
                  yaxis5 = dict(tickfont = dict(size=10)),
                  yaxis6 = dict(tickfont = dict(size=10)),
                  
                  xaxis = dict(tickfont = dict(size=10)),
                  xaxis2 = dict(tickfont = dict(size=10)),
                  xaxis3 = dict(tickfont = dict(size=10)),
                  xaxis4 = dict(tickfont = dict(size=10)),
                  xaxis5 = dict(tickfont = dict(size=10)),
                  xaxis6 = dict(tickfont = dict(size=10)),
                  
                  xaxis_showticklabels=True, 
                  xaxis2_showticklabels=True, 
                  xaxis3_showticklabels=True, 
                  xaxis4_showticklabels=True,  
                  xaxis5_showticklabels=True,
                  xaxis6_showticklabels=True,  

                  )

fig.update_annotations(font_size=12)

#fig.show()
fig.write_html("dublinbikes_covid19_visualisation.html")