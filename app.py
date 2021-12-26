########################  Welcome ########################  
#To Transit! An app tracking CTTransit buses created by Helena for ASTR 330

########################  Import Statements ########################  
import streamlit as st
import pandas as pd
from functions import update_buses
from functions import bus
from functions import make_buses_into_dataframe
from functions import make_bus_into_dataframe
from functions import stop_times
from functions import stops 
from functions import func
from functions import bus_speed_image
from functions import determine_direction
from functions import which_stop_is_next
from functions import make_schedule_into_dataframe
import numpy as np
import pydeck as pdk
import time
import matplotlib.pyplot as plt

########################  Set up session state variables ########################  
if 'running' not in st.session_state:
    st.session_state['running'] = True 
if 'green' not in st.session_state:
    st.session_state['green'] = False 
if 'emph' not in st.session_state:
    st.session_state['emph'] = False
if 'emphstop' not in st.session_state:
    st.session_state['emphstop'] = False

########################  Headers and information ########################
st.title('TRANSIT: A New Haven Bus Map')
st.subheader('Here you can track the buses in New Haven and use our interactive features.')
st.write('Note: this app runs on real time data from CTTransit. If buses are not currently running, check the box below to see a demo.')

########################  Demo setting: for use if there are no buses currently running but you want to see the app in action ########################  
agree = st.checkbox('Demo Please')

demo=False
if agree:
     demo=True

########################  Making the Map ########################       
def make_original_layer():
    buses = update_buses(demo)
    my_dataframe = make_buses_into_dataframe(buses)

    data = pd.DataFrame(data=my_dataframe)

    layer_original = pdk.Layer('ScatterplotLayer',data=data,get_position='[longitude, latitude]',get_color='[200, 30, 0, 160]',get_radius=20)
    return layer_original, buses, my_dataframe

def make_deck(my_layers):
    deck = pdk.Deck(map_style = 'mapbox://styles/mapbox/light-v9', initial_view_state=pdk.ViewState(latitude=41.31,longitude=-72.92,zoom=13,pitch=0),
        layers = my_layers          
    )
    return deck

layer_original, buses, my_dataframe = make_original_layer()

my_layers =  [layer_original]

deck = make_deck(my_layers)

######################## Making the Feature Buttons ######################## 

col1, col2, col3, col4 = st.columns(4)

def Index():
    buses = update_buses(demo)
    d = make_buses_into_dataframe(buses)
    data = pd.DataFrame(data=d)
    deck.update()

########################  Update Bus Locations ########################  

col1.button('Update Buses', on_click=Index(), args=None, kwargs=None)

########################  Refresh Extra Features ########################  
if col2.button('Refresh Features'):
    st.session_state.green=False
    st.session_state.emph=False
    st.session_state.emphstop=False
    
########################  Buses that go to the New Haven green ########################  

def make_green_layer(buses):
    stops_green = [4331,4332,4333,4334,4336,4337]
    
    green_trips = stop_times.loc[stop_times['stop_id'].isin(stops_green)]['trip_id'].unique()

    green_buses = []
    for i in buses:
        if(np.isin(i.trip_id,green_trips)):
            green_buses.append(i)
    d_green = make_buses_into_dataframe(green_buses)
    data_green = pd.DataFrame(data=d_green)
    layer_green = pdk.Layer('ScatterplotLayer',data=data_green, get_position='[longitude, latitude]',get_color='[0, 250, 0]',get_radius=20)
    return layer_green

if col3.button('Buses that go to the green'):
    st.session_state.green=True
    layer_original, buses, my_dataframe = make_original_layer()
    layer_green = make_green_layer(buses)
    my_layers =  [layer_original,layer_green]   
    deck = make_deck(my_layers)
    deck.update()
    
else:
    print('waiting')

########################  Emphasize a bus button ########################  
    
num4 = st.sidebar.text_input('Enter the bus number and press the Emphasize Bus button to emphasize it on the map',value=40)

def make_emphasis_layer(buses,num4):
    d_emphasize = make_bus_into_dataframe(buses,int(num4))
    data_emphasize = pd.DataFrame(data=d_emphasize)
    layer_emphasize = pdk.Layer('ScatterplotLayer',data=data_emphasize, get_position='[longitude, latitude]',get_color='[0, 0, 250]',get_radius=100)
    return layer_emphasize
    
if st.sidebar.button('Emphasize Bus'):
    st.session_state.emph=True
    layer_original, buses, my_dataframe = make_original_layer()
    
    try:        
        layer_emphasize = make_emphasis_layer(buses,num4)
        my_layers =  [layer_original,layer_emphasize]
        deck = make_deck(my_layers)
        deck.update()
    except:
        st.write('Sorry, that bus is not online right now')
    
else:
    print('waiting')

########################  Emphasize a stop button ########################  

num41 = st.sidebar.text_input('Enter a stop name and press the See Stop button to see it on the map',value='Elm St and Temple St')

def make_stop_emphasis_layer(buses,num41,stops):
    stop_name = num41
    stop_row = stops[stops['stop_name']==stop_name]
    stop_id = []
    latitude = []
    longitude = []
    for i in stop_row['stop_id']:
        stop_id.append(i)
    for i in stop_row['stop_lat']:
        latitude.append(i)
    for i in stop_row['stop_lon']:
        longitude.append(i)
    d_emphasize = pd.DataFrame()
    d_emphasize['stop_id'] = stop_id
    d_emphasize['latitude'] = latitude
    d_emphasize['longitude'] = longitude
    data_emphasize = pd.DataFrame(data=d_emphasize)
    layer_emphasize = pdk.Layer('ScatterplotLayer',data=data_emphasize, get_position='[longitude, latitude]',get_color='[100, 0, 100]',get_radius=100)
    return layer_emphasize


if st.sidebar.button('See Stop'):
    st.session_state.emphstop=True
    layer_original, buses, my_dataframe = make_original_layer()
    try:        
        layer_emphasize = make_stop_emphasis_layer(buses,num41,stops)
        my_layers =  [layer_original,layer_emphasize]
        deck = make_deck(my_layers)
        deck.update()
    except:
        st.write('Sorry, that is not an existing stop')
    
else:
    print('waiting')

########################  Session state variables that will allow these features to stay on the map even when refreshing ########################  

if st.session_state.emphstop:
    layer_original, buses, my_dataframe = make_original_layer()       
    layer_emphasize = make_stop_emphasis_layer(buses,num41,stops)
    my_layers =  [layer_original,layer_emphasize]
    deck = make_deck(my_layers)
    deck.update()
    
if st.session_state.green:
    layer_original, buses, my_dataframe = make_original_layer()
    layer_green = make_green_layer(buses)
    my_layers =  [layer_original,layer_green]   
    deck = make_deck(my_layers)
    deck.update()
    
if st.session_state.emph:
    layer_original, buses, my_dataframe = make_original_layer()    
    try:        
        layer_emphasize = make_emphasis_layer(buses,num4)
        my_layers =  [layer_original,layer_emphasize]
        deck = make_deck(my_layers)
        deck.update()
    except:
        st.write('Sorry, that bus is not online right now')

if st.session_state.green and st.session_state.emph:
    layer_original, buses, my_dataframe = make_original_layer()
    layer_green = make_green_layer(buses)
    try:        
        layer_emphasize = make_emphasis_layer(buses,num4)
        my_layers =  [layer_original,layer_green,layer_emphasize]
        deck = make_deck(my_layers)
        deck.update()
    except:
        st.write('Sorry, that bus is not online right now')
        my_layers =  [layer_original,layer_green]
        deck = make_deck(my_layers)
        deck.update()
        
if st.session_state.green and st.session_state.emphstop:
    layer_original, buses, my_dataframe = make_original_layer()
    layer_green = make_green_layer(buses)
    try:        
        layer_emphasize = make_stop_emphasis_layer(buses,num41,stops)
        my_layers =  [layer_original,layer_green,layer_emphasize]
        deck = make_deck(my_layers)
        deck.update()
    except:
        st.write('Sorry, that bus is not online right now')
        my_layers =  [layer_original,layer_green]
        deck = make_deck(my_layers)
        deck.update()
    
if st.session_state.emph and st.session_state.emphstop:
    layer_original, buses, my_dataframe = make_original_layer()
    try:        
        layer_emphasize = make_emphasis_layer(buses,num4)
        layer_emphasize2 = make_stop_emphasis_layer(buses,num41,stops)
        my_layers =  [layer_original,layer_emphasize,layer_emphasize2]
        deck = make_deck(my_layers)
        deck.update()
    except:
        st.write('Sorry, that bus is not online right now')
        my_layers =  [layer_original]
        deck = make_deck(my_layers)
        deck.update()
    
if st.session_state.green and st.session_state.emph and st.session_state.emphstop:
    layer_original, buses, my_dataframe = make_original_layer()
    layer_green = make_green_layer(buses)
    try:        
        layer_emphasize = make_emphasis_layer(buses,num4)
        layer_emphasize2 = make_stop_emphasis_layer(buses,num41,stops)
        my_layers =  [layer_original,layer_green,layer_emphasize,layer_emphasize2]
        deck = make_deck(my_layers)
        deck.update()
    except:
        st.write('Sorry, that bus is not online right now')
        my_layers =  [layer_original,layer_green]
        deck = make_deck(my_layers)
        deck.update()

####################### More Special Features Found on the Sidebar ########################   
 
buses = update_buses(demo)

########################  Enter bus number to find next scheduled stop ########################  
num = st.sidebar.text_input('Enter the bus number to find out its next scheduled stop',value=40)
st.sidebar.write('The next stop is', func(num,buses,stop_times,stops,demo))

########################  Enter bus number to find the stop it's closest to ########################  
num1 = st.sidebar.text_input('Enter the bus number to find out which stop it is currently closest to',value=40)
st.sidebar.write('The closest stop is', which_stop_is_next(buses,int(num1),stops,stop_times,demo))

########################  Enter bus number to see a visual of its speed and direction ########################  
num2 = st.sidebar.text_input('Enter the bus number to find out how fast it is going',value=40)
fig,ax = plt.subplots(figsize=(10,10))
fig,ax,direction,speed = bus_speed_image(int(num2),buses,fig,ax)
st.sidebar.write('The bus is going in mph ', speed,' in the direction ', direction)
st.sidebar.pyplot(fig)

########################  Displaying map ########################  
st.pydeck_chart(deck)

########################  Print buses in New Haven right now ########################  
st.subheader('Which buses are in Downtown New Haven right now?')
my_dataframe = make_buses_into_dataframe(buses)
my_dataframe_abridged = my_dataframe.drop(columns=['latitude', 'longitude','trip_id'])
st.write(my_dataframe_abridged)

########################  Print schedule for a particular bus ########################  
st.subheader('Display the schedule for the bus you are interested in!')
num5 = st.text_input('Enter the bus number to see its schedule:',value=40) 

if st.button('Display'):
    bus = buses[int(num5)]
    trip_id = int(bus.trip_id)
    relevant_stops = stop_times.loc[stop_times['trip_id']==trip_id]
    schedule = make_schedule_into_dataframe(relevant_stops,stops)
    st.write(schedule)
else:
    print('waiting')

########################  Celebrate! ########################$ 
if st.button('Celebrate'):
    st.balloons()
else:
    print('waiting')
