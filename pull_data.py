import urllib, json
import numpy as np

url = "https://s3.amazonaws.com/cttransit-realtime-prod/vehiclepositions_pb.json"
response = urllib.request.urlopen(url)
data = json.loads(response.read())

af = asdf.AsdfFile(data)

# Write the data to a new file
af.write_to('~/Downloads/example.asdf')