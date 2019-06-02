from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np
import regression
import pandas as pd
import heapq

class toplines(MRJob):
    
    def mapper_first(self, _, line):
        '''
        pass to another mapper? for this line, give another mapper
        the csv and the line and then compare them all
        '''

        arr = line.strip("[]").split(", ")
        yield arr, line

    def mapper_second(self, arr, line):
        arrmatey = line.strip("[]").split(", ")
        tuple_score = regression.do_everything(arr, arrmatey)
        yield tuple_score[0], tuple_score[1]

    def combiner_init(self):
        '''
        score_store = []
        covars_store = []
        '''
        scores = {}

    def combiner(self, covars, score):
        scores[covars] = score

    def combiner_final(self):
        '''
        
        dataframe = pd.DataFrame(np.array([score_store, covars_store]), columns=['scores', 'covars'])
        yield None, dataframe.sort_values(by=['scores']).head(50)
        '''
        k = 50
        for i in len(dict):
            n = int(i)
            scores[n] = scores.setdefault(n, 0) + 1
        h = [(score, covars) for (covars, score) in list(scores.items())[:k]]
        heapq.heapify(h)

        for covars, score in scores.items()[k:]:
            min_score, min_covars = h[0]

            if score > min_score:
                heapq.heapreplace(h, (score, covars))
        
        h.sort(reverse=True)
        yield None, h

    def reducer_init(self):
        list_tops = []

    def reducer(self, _, h):
        list_tops.append(h)

    def reducer_final(self):
        h = list_tops[:k]
        heapq.heapify(h)
        
        for covars, score in scores.items()[k:]:
            min_score, min_covars = h[0]

            if score > min_score:
                heapq.heapreplace(h, (score, covars))
        
        h.sort(reverse=True)
        yield None, h

    def steps(self):
        return [
            MRStep(mapper=self.mapper_first),
            MRStep(mapper=self.mapper_second,
                combiner_init=self.combiner_init,
                combiner=self.combiner,
                combiner_final=self.combiner_final,
                reducer_init=self.reducer_init,
                reducer=self.reducer,
                reducer_final=self.reducer_final)]


if __name__ == '__main__':
    toplines.run()