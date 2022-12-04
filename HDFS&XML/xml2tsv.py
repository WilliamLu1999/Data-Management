# William Lu
# 7424831487
# This python script, which deals with XML and fsimages, is the homework 2 of Data Management. 
import pandas as pd
import numpy as np
from lxml import etree
import datetime
from datetime import timezone
import sys
from helper import printf
import csv


image_xml = sys.argv[1] # take the input
image_tsv = sys.argv[2]

tree = etree.parse(open(image_xml))
root = tree.getroot()

# creating list to store each column
path_list=[]
modification_time_list=[]
block_count_list=[]
permission_node_list =[]
file_size_list=[]

permission =['---','--x','-w-','-wx','r--','r-x','rw-','rwx'] # to store the permissions
# reference: https://www.multacom.com/faq/password_protection/file_permissions.htm
for inode in tree.xpath('/fsimage/INodeSection/inode'):
	# getting modification time list
	mod_time = inode.xpath('mtime/text()')
	mod_time = datetime.datetime.fromtimestamp(int(mod_time[0])/1000,timezone.utc)
	mod_time = mod_time.strftime('%-m/%-d/%Y %-H:%M') # convert time to string
	# reference: https://www.programiz.com/python-programming/datetime/strftime
	modification_time_list.append(mod_time)
	# getting the blocks count list
	# need to check type node because only type node FILE has block
	type_node =inode.xpath('type/text()')
	if type_node[0] =='FILE':
		block_count=1
	else:
		block_count=0
	block_count_list.append(block_count)

	# getting the file size list
	# need to check type node because only type node FILE has file size
	if type_node[0] =='FILE':
		byte_count=inode.xpath('blocks/block')
		file_size =0
		for byte in byte_count:
			file_size= file_size + int(byte.xpath('numBytes/text()')[0])
			file_size_list.append(file_size)
	else:
		file_size_list.append(0) # we need to append zeros since DIRECTORY have file size 0. Got to match.

	# getting the permission list
	permission_node =inode.xpath('permission/text()')[0][-3:] #getting the last three digit
	for a in permission_node:
		permission_node +=''.join(permission[int(a)])
	if type_node[0] =='DIRECTORY':
		permission_node = 'd'+permission_node[3:]
		permission_node_list.append(permission_node) # getting the right permission
	else:
		permission_node = '-'+permission_node[3:] # getting the right permission
		permission_node_list.append(permission_node)

	path = inode.xpath('name/text()')
	# this does not give us / and only the subdirectory name not the whole path
	path_list.append(path)


dict_path_keys=tree.xpath('/fsimage/INodeSection/inode/id/text()')
#print(dict_path_keys)
# make sure the Path column is correct
path_list=np.concatenate(path_list)
path_list=np.insert(path_list,0,'')

# creating a dictionary for path
dict_path=dict(zip(dict_path_keys,path_list))

#print(dict_path)
final_path_list=dict(dict_path) # store the root directory first
#for key in dict_path.key():



# Create a dictionary for parent and child in the INodeDirectory section
parent_child={}
for i in tree.iter("directory"):
	parent = i.find("parent").text
	child = [x.text for x in i.findall('child')]
	parent_child[parent]=child

# adding name to the dictionary	
# check if the key in dict path is in the parent child values, if it is, then we know
# that the value for dict path can keep adding the path
for key in dict_path.keys():
	for a,b in parent_child.items():
		if key in b:
			final_path_list[key]=final_path_list[a]+'/'+final_path_list[key]

#print(final_path_list)
#print(parent_child)
#print(final_path_list.values())
stored_path_list = list(final_path_list.values())
# make sure the root is having '/'
stored_path_list[0]='/'
#print(stored_path_list)
lists = [stored_path_list, modification_time_list, block_count_list, file_size_list,permission_node_list]
df = pd.concat([pd.Series(x) for x in lists], axis=1)
df.columns=['Path','ModificationTime','BlocksCount','FileSize','Permission']
df.to_csv(str(image_tsv),index=False)
# write to the tsv file in the command line arguments
with open(str(image_tsv), 'w') as f:
	sys.stdout = f
	df.to_csv(str(image_tsv),index=False,sep='\t')

    
