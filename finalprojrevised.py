#Code Review 1(ish)
#How to use streamlit????? That could be great- currently not working spatially
#How to make the buses disappear each time we update
#Is this project enough???
#Talk through the algorithm I'm working on (which isn't fully working yet)

import urllib, json
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
import pandas as pd
import time 
from PIL import Image

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

def update_buses():
    #Import data
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
    #fig.canvas.draw()

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
    
def given_bus_next_stop(stop_times,stops,bus):
    t = time.localtime()
    trip_id = bus.trip_id
    nums = stop_times.loc[stop_times['trip_id']==int(trip_id)]
    next_stops = nums[(nums['arrival_time']>time.asctime(t)[11:19])]
    stop_id = next_stops.head(1)['stop_id']
    stop_name = stops.loc[stops['stop_id']==str(int(stop_id))]['stop_name']
    print('Next stop is: ' + stop_name)
    plt.text(.81,.5,'Next stop is: %s'  % (stop_name) )
    t = time.localtime()

def func(expr):
    bus = buses[int(expr)]
    given_bus_next_stop(stop_times,stops,bus)
    
def bus_speed_image(busid, buses, fig, ax):
    bearing = buses[busid].bearing
    img = Image.open("bus.JPG")
    img = img.rotate(bearing)
    ax = fig.add_subplot(1, 2, 1)
    imgplot = plt.imshow(img)
    #How to make a new pop up window?
    speed = round(buses[busid].speed,2)
    direction = determine_direction(bearing)
    plt.text(.1,.8,'The bus is going in the direction %s at %f mph' % (direction, speed) )

def determine_direction(bearing):
    if bearing>0 and bearing<22.5:
        return 'N'
    elif bearing<(67.5):
        return 'NE'
    elif bearing<112.5:
        return 'E'
    elif bearing<157.5:
        return 'SE'
    elif bearing<202.5:
        return 'S'
    elif bearing<247.5:
        return 'SW'
    elif bearing<292.5:
        return 'W'
    elif bearing<337.5:
        return 'NW'
    else:
        return 'N'
    
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

def closest_stop(bus):
    lat = bus.lat
    lon = bus.lon
    trip_id = bus.trip_id
    trip_id = int(trip_id)
    stops_available = stop_times.loc[stop_times['trip_id']==trip_id]['stop_id']
   
    #Next part: only make possibilities stops within ~20 minutes of schedule
    
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
    return min_dist, name, stop_id
    
def return_next_stop_given_stop(stop_id,trip_id):
    stop = df.loc[(stop_times['stop_id']==stop_id) & (stop_times['trip_id']==trip_id)]
    stop_sequence = int(stop_times['stop_sequence'])
    stop_sequence = stop_sequence+1
    next_stop = df.loc[(stop_times['stop_sequence']==str(stop_sequence)) & (stop_times['trip_id']==trip_id)]
    return next_stop['stop_id']

def from_stop_id_give_stop_name(stop_id):
    stop = df.loc[(stops['stop_id']==stop_id)]
    return stop['stop_name']

def which_stop_is_next(bus):
    trip_id = bus.trip_id
    min_dist1,name1,stop_id1 = closest_stop(bus)
    time.sleep(3)
    update_buses()
    min_dist2,name2,stop_id2 = closest_stop(bus)
    if name1==name2:
        if min_dist1<min_dist2:
            return from_stop_id_give_stop_name(return_next_stop_given_stop(stop_id1,trip_id))
        else:
            return name1
    else:
        return name2
    

callback = Index()
axrefresh = plt.axes([0.81, 0.05, 0.1, 0.075])
brefresh = Button(axrefresh, 'Refresh')
brefresh.on_clicked(callback.refresh)

draw_map(fig,ax)
buses = update_buses()

axtextbox = plt.axes([0.81, 0.8, 0.1, 0.075])
btextbox = TextBox(axtextbox, 'Get next stop from bus number: ')
btextbox.on_submit(func)
        
draw_bus_locations(fig,ax,buses)

print(which_stop_is_next(buses[5]))
print('hi')

#Demonstration of plotting bus and route from ID
#plot_route_and_buses_from_id(fig,ax,'12421',buses)

#Demonstration of Giving Next Stop of Bus
#given_bus_next_stop(stop_times,stops,buses[1])

bus_speed_image(5,buses,fig,ax)

plt.show()

#Help: how to tell if a bus has gotten to a location or not yet?



    #Neighborhood lines
#     url2 = 'https://gist.githubusercontent.com/camille-s/c8cfa583ef22105e90d53ceb299f1a7b/raw/fc087f30ddb2658a05fb5408f1e9d5276b8a433d/nhv.json'
#     response2 = urllib.request.urlopen(url2)
#     data2 = json.loads(response2.read())

#     names = ['edgewood_locs', 'locs2', 'locs3', 'locs4', 'locs5', 'locs6', 'locs7', 'locs8', 'locs9', 'locs10', 'locs11', 'locs12', 'locs13', 'locs14', 'locs15', 'locs16', 'locs17', 'locs18', 'locs19', 'locs20']
#     for i in range(0,20):
#         locals()[names[i]] = np.ones([2,np.shape(data2['features'][i]['geometry']['coordinates'][0])[0]])
#  #       exec("%s=%d" % (names[i], np.ones([2,np.shape(data2['features'][i]['geometry']['coordinates'][0])[0]])))
#     for i in names:
#         ax.plot(i[0],i[1])