import streamlit as st
import pandas as pd
from finalprojrevised import update_buses
from finalprojrevised import bus
import numpy as np
import pydeck as pdk
import time
# a = st.empty()
# a.write('gpu info')
buses = update_buses()
st.title('New Haven Bus Map')
st.subheader('Map of all buses')
lats = np.array([i.lat for i in buses])
lons = np.array([i.lon for i in buses])
d = {'latitude': lats,'longitude' :lons}


data = pd.DataFrame(data=d,data_green=[])

deck = pdk.Deck(map_style = 'mapbox://styles/mapbox/light-v9', initial_view_state=pdk.ViewState(latitude=41.31,longitude=-72.92,zoom=13,pitch=0),
    layers = [
        pdk.Layer('ScatterplotLayer',data=data,get_position='[longitude, latitude]',get_color='[200, 30, 0, 160]',get_radius=20),
        pdk.Layer('NH Green Layer',data=data_green,get_position='[longitude, latitude]',get_color='[0, 100, 0, 160]',get_radius=20)
    ]
           
)

def Index():
    buses = update_buses()
    lats = np.array([i.lat for i in buses])
    lons = np.array([i.lon for i in buses])
    d = {'latitude': lats,'longitude' :lons}
    data = pd.DataFrame(data=d)
    deck.update()
    print(deck)
    
def Index2():
    buses = update_buses()
    lats = np.array([i.lat for i in buses])
    lons = np.array([i.lon for i in buses])
    d = {'latitude': lats,'longitude' :lons}
    stops_green = [4331,4332,4333,4334,4336,4337]
    green_routes = stop_times.loc[stop_times['stop_id'].isin(stops_green)]
    green_trips = stop_times.loc[stop_times['route_id'].isin(green_routes)]['trip_id']
    green_buses = buses[buses.trip_id.isin(green_trips)]
    lats = np.array([i.lat for i in buses])
    lons = np.array([i.lon for i in buses])
    d = {'latitude': lats,'longitude' :lons}
    data = pd.DataFrame(data=d, data_green = dg)
    deck.update()
    print(deck)
    
st.button('Update', on_click=Index(), args=None, kwargs=None)
st.button('Buses that go to the green', on_click=Index(), args=None, kwargs=None)
st.pydeck_chart(deck)




