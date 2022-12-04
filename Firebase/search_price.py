# Q2: takes two numbers as range to filter out information. i.e get the cars that fall into the price range
# Author: William Lu
# email: wlu98761@usc.edu

import json
import pandas as pd
import requests
import sys


# First: specify the range using command line arguments
range_num_1 = sys.argv[1]
range_num_2= sys.argv[2]

r = requests.get(url='https://homework-1-6d336-default-rtdb.firebaseio.com/cars.json?orderBy="price"&startAt='+range_num_1+'&endAt='+range_num_2)
d =r.json()
id=[]
if len(d)==0:
    print("No cars found with the given range")
else:
    for i,j in d.items():
        id.append(j['car_ID'])
    print("ID for the car price range are:\n",sorted(id))