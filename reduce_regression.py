from mrjob.job import MRJob
import numpy as np
import regression

class toplines(MRJob):
    
    def mapper_init(self):
        value_storer = []
        added = False

    def mapper(self, _, line):
        '''
        pass to another mapper? for this line, give another mapper
        the csv and the line and then compare them all
        '''
        arr = np.asarray(line.split())
        if arr not in value_storer:
            if not added:
                value_storer.append(arr)
                added = True
            else:
                score = regression.find_best_fit(arr, value_storer[-1])
    	yield (arr, value_storer[-1]), score

    def combiner():
        yield

    def reducer():
        yield

    def steps(self):
        return []