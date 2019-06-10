#Code for running regressions and selecting a explaination score from two


def get_score(x, y):
    '''
    Gets the covariance between x and y, starting from the later of the first 
        nonzero entries of x or y 

    Inputs:
        x: a list of floats
        y: a list of floats.  x and y must have the same length

    Output:
        The score of x and y (float)
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
    


def find_best_fit(x, y):
    '''
    Runs through all possible ways to align x and y that for which both x and 
        y have nonzero entries and chooses the alighment with the highest score

    Inputs:
        x: a list of floats
        y: a list of floats.  x and y must have the same length

    Output: a tuple containing the best score among all alignments of x and y
        and the number of months by which x and y are offset to obtain this
        highest score
    '''

    orig_len = len(x)
    best_score = 0
    offset = 0

    for i in range(orig_len - 1):
        y_range = orig_len - i
        x_slice = x[i:]
        y_slice = y[:y_range]
        if sum(x_slice) == 0 or sum(y_slice) == 0:
            break
        offset_score = get_score(x_slice, y_slice)
        if offset_score > best_score:
            best_score = offset_score
            offset = i

    for i in range(len(y)-1):
        x_range = len(x) - i
        x_slice = x[:x_range]
        y_slice = y[i:]
        if sum(x_slice) == 0 or sum(y_slice) == 0:
            break
        offset_score = get_score(y_slice, x_slice)
        if offset_score > best_score:
            best_score = offset_score
            offset = -1 * i

    return (best_score, offset)



def do_everything(line1, line2):
    '''
    A wrapper function for find_best_fit that takes in the input the mapper
        gives it and applies find_best_fit to it.

    Inputs:
        line1 (list of strings): a read line of a csv
        line2 (list of strings): a read line of a csv

    Outputs: a tuple that contains a (tuple of product ids (strings) and 
        the offset that gives the best score from find_best_fit (int)) and 
        (the best score from find_best_fit (float))
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
    A function that calculates the covariance of x and y

    Inputs:
        x: a list of floats
        y: a list of floats.  x and y must have the same length
        sumx: the sum of items of x (float)
        sumy: the sum of items of y (float).  Sums are included as inputs to 
        avoid redundant calculations within the find_best_fit functions.
    
    Output:
        The covariance of x and y (float)
    '''
    N = len(x)
    meanx = sumx/N
    meany = sumy/N
    cov = 0

    for i in range(N):
        cov += (x[i]-meanx)*(y[i]-meany)

    cov = cov/(N-1)
    return cov
