#Code for running regressions and selecting a explaination score from two

import numpy as np
from sklearn import linear_model

def get_score(x, y):
	'''
	'''

	reg = LinearRegression.fit(x, y)
	
	return reg.score(x,y) * np.log(np.sum(y))



def find_best_fit(x, y):
    '''
    '''

    best_score = 0
    offset = 0
    for i in range(len(x)):
    	y_range = i - len(y)
    	offset_score = get_score(x[i:], y[y_range:])
    	if offset_score > best_score:
    		best_score = offset_score
    		offset = i
    for i in range(len(y)):
    	x_range = i - len(x)
    	offset_score = get_score(y[i:], x[x_range:])
    	if offset_score > best_score:
    		best_score = offset_score
    		offset = -1 * i

	return best_score