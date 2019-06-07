#Code for running regressions and selecting a explaination score from two

import numpy as np

def get_score(x, y):
    '''
    '''
    
    orig_len = len(x)
    start = 0
    for i in range(orig_len):
        if x[i] != 0:
            start = i
            break
    for j in range(orig_len):
        if y[j] != 0:
            start = max(j, start)
            break
    working_x = x[start:]
    working_y = y[start:]
    sumx = sum(working_x)
    sumy = sum(working_y)
    return covariance(working_x, working_y, sumx, sumy)
    #return np.corrcoef(working_x, working_y)[0][1] * \
        #np.log(max(1, min(1000, sum(working_x)) * min(1000, sum(working_y))))



def find_best_fit(x, y):
    '''
    '''

    if sum(x) <= 20 or sum(y) <= 20:
        return (0, 0)

    orig_len = len(x)
    best_score = 0
    offset = 0

    for i in range(orig_len - 1):
        y_range = orig_len - i
        x_slice = x[i:]
        y_slice = y[:y_range]
        if sum(x_slice) <= 20 or sum(y_slice) <= 20:
            break
        offset_score = get_score(x_slice, y_slice)
        if offset_score > best_score:
            best_score = offset_score
            offset = i

    for i in range(len(y)-1):
        x_range = len(x) - i
        x_slice = x[:x_range]
        y_slice = y[i:]
        if sum(x_slice) <= 20 or sum(y_slice) <= 20:
            break
        offset_score = get_score(y_slice, x_slice)
        if offset_score == 0:
            break
        if offset_score > best_score:
            best_score = offset_score
            offset = -1 * i

    return (best_score, offset)



def do_everything(line1, line2):
    '''
    '''

    id1 = line1[0]
    id2 = line2[0]
    x = []
    y = []
    for i in range(1, len(line1)):
        x.append(float(line1[i]))
    for i in range(1, len(line2)):
        y.append(float(line2[i]))
    best = find_best_fit(x,y)
    return((id1, id2, best[1]), best[0])





def covariance(x, y, sumx, sumy):
    '''
    '''
    N = len(x)
    meanx = sumx/N
    meany = sumy/N
    cov = 0

    for i in range(N):
        cov += (x[i]-meanx)*(y[i]-meany)

    cov = cov/(N-1)
    return cov
