import sys
import pandas as pd
import numpy as np

print(sys.argv)

file = open(sys.argv[1], "r")
score_list = []
label_list = []
for line in file:
    list_split = line[4:-3]
    list_split = list_split.split("], ")
    #print(list_split)
    new_list = []
    for thing in list_split:
        new_item = thing[1:].split(", ")
        score_list.append(float(new_item[0]))
        label_list.append(new_item[1][1:-1])

df = pd.DataFrame({'score': score_list, 'label': label_list})
df = df.sort_values(by='score', ascending=False)
print(df.head(50))