import requests
import json
import sys
import pandas as pd

#output_path = '/Users/William/Downloads/ouput.json'
# reference: https://gist.github.com/noize-e/ff0345dde2e3bdf4449ba798720bbf67

# https://stackoverflow.com/questions/14419925/storing-lambdas-in-a-dictionary

input_name = sys.argv[1] # this is input.json
output_name = sys.argv[2] # this is output.json

    
dynamoDB = json.loads(open(input_name, 'r').read())
'''
#print(dynamoDB['bookid'].keys())
# create a dictionary to store data types and convert them using the right function
dynamo_data_types = {
	#"S": lambda d: str(d), # string
	#"N": lambda d: int(d), # numbers
	#"SS": lambda d: convert_data_types(d), # string set
	#"NS": lambda d: convert_data_types(d), # number set
	"L": lambda d: convert_data_types(d), # list
	"M": lambda d: convert_data_types(d) # map
}
def convert_data_types_list(dynamo):
	# this consider list form
	if type(dynamo) is list:
		dlist =[]
		for i in dynamo:
			dlist.append(convert_data_types_list(i))
		dynamo=dlist
		return dynamo
	
def convert_data_types(dynamo):
	dynamo_type = type(dynamo)

	if type(dynamo) == dict: # this is for map 
		keys = dynamo.keys()
		for key in keys:
			if key=='L' or key=='S'or key=='N'or key=='SS'or key=='M'or key=='L':
				dynamo = dynamo_data_types[key](dynamo[key])
				break
			else:
				dynamo[key] = convert_data_types(dynamo[key])
		return dynamo

	if dynamo_type == list: # this is for SS, NS, L list
		dynamolist = []
		for index in dynamo:
			dynamolist.append(convert_data_types(index)) # parse into every item of the list
		dynamo = dynamolist
		return dynamo
	else: 
		return dynamo
'''
dynamo_data_types2={}
final={}
dy_keys =dynamoDB.keys()
for k in dy_keys:
	for j in dynamoDB[k].keys():
		if j=='S':
			dynamoDB[k][j]=str(dynamoDB[k][j])
			#dynamo_data_types2['S']=dynamoDB[k][j]
			final[k]=dynamoDB[k][j]
		if j=='N':
			dynamoDB[k][j]=int(dynamoDB[k][j])
			final[k]=dynamoDB[k][j]
		if j=='SS':
			#dynamoDB[k][j]=convert_data_types(dynamoDB[k][j])
			final[k]=dynamoDB[k][j]
		if j=='NS':
			#dynamoDB[k][j]=convert_data_types(dynamoDB[k][j])
			final[k]=dynamoDB[k][j]
		if j =='L':
			temp=[]
			for i in dynamoDB[k][j]:
				for n in i.keys():
					if n=='S':
						temp.append(str(i[n]))
					if n=='N':
						temp.append(int(i[n]))
			final[k]=temp
		if j =='M':
			#print(dynamoDB[k][j])
			
			temp2={}
			for i in dynamoDB[k][j].keys():
				for q in dynamoDB[k][j][i].keys():
					if q=='S':
						temp2[i]=str(dynamoDB[k][j][i][q])
					if q=='N':
						temp2[i]=int(dynamoDB[k][j][i][q])
				#for n in i.values():
					#print(n)
					#if n=='S':
						#temp2[i]=str(i[n])
					#if n=='N':
						#temp2[i]=int(i[n])
			final[k]=temp2
			
#print(final)

# write to the tsv file in the command line arguments
with open(str(output_name), 'w') as f:
	sys.stdout = f
	f.write(json.dumps(final))
	f.close()
#print('success')