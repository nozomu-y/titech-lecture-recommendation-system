import pandas as pd
import glob

import json
path_open = open('path_clustering.json', 'r')
paths = json.load(path_open)

import pandas as pd 
docs=[]

for path in paths.keys():
    print(path)
    csv_files_goal = 'DetData/'+path+'/goal.csv'
    csv_files_key = 'DetData/'+path+'/key.csv'
    csv_files_rela = 'DetData/'+path+'/rela.csv'
    csv_files_sum = 'DetData/'+path+'/sum.csv'
    csv_files_task = 'DetData/'+path+'/task.csv'
    
    #df = pd.read_csv(path)
    data_list = []
    for i in range(5):
        data_list.append(pd.read_csv(csv_files_goal))
    for i in range(5):
        data_list.append(pd.read_csv(csv_files_key))
    for i in range(1):
        data_list.append(pd.read_csv(csv_files_rela))
    for i in range(7):
        data_list.append(pd.read_csv(csv_files_sum))
    for i in range(1):
        data_list.append(pd.read_csv(csv_files_task))
    
    df = pd.concat(data_list, axis=0)
    df.to_csv('data/'+path+'.csv',index=False)
