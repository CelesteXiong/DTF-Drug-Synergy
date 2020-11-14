# split all valid values to 5 folds based on stratififed cross validation in cv.png
# leave gene combinations out 
# use the first fold (fold_0) as val dataset

import os
import pandas as pd 
import numpy as np
from config import config

path = 'C:/Users/xiongxiaoji/Desktop/41467_2018_4647_MOESM4_ESM.csv'
result_root = config['tensor_root']
# result_root = 'C:/Users/xiongxiaoji/Documents/GitHub/DTF-Drug-Synergy/data_sets/tensor'
data = pd.read_csv(path)
print(data['cancer_type'].value_counts())
top_k = 3
top_type = data['cancer_type'].value_counts()[:top_k].index.to_list()
print(top_type)

filter = data[(data['cancer_type'] ==  top_type[0]) | (data['cancer_type'] ==  top_type[1]) ]
print(filter.shape)

# filter the combinations valid in all cancer type
valid_count = {} # {[gene1, gene2]: count}
# for c in range(len(num_cancer_type)):
filter_data = filter.groupby(['gene1', 'gene2']).count().reset_index()
filter_data = filter_data[filter_data['SL'] == 2].reset_index()[['gene1', 'gene2', 'cancer_type', 'SL']]
print(filter_data.head())
print(data.shape)
print(filter_data.shape)

# 计算频率
num_cancer_type = 8
top_type = data['cancer_type'].value_counts().index.to_list()
sort_dict = {}
for i in range(num_cancer_type):
    print(top_type[i])
    filter = data[(data['cancer_type'] ==  top_type[i])]
    # print(filter.shape)

    # filter the combinations valid in all cancer type
    valid_count = {} # {[gene1, gene2]: count}
    # for c in range(len(num_cancer_type)):
    filter_data = filter.groupby(['gene1', 'gene2']).count().reset_index()
    filter_data = filter_data.reset_index()[['gene1', 'gene2', 'cancer_type', 'SL']]
    print(filter_data.head())
    print(data.shape)
    print(filter_data.shape)
    sort_dict[top_type[i]] = filter_data.shape

print(sorted(sort_dict.items(),key=lambda x:x[1][0], reverse=True))

