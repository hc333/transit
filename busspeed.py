import urllib, json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from matplotlib.widgets import Button


url = "https://s3.amazonaws.com/cttransit-realtime-prod/vehiclepositions_pb.json"
response = urllib.request.urlopen(url)
data = json.loads(response.read())


#speeds = np.ones([1,np.shape(data['entity'])[0]])
speeds = np.ones([1,4])


#for i in range(np.shape(data['entity'])[0]):
for i in range(0,4):
    try:
        speeds[0][i] = data['entity'][i]['vehicle']['position']['speed']
    except:
        speeds[0][i] = 0
        
fig, axs = fig, axs = plt.subplots(2, 2, figsize=(6, 6))

img = Image.open("bus.JPG")
 

counter=0
for i in range(0,2):
    for j in range(0,2):
        width, height = img.size
        #im = im.rotate(180) - going to add direction
        newsize = (int(width*5*speeds[0][counter])+1,int(height*5*speeds[0][counter])+1)
        img1 = img.resize(newsize)
        axs[i, j].imshow(img1)
        axs[i, j].imshow(img1)
        axs[i, j].imshow(img1)
        axs[i, j].imshow(img1)
        counter = counter+1


button1 = plt.axes([0.8, .9, 0.1, 0.075])
buttons1 = Button(button1, str(speeds[0][0]))
button2 = plt.axes([0.35, .9, 0.1, 0.075])
buttons2 = Button(button2, str(speeds[0][1]))
button3 = plt.axes([0.8, 0.01, 0.1, 0.075])
buttons3 = Button(button3, str(speeds[0][2]))
button4 = plt.axes([0.35, 0.01, 0.1, 0.075])
buttons4 = Button(button4, str(speeds[0][3]))

names = [button1, button2, button3, button4]
names1 = [buttons1, buttons2, buttons3, buttons4]
heights = [.9, .9, .01, .01]
xs = [.15, .15, .6, .6]

for i in range(0,4):
    if speeds[0][i]==0:
        names[i] = plt.axes([xs[i], heights[i], 0.1, 0.075])
        names1[i] = Button(names[i], 'No speed currently')


     

plt.show()
