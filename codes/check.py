import pandas as pd 
# filter
a = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 2, 4], [4, 5, 3]], columns=['gene1', 'gene2', 'cancer_type'])
# print(a)
# print(a[(a['gene1']==1) & (a['gene2'] == 2)])
# if a[(a['gene1']==1) & (a['gene2'] == 4)].empty: 
#     print('yes')

print(a.groupby(['gene1', 'gene2']).count().reset_index())

# import os
# import pandas as pd 
# import numpy as np
# from config import config

# path = 'C:/Users/xiongxiaoji/Desktop/41467_2018_4647_MOESM4_ESM.csv'
# result_root = config['tensor_root']
# # result_root = 'C:/Users/xiongxiaoji/Documents/GitHub/DTF-Drug-Synergy/data_sets/tensor'
# data = pd.read_csv(path)[:1000]
# print(sum(data['SL']))