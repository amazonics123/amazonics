from mrjob.job import MRJob
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
        arr = np.asarray(line.split())
    	yield arr, None

    def mapper_second(self, arr, line):
        arrmatey = np.asarray(line.split())
        score = regression.find_best_fit(arr, value_storer[-1])
        yield (arr, arrmatey), score

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
        h = [(score, covars) for (covars, score) in list(counts.items())[:k]]
        heapq.heapify(h)

        for covars, score in

    def reducer_init(self):
        over_df = pd.DataFrame(columns=['scores', 'covars'])

    def reducer(self, _, df):
        over_df = over_df.append(df)

    def reducer_final(self):
    	yield None, over_df.sort_values(by=['scores']).head(50)

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