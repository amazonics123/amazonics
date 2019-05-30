from mrjob.job import MRJob
import numpy as np
import regression

class toplines(MRJob):
    
    def mapper(self, firstline, line):
        '''
        pass to another mapper? for this line, give another mapper
        the csv and the line and then compare them all
        '''
        firstline = np.asarray(firstline.split())
        newline = np.asarray(line.split())
        score = regression.find_best_fit(x, y)
    	yield line, score

    def combiner():
        yield

    def reducer():
        yield


class comparer(MRJob):
    def mapper(self, param, line):
        array = line.split(",")