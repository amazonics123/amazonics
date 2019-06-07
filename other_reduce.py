from mrjob.job import MRJob
import heapq

class toplines(MRJob):
    

    # add to command line --file file2.csv

    

    def mapper_init(self):
        self.lines_run = []
        self.score_tuples = []

    def mapper(self, _, line):

        linemod = line[1:11]+", "+line[14:-1]
        arr = linemod.split(", ")[:-1]

        for lyne in self.lines_run:
            tuple_score = do_everything(arr, lyne)
            pair = str(tuple_score[0][0])+" "+str(tuple_score[0][1])+" "+str(tuple_score[0][2])
            self.score_tuples.append((pair, tuple_score[1]))

        self.lines_run.append(arr)

    def mapper_final(self):
        for pair, score in self.score_tuples:
            yield pair, score

    '''
    def mapper_first(self, _, line1):
        
        #below we have some very janky string comprehension
        
        linemod = line1[1:11]+", "+line1[14:-1]
        #print(line[1:11])
        arr = linemod.split(", ")[:-2]

        yield arr, linemod

    def mapper_second(self, arr, line2):
        linebod = line2[0:10]+", "+line2[14:-1]
        #print(line[0:10])
        arrmatey = linebod.split(", ")[:-1]
        tuple_score = regression.do_everything(arr, arrmatey)
        value = str(tuple_score[0][0])+" "+str(tuple_score[0][1])+" "+str(tuple_score[0][2])
        #print(tuple_score[1])
        a = tuple_score[1]
        yield value, a
    '''
    

    def combiner_init(self):
        '''
        score_store = []
        covars_store = []
        '''
        self.scores = {}

    def combiner(self, covars, scores):
        ''
        pair = covars
        score = list(scores)[0]
        #print(pair)
        #print(score)
        #print("aaa")
        self.scores[covars] = score
        score_list = list(scores)

    def combiner_final(self):
        '''
        
        dataframe = pd.DataFrame(np.array([score_store, covars_store]), columns=['scores', 'covars'])
        yield None, dataframe.sort_values(by=['scores']).head(50)
        '''
        k = 50
        h = []
        h = [(score, covars) for (covars, score) in list(self.scores.items())[:k]]
        heapq.heapify(h)
        q = [(score, covars) for (covars, score) in list(self.scores.items())[k:]]
        for score, covars in q:
            min_score, min_covars = h[0]

            if score > min_score:
                heapq.heapreplace(h, (score, covars))
        
        h.sort(reverse=True)
        #print(h)
        yield None, h

    def reducer_init(self):
        self.list_tops = []

    def reducer(self, _, h):
        self.list_tops = self.list_tops + list(h)[0]

    def reducer_final(self):

        k=50

        h = self.list_tops[:k]
        heapq.heapify(h)

        #print(self.list_tops[0])

        for unit in self.list_tops:
            min_score, min_covars = h[0]

            if unit[0] > min_score:
                heapq.heapreplace(h, unit)
        
        h.sort(reverse=True)
        yield len(h), h



def compare_lexicographic_order(str1, str2):
    '''
    '''

    for i in range(10):
        o1 = ord(str1[i])
        o2 = ord(str2[i])
        if o1 > o2:
            return True
        if o1 < o2:
            return False
    return False

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
    if cov > 1:
        cov = cov/(N-1)
        return cov
    else:
        cov = cov/N
        return cov




if __name__ == '__main__':
    toplines.run()