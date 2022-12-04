# Q1: load the csv file to firebase
# Author: William Lu
# email: wlu98761@usc.edu
import requests
import json
import sys
import pandas as pd

#output_path = '/Users/William/Downloads/Homework_1/cars.json'
with open(sys.argv[1]) as filename:
    df =pd.read_csv(filename)
    jsonlist = json.loads(df.to_json(orient='records'))
    

requests.put(url='https://homework-1-6d336-default-rtdb.firebaseio.com/cars.json',json=jsonlist)
#print('hi') 

