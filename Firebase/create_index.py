# Q3: create index for cars and add cars under them
# Author: William Lu
# email: wlu98761@usc.edu
import json
import requests
import sys
import pandas as pd
import re

with open(sys.argv[1]) as filename:
    df =pd.read_csv(filename)
    # create a list to store unique keys
    keys=[]
    temp =df['CarName'].tolist()
    
    for item in temp:
        # replace the parenthesis and hyphen in each string
        key_temp = re.sub("[()]|[-]+"," ", item)
        
        keys.append(key_temp)
    #print(keys)    
    # strip each item and add each small part to the list as individual word
    car_keys=[]
    for key in keys:
        res = key.split()
        #print(res)
        car_keys.append(res)

    # need to faltten out the list of lists
    flat_car_keys=[i for sublist in car_keys for i in sublist]
    #print(car_keys)
    #need to get the key to be unique for json later
    unique_flat_car_keys = []
    for x in flat_car_keys:
        if x not in unique_flat_car_keys:
            unique_flat_car_keys.append(x)
    #print(df.index)
    #print(unique_flat_car_keys)
    # create a temp_dict_car where each car name will be in a list with ID being the key.
    temp2 =df['car_ID'].tolist()
    temp_dict_car= dict(zip(temp2,car_keys))

    
    # Create a dict for json later
    dict_car ={}
    for i in unique_flat_car_keys:
        dict_car[i] = None # temperory value for the dictionary as we have not clear up the car names
    #print(dict_car)
    for key in dict_car:
        id=[] # we need to store id list for each car key 
        for i in temp_dict_car: 
            # check if the keyword is in the name of the car
            if key in temp_dict_car[i]:
                # Since Object of type int64 is not JSON serializable,
                # we need to convert each car_ID as integer
                # i is the list of every car name
                id.append(i)
        
        dict_car[key]=id
    
            #print(df['car_ID'][i], df['CarName'][i])    
        #jsonlist = json.loads(df.to_json(orient='records'))
    
# we can pass in our dictionary to json directly
requests.put(url='https://homework-1-6d336-default-rtdb.firebaseio.com/keyword_index.json',json=dict_car)
print('hi')
