# Q4: search car by user inputs but return IDs
# Author: William Lu
# email: wlu98761@usc.edu
import json
import requests
import sys
import pandas as pd
import re
import operator

temp_input = sys.argv[1]
# we need to make sure the user input don't have any weird chracters
user_input = re.sub("[()]|[-]+|[,]+|[.]+|[[]+|[]]+"," ", temp_input)
user_input_list=user_input.split()

# store how many times the value (IDs) appeared in each keyword of user_input_list
counter={}


r = requests.get(url='https://homework-1-6d336-default-rtdb.firebaseio.com/keyword_index.json/')
data =r.json()
j = list(data.keys())
#print(j)
#wanted_keys = user_input_list# The keys you want
#print(user_input_list)
#print(data) 
new_dict = dict((k, data[k]) for k in user_input_list if k in data.keys())
#print(new_dict)
# have a reference here: https://stackoverflow.com/questions/5352546/extract-subset-of-key-value-pairs-from-dictionary
# now we have the mini dictionary, we just need to count each IDs across the dictionary and report them
for keyword in new_dict:
    for id in new_dict[keyword]:
        if id not in counter:
            counter[id]=1
        else:
            counter[id]+=1

# now we just need to print out IDs based on descending occurances
#print(counter)
# need to reverse the counter first so that the output will show keys that are greater, otherwise, it will only be sorted in descending based on values
# we want to show IDs in descending order of both keys and values
reverse_counter = dict(reversed(list(counter.items())))
#print(reverse_counter)
# reference: https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-1.php
sorted_counter = dict( sorted(reverse_counter.items(), key=operator.itemgetter(1),reverse=True))
print("IDs of the cars are:\n",list(sorted_counter.keys())) # convert it to list so that no "dict_keys" will be in the print statement
