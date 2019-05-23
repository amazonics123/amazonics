#Code for running regressions and selecting a explaination score from two

import numpy as np

def get_score(x, y):
    '''
    '''

    return np.corrcoef(x,y)[0][1] * \
        np.log(min(1000, np.sum(y)) * min(1000, np.sum(x)))



def find_best_fit(x, y):
    '''
    '''

    best_score = 0
    offset = 0
    for i in range(len(x)):
        y_range = len(y) - i
        offset_score = get_score(x[i:], y[:y_range])
        if offset_score > best_score:
            best_score = offset_score
            offset = i
    for i in range(len(y)):
        x_range = len(x) - i
        offset_score = get_score(y[i:], x[:x_range])
        if offset_score > best_score:
            best_score = offset_score
            offset = -1 * i

    return (best_score, offset)