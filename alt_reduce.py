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




if __name__ == '__main__':
    toplines.run()
