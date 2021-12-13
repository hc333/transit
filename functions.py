########################  For TRANSIT, an app made for ASTR 330 ########################  
########################  Here is where many of the functions for the app are stored ########################  
import urllib, json
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
import pandas as pd
import time 
from PIL import Image
import datetime
import streamlit as st
import pydeck as pdk

shapes = pd.read_csv('shapes.txt')
trips = pd.read_csv('trips.txt')
stop_times = pd.read_csv('stop_times.txt')
trips = pd.read_csv('trips.txt')
stops = pd.read_csv('stops.txt')
fig,ax = plt.subplots(figsize=(10,10))

def draw_map(fig,ax):
    #Road lines
    map = gpd.read_file('Trans_RoadSegment.shp')
    map.plot(ax=ax)
    ax.set_xlim(-72.98,-72.88)
    ax.set_ylim(41.26,41.355)
    #ax.set_ylim(41.29,41.33)

class bus():
    def __init__(self, new_data, number):
        self.lat = new_data['entity'][number]['vehicle']['position']['latitude']
        self.lon = new_data['entity'][number]['vehicle']['position']['longitude']
        try:
            self.bearing = new_data['entity'][number]['vehicle']['position']['bearing']
        except:
            self.bearing = 0
        self.vehicleid = new_data['entity'][number]['vehicle']['vehicle']['id']
        self.trip_id = new_data['entity'][number]['vehicle']['trip']['trip_id']
        self.route_id = new_data['entity'][number]['vehicle']['trip']['route_id']
        try:
            self.speed = new_data['entity'][number]['vehicle']['position']['speed']
        except:
            self.speed = 0
    def emphasize_bus(self,fig,ax):
        ax.scatter(i.lon,i.lat,c='black',marker='*',s=170)
    def draw_my_route(self,fig,ax):
        plot_route(fig,ax,self.route_id)

def update_buses(demo=False):
    #Import data
    if demo==True:
        f = open('Transit_data.json')
        data = json.load(f)
    else:
        url = "https://s3.amazonaws.com/cttransit-realtime-prod/vehiclepositions_pb.json"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())

    buses = []
    for i in range(0,np.shape(data['entity'])[0]):
        new_bus = bus(data,i)
        buses.append(new_bus)
    return buses
        
def draw_bus_locations(fig,ax,buses):
    for i in buses:
        ax.scatter(i.lon,i.lat,c='red')
    #From Imad: updating plots:
    #     lons array
    #     lats array
    #line = ax.plot(x,y) -> use plot not scatter
    #line.set_data(x,y) -> when updating the map
    #fig.canvas.draw() ->underneath set data

class Index:
    def refresh(self,event):
        buses = update_buses()
        draw_bus_locations(fig,ax,buses)

def find_bus_from_route(buses, route_id):
    trip_ids = []
    for i in buses:
        if i.route_id == route_id:
            trip_ids.append(i.trip_id)
        else:
            0
    return trip_ids
        
def draw_route(fig,ax,route_id):
    route_shape = trips.loc[trips['route_id']==route_id]['shape_id'].unique()
    for i in route_shape:
        condition = (shapes['shape_id']==i)
        ax.plot(shapes[condition]['shape_pt_lon'],shapes[condition]['shape_pt_lat'],c='green')

def emphasize_buses(fig,ax,trip_ids,buses):
    new_buses = []
    for i in trip_ids:
        for j in buses:
            if j.trip_id==i:
                new_buses.append(j)
    for i in new_buses:
        ax.scatter(i.lon,i.lat,c='black',marker='*',s=170)

def plot_route_and_buses_from_id(fig,ax,route_id,buses):
    draw_route(fig,ax,route_id)
    trip_ids = find_bus_from_route(buses,route_id)
    emphasize_buses(fig,ax,trip_ids,buses)
    
#stop_times = pd.read_csv('stop_times.txt')

def given_bus_next_stop(stop_times,stops,bus,demo):
    if demo==True:
        t = '18:57:33'
    else:
        t = time.localtime()
    
    trip_id = int(bus.trip_id)
    nums = stop_times.loc[stop_times['trip_id']==trip_id]     
    if demo==True:
        next_stops = nums[(nums['arrival_time']>t)]
    else:
        next_stops = nums[(nums['arrival_time']>time.asctime(t)[11:19])]
    next_stops_ids = next_stops['stop_id']
    next_stops_ids_arrays = []
    for i in next_stops_ids:
        next_stops_ids_arrays.append(i)
    stop_id = next_stops_ids_arrays[0]
    stop_name = from_stop_id_give_stop_name(stop_id)
#     try:
#         stop_id = next_stops.head(1)['stop_id']
#         stop_name = stops.loc[stops['stop_id']==str(int(stop_id))]['stop_name']
#     except: 
#         stop_name = 'Unavailable'
#     print('Next stop is: ' + stop_name)
#     plt.text(.81,.5,'Next stop is: %s'  % (stop_name) )
    return stop_name

def func(expr,buses,stop_times,stops,demo):
    bus = buses[int(expr)]
    my_string = str(given_bus_next_stop(stop_times,stops,bus,demo))
    return my_string.split("Name:")[0]
    
def bus_speed_image(busid, buses, fig, ax):
    bearing = buses[busid].bearing
    img = Image.open("bus.JPG")
    img = img.rotate(bearing)
    imgplot = plt.imshow(img)
    #How to make a new pop up window?
    speed = round(buses[busid].speed,2)
    direction = determine_direction(bearing)
    return fig,ax,direction,speed
  #  plt.text(.05,.8,'The bus is going in the direction %s at %f mph' % (direction, speed) )

def determine_direction(bearing):
    if bearing>0 and bearing<22.5:
        return 'W'
    elif bearing<(67.5):
        return 'SW'
    elif bearing<112.5:
        return 'S'
    elif bearing<157.5:
        return 'SE'
    elif bearing<202.5:
        return 'E'
    elif bearing<247.5:
        return 'NE'
    elif bearing<292.5:
        return 'N'
    elif bearing<337.5:
        return 'NW'
    else:
        return 'W'
    
def next_stop_in_shape(bus): #In the shape
    route_id = bus.route_id
    lat = bus.lat
    lon = bus.lon
    route_shape = trips.loc[trips['route_id']==route_id]['shape_id'].unique()
    for i in route_shape:
        condition = (shapes['shape_id']==i)
        first_lat = shapes[condition]['shape_pt_lat'].iloc[0]
        last_lat = shapes[condition]['shape_pt_lat'].iloc[-1]
        first_lon = shapes[condition]['shape_pt_lon'].iloc[0]
        last_lon = shapes[condition]['shape_pt_lat'].iloc[-1]
        for j in shapes[condition]['shape_pt_lon']:
            for k in shapes[condition]['shape_pt_lat']:
                if first_lat<last_lat:
                    if first_lon<last_lon:
                        if k<lat and j<lon:
                            next_step_lon = j
                            next_step_lat = k
                            return next_step_lon,next_step_lat
                    else:
                        if k<lat and j>lon:
                            next_step_lon = j
                            next_step_lat = k
                            return next_step_lon,next_step_lat
                else:
                    if first_lon<last_lon:
                        if k>lat and j<lon:
                            next_step_lon = j
                            next_step_lat = k
                            return next_step_lon,next_step_lat
                    else:
                        if k>lat and j>lon:
                            next_step_lon = j
                            next_step_lat = k
                            return next_step_lon,next_step_lat

def distance(lat1,lon1,lat2,lon2):
    return np.sqrt((lat1-lat2)**2 + (lon1-lon2)**2)

#Function under construction
def stops_within_5_minutes(bus):
    trip_id = bus.trip_id
    minutes = datetime.timedelta(minutes=5)
    t = datetime.datetime.today()
    before = t-minutes
    after = t+minutes
    nums = stop_times.loc[stop_times['trip_id']==int(trip_id)]
    next_stops = nums[(nums['arrival_time']<str(after)[11:19])& (nums['arrival_time']>str(before)[11:19])]
    return next_stops['stop_id']

def closest_stop(bus,stops,stop_times):
    lat = bus.lat
    lon = bus.lon
    trip_id = bus.trip_id
    print(trip_id)
    trip_id = int(trip_id)
    stops_available = stop_times.loc[stop_times['trip_id']==trip_id]['stop_id']
    nearby_stops = stops_within_5_minutes(bus)
    stops_available = stops_available.loc[stops_available.isin(nearby_stops)]
    #Next part: only make possibilities stops within ~20 minutes of schedule
    stops_available = [str(i) for i in stops_available]
    stop_lats = stops.loc[stops['stop_id'].isin(stops_available)]['stop_lat']
    stop_lons = stops.loc[stops['stop_id'].isin(stops_available)]['stop_lon']
    stop_names = stops.loc[stops['stop_id'].isin(stops_available)]['stop_name']
    stop_ids = stops.loc[stops['stop_id'].isin(stops_available)]['stop_id']
    min_dist = 10000000
    name = ''
    stop_id = ''
    for i,j,k,l in zip(stop_lats,stop_lons,stop_names,stop_ids):
        d=distance(i,j,lat,lon)
        if (d)<min_dist:
            min_dist = d
            name = k
            stop_id = l
    print(min_dist)
    return min_dist, name, stop_id
    
def return_next_stop_given_stop(stop_id,trip_id,stop_times):
    stop = stop_times.loc[(stop_times['stop_id']==stop_id) & (stop_times['trip_id']==trip_id)]
    stop_sequence = stop['stop_sequence']
    for i in stop_sequence:
        stop_sequence_present = int(i)
    stop_sequence_next = stop_sequence_present+1
    next_stop = stop_times.loc[(stop_times['stop_sequence']==str(stop_sequence_next)) & (stop_times['trip_id']==trip_id)]
    for i in next_stop['stop_id']:
        next_stop_id = i
    return next_stop_id

def from_stop_id_give_stop_name(stop_id):
    stop = stops.loc[(stops['stop_id']==str(stop_id))]
    stop_name = stop['stop_name']
    for i in stop_name:
        real_stop_name = i
    return real_stop_name

def which_stop_is_next(buses,bus_id,stops,stop_times,demo):
    bus = buses[bus_id]
    trip_id = bus.trip_id
    min_dist1,name1,stop_id1 = closest_stop(bus,stops,stop_times)
    time.sleep(3)
    buses = update_buses(demo)
    bus = buses[bus_id]
    min_dist2,name2,stop_id2 = closest_stop(bus,stops,stop_times)
    if name1==name2:
        if min_dist1<min_dist2:
            final_name = from_stop_id_give_stop_name(return_next_stop_given_stop(stop_id1,trip_id,stop_times))
        else:
            final_name = name1
    else:
        final_name = name2
    return final_name

def how_late_is_the_bus(buses,bus_id,current_stop):
    bus = buses[bus_id]
    actual_stop = current_stop
    supposed_stop = func(bus_id,buses)
    trip_id = int(bus.trip_id)

def closest_neighborhood(bus):
    east_rock = [[41.321,-72.907],'East Rock']
    fair_haven = [[41.311,-72.896],'Fair Haven']
    westville = [[41.331,-72.972],'Westville']
    east_shore = [[41.270, -72.8959],'East Shore']
    downtown = [[41.3087, -72.9254], 'Downtown']
    wooster_square = [[41.3069, -72.9136],'Wooster Square']
    the_hill = [[41.2958,-72.9372],'The Hill']
    dwight = [[41.3119, -72.9387],'Dwight']
    newhallville = [[41.3291, -72.9313],'Newhallvillle']
    dixwell = [[41.3193, -72.9313],'Dixwell']
    west_rock = [[41.3384, -72.9608],'West Rock']
    beaver_hills = [[41.3254,-72.9475],'Beaver Hills']
    prospect_hill = [[41.3263,-72.9210],'Prospect Hill']
    west_river = [[41.3064,-72.9505],'West River']
    edgewood = [[41.3161, -72.9505],'Edgewood']
    neighborhoods = [east_rock,fair_haven,westville,east_shore,downtown,wooster_square,the_hill,dwight,newhallville,dixwell,west_rock,beaver_hills,prospect_hill,west_river,edgewood]
    distance_max = 100000
    closest = ''
    for i in neighborhoods:
        dist = distance(i[0][0],i[0][1],bus.lat,bus.lon)
        if dist<distance_max:
            closest = i[1]
            distance_max = dist
    return closest

def closest_town(bus):
    new_haven = [[41.3083, -72.9279],'New Haven']
    waterbury = [[41.5582, -73.0515],'Waterbury']
    hartford = [[41.7658, -72.6734],'Hartford']
    wallingford = [[41.4570, -72.8231],'Wallingford']
    stamford = [[41.0534, -73.5387],'Stamford']
    new_britain = [[41.6612, -72.7795],'New Britain']
    meriden = [[41.5382, -72.8070],'Meriden']
    towns = [new_haven,waterbury,hartford,wallingford,stamford,new_britain,meriden]
    distance_max = 100000
    closest = ''
    for i in towns:
        dist = distance(i[0][0],i[0][1],bus.lat,bus.lon)
        if dist<distance_max:
            closest = i[1]
            distance_max = dist
    return closest


def make_schedule_into_dataframe(relevant_stops,stops):
    arrival_times = []
    departure_times = []
    stop_ids = relevant_stops['stop_id']

    for i in relevant_stops['arrival_time']:
        arrival_times.append(i)
    for i in relevant_stops['departure_time']:
        departure_times.append(i)
    stop_names = np.empty(np.shape(arrival_times),dtype = "object")
    counter=0
    for i in stop_ids:
        name = stops.loc[(stops['stop_id']==str(i))]['stop_name']
        for j in name:
            stop_names[counter] = j
        counter = counter+1
    
    data = pd.DataFrame()
    data['Stop Name'] = stop_names
    data['Arrival Time'] = arrival_times
    data['Departure Time'] = departure_times
    return data
    
    
def make_buses_into_dataframe(buses):
    data = pd.DataFrame()
    lats = []
    lons = []
    trip_ids = []
    neighborhoods = []
    towns = []
    downtown = []
    for i in buses:
        lats.append(i.lat)
        lons.append(i.lon)
        trip_ids.append(i.trip_id)
        town = closest_town(i)
        if town=='New Haven':
            neighborhood = closest_neighborhood(i)
            neighborhoods.append(neighborhood)
            i.neighborhood = closest_neighborhood(i)
            if i.lat>41.26 and i.lat<41.335 and i.lon<-72.88 and i.lon>-72.98:
                downtown.append('Yes')
            else:
                downtown.append('No')
        else:
            neighborhoods.append('')
            downtown.append('No')
        i.town = town
        towns.append(town)
        
    trip_names = [str(trips[trips['trip_id']==int(i)]['trip_headsign']).split("Name:")[0].split(' ',1)[1] for i in trip_ids]
            
      
    data['Neighborhood'] = neighborhoods
    data['Town'] = towns
    data['latitude'] = lats
    data['longitude'] = lons
    data['trip_id'] = trip_ids
    data['trip_names'] = trip_names
    data['Downtown?'] = downtown
    return data[data['Town']=='New Haven']

def make_bus_into_dataframe(buses,bus_id):
    bus_id = int(bus_id)
    data = pd.DataFrame()
    lats = []
    lons = []
    trip_ids = []
    neighborhoods = []
    towns = []
    bus = buses[bus_id]
    lats.append(bus.lat)
    lons.append(bus.lon)
    trip_ids.append(bus.trip_id)
    town = closest_town(bus)
    if town=='New Haven':
        neighborhood = closest_neighborhood(bus)
        neighborhoods.append(neighborhood)
        bus.neighborhood = closest_neighborhood(bus)
    else:
        neighborhoods.append('')
    bus.town = town
    towns.append(town)
        
    trip_names = [str(trips[trips['trip_id']==int(i)]['trip_headsign']) for i in trip_ids]
    data['Neighborhood'] = neighborhoods
    data['Town'] = towns
    data['latitude'] = lats
    data['longitude'] = lons
    data['trip_id'] = trip_ids
    data['trip_names'] = trip_names
    return data[data['Town']=='New Haven']




callback = Index()
axrefresh = plt.axes([0.81, 0.05, 0.1, 0.075])
brefresh = Button(axrefresh, 'Refresh')
brefresh.on_clicked(callback.refresh)

draw_map(fig,ax)
buses = update_buses()

axtextbox = plt.axes([0.90, 0.8, 0.1, 0.075])
btextbox = TextBox(axtextbox, 'Get next stop from bus number: ')
btextbox.on_submit(func)
        
draw_bus_locations(fig,ax,buses)

