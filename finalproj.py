import urllib, json
import matplotlib.pyplot as plt
import numpy as np

url = "https://s3.amazonaws.com/cttransit-realtime-prod/vehiclepositions_pb.json"
response = urllib.request.urlopen(url)
data = json.loads(response.read())

print(np.shape(data['entity'])[0])
locations = np.ones([2,np.shape(data['entity'])[0]])
for i in range(np.shape(data['entity'])[0]):
    locations[0][i] = data['entity'][i]['vehicle']['position']['latitude']
    locations[1][i] = data['entity'][i]['vehicle']['position']['longitude']
import geopandas as gpd
map = gpd.read_file('Trans_RoadSegment.shp')
fig,ax = plt.subplots(figsize=(10,10))
map.plot(ax=ax)

url2 = 'https://gist.githubusercontent.com/camille-s/c8cfa583ef22105e90d53ceb299f1a7b/raw/fc087f30ddb2658a05fb5408f1e9d5276b8a433d/nhv.json'
response2 = urllib.request.urlopen(url2)
data2 = json.loads(response2.read())

edgewood_locs = np.ones([2,np.shape(data2['features'][0]['geometry']['coordinates'][0])[0]])
locs2 = np.ones([2,np.shape(data2['features'][1]['geometry']['coordinates'][0])[0]])
locs3 = np.ones([2,np.shape(data2['features'][2]['geometry']['coordinates'][0])[0]])
locs4 = np.ones([2,np.shape(data2['features'][3]['geometry']['coordinates'][0])[0]])
locs5 = np.ones([2,np.shape(data2['features'][4]['geometry']['coordinates'][0])[0]])
locs6 = np.ones([2,np.shape(data2['features'][5]['geometry']['coordinates'][0])[0]])
locs7 = np.ones([2,np.shape(data2['features'][6]['geometry']['coordinates'][0])[0]])
locs8 = np.ones([2,np.shape(data2['features'][7]['geometry']['coordinates'][0])[0]])
locs9 = np.ones([2,np.shape(data2['features'][8]['geometry']['coordinates'][0])[0]])
locs10 = np.ones([2,np.shape(data2['features'][9]['geometry']['coordinates'][0])[0]])
locs11 = np.ones([2,np.shape(data2['features'][10]['geometry']['coordinates'][0])[0]])
locs12 = np.ones([2,np.shape(data2['features'][11]['geometry']['coordinates'][0])[0]])
locs13 = np.ones([2,np.shape(data2['features'][12]['geometry']['coordinates'][0])[0]])
locs14 = np.ones([2,np.shape(data2['features'][13]['geometry']['coordinates'][0])[0]])
locs15 = np.ones([2,np.shape(data2['features'][14]['geometry']['coordinates'][0])[0]])
locs16 = np.ones([2,np.shape(data2['features'][15]['geometry']['coordinates'][0])[0]])
locs17 = np.ones([2,np.shape(data2['features'][16]['geometry']['coordinates'][0])[0]])
locs18 = np.ones([2,np.shape(data2['features'][17]['geometry']['coordinates'][0])[0]])
locs19 = np.ones([2,np.shape(data2['features'][18]['geometry']['coordinates'][0])[0]])
locs20 = np.ones([2,np.shape(data2['features'][19]['geometry']['coordinates'][0])[0]])
locsx = np.ones([2,1727])

names = [edgewood_locs, locs2, locs3, locs4, locs5, locs6, locs7, locs8, locs9, locs10, locs11, locs12, locs13, locs14, locs15, locs16, locs17, locs18, locs19, locs20]

from matplotlib.widgets import Button

import matplotlib.pyplot as plt
fig,ax = plt.subplots(figsize=(10,10))
map.plot(ax=ax)
for i in names:
    ax.plot(i[0],i[1])

ax.scatter(locations[1],locations[0],c='red')
plt.xlim(-72.98,-72.88)
plt.ylim(41.26,41.355)
import time
class Index:
    def on(self,event):
        url = "https://s3.amazonaws.com/cttransit-realtime-prod/vehiclepositions_pb.json"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        locations = np.ones([2,np.shape(data['entity'])[0]])
        for i in range(np.shape(data['entity'])[0]):
            locations[0][i] = data['entity'][i]['vehicle']['position']['latitude']
            locations[1][i] = data['entity'][i]['vehicle']['position']['longitude']
        ax.scatter(locations[1],locations[0],c='red')


#     def on(self, event):
#         for i in range(0,10):
#             print('hi')
#             url = "https://s3.amazonaws.com/cttransit-realtime-prod/vehiclepositions_pb.json"
#             response = urllib.request.urlopen(url)
#             data = json.loads(response.read())

#             print(np.shape(data['entity'])[0])
#             locations = np.ones([2,np.shape(data['entity'])[0]])
#             for i in range(np.shape(data['entity'])[0]):
#                 locations[0][i] = data['entity'][i]['vehicle']['position']['latitude']
#                 locations[1][i] = data['entity'][i]['vehicle']['position']['longitude']
#             ax.scatter(locations[1],locations[0],c='red')
#             fig.canvas.draw()
#             time.sleep(1)
#     def off(self,event):
#         0
            
 
callback = Index()
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'On')
bnext.on_clicked(callback.on)
plt.show()

# callback = Index()
# axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
# bnext = Button(axnext, 'On')
# bnext.on_clicked(callback.on)

# axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
# bprev = Button(axprev, 'Off')
# bprev.on_clicked(callback.off)
# plt.show()