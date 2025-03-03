import sys
import gzip
import pandas as pd
import numpy as np

'''Note: make sure the zipped medadata file for the desired product
category is in your current working directory.

Instructions: to see the top 50 list, run the following:

	python3 real_top_50.py <name_of_subset.json.gz> <name_of_result.txt>
	
 '''

'''Following two functions used to create metadata dict from 
compressed metadata file'''

def parse(path): 
	g = gzip.open(path, 'rb') 
	for l in g: 
		yield eval(l) 

def getDF(path): 
	i = 0 
	df = {} 
	for d in parse(path): 
		try:
			df[d['asin']] = d['title'] 
		except:
			df[d['asin']] = "No Title"
		i += 1 
	return df

def find_real_50(path):
	'''
	Returns pandas df of top 50 product pairs in descending order
	of score
	Input: (str) file name 
	Output: (pd.DataFrame) a dataframe 
	'''
	file = open(path, "r")
	score_list = []
	label_list = []
	for line in file:
	    list_split = line[4:-3]
	    list_split = list_split.split("], ")
	    new_list = []
	    for thing in list_split:
	        new_item = thing[1:].split(", ")
	        score_list.append(float(new_item[0]))
	        label_list.append(new_item[1][1:-1])

	df = pd.DataFrame({'score': score_list, 'label': label_list})
	df = df.sort_values(by='score', ascending=False).reset_index(drop=True)
	df = df.drop_duplicates()
	return(df.head(50))

def result_names(meta, top_50):
	'''
	Prints score, product pair, their timeshift, and mean, variance
	of time shifts in top 50 results.
	Input: (dict) metadata 
	Output: None
	'''
	shift_list = []
	for n, row in top_50.iterrows():
		split, score = row[0].split(" "), row[1]
		prod1, prod2, shift = split[0], split[1], split[2]
		shift_list.append(abs(int(shift)))
		title1 = meta[prod1]
		title2 = meta[prod2]
		print(score, " ", title1, " + ", title2 + " ", shift)
		print("\n")
	print("mean time shift was:", np.mean(shift_list))
	print("variance of time shift was:", np.var(shift_list))

if __name__ == '__main__':
	df = getDF(sys.argv[1])
	fifty = find_real_50(sys.argv[2])
	result_names(df, fifty)
	

