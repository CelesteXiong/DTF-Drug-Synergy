# the file is used to create tensor
# if the class of gene and cancer type is D and C, respectively, then the tensor will be in shape of D * D * C
# the tensor is saved as C files, in which a matrix with shape D * D is saved as a numpy

import os
import pandas as pd 
import numpy as np
from config import config

path = 'C:/Users/xiongxiaoji/Desktop/41467_2018_4647_MOESM4_ESM.csv'
result_root = config['tensor_root']
# result_root = 'C:/Users/xiongxiaoji/Documents/GitHub/DTF-Drug-Synergy/data_sets/tensor'
data = pd.read_csv(path)
# data = pd.DataFrame([[1, 1, 0, 1], [1, 2, 1, 1], [2, 1, 0, 0], [2, 2, 1, 0], [2, 2, 1, 0]], columns=['gene1', 'gene2', 'cancer_type', 'SL'])
print(data.isnull().any())

cancer_type = data['cancer_type']
all_cancer_type = list(set(cancer_type))
print(f'length of all cancer type: {len(all_cancer_type)}')

gene1 = set(data['gene1'])
gene2 = set(data['gene2'])
print(f'legnth of gene1: {len(gene1)}, legnth of gene2: {len(gene2)}')

all_gene = list(gene1 | gene2)
print(f'length of all gene: {len(all_gene)}')
all_info = data
# print(data.head())

# encode 
from sklearn import preprocessing
gene_le = preprocessing.LabelEncoder()
gene_le.fit(all_gene)
all_info['gene1'] = gene_le.transform(all_info['gene1'])
all_info['gene2'] = gene_le.transform(all_info['gene2'])

# Encode target labels with value between 0 and n_classes-1.
cancer_le = preprocessing.LabelEncoder()
cancer_le.fit(all_cancer_type)
all_info['cancer_type'] = cancer_le.transform(all_info['cancer_type'])

# manipulate duplicate (gene, gene) pair
dedup_info = all_info.drop_duplicates(subset=['gene1', 'gene2', 'cancer_type'])[['gene1', 'gene2', 'cancer_type', 'SL']]
print(dedup_info.head())
# print(all_info.shape)
# print(dedup_info.shape)

# # save all names and encode
# basic_info = r'C:\Users\xiongxiaoji\Documents\GitHub\DTF-Drug-Synergy\data_sets\basic_info'
# pd.DataFrame(list(zip(gene_le.transform(all_gene), all_gene)), columns=['encode', 'name']).to_csv(os.path.join(basic_info, 'gene_names.csv'), index= False)
# pd.DataFrame(list(zip(cancer_le.transform(all_cancer_type), all_cancer_type)), columns=['encode', 'name']).to_csv(os.path.join(basic_info, 'cancer_tpye_names.csv'), index=False)


# # # create output matrix
# # shape = (len(all_gene), len(all_gene))

# # # 生成tensor, 并保存
# # # ! 先取7个cancer type做实验
# # for i in range(len(all_cancer_type)):
# #     print('i: ', i)
# #     one_cancer = dedup_info[dedup_info['cancer_type'] == i]
# #     index = one_cancer.index.to_list()
# #     print(dedup_info)
# #     one_cancer = one_cancer.reset_index(drop=True)
# #     # fill in matrix with valid SL value
# #     matrix = np.zeros(shape)
# #     # record locations of valid values
# #     count = 0
# #     locate_valid = np.zeros((len(all_gene), len(all_gene)))
# #     # print(one_cancer)
# #     for idx in range(one_cancer.shape[0]):
# #         matrix[one_cancer['gene1'][idx], one_cancer['gene2'][idx]] = one_cancer['SL'][idx]
# #         # print(one_cancer['SL'][idx])
# #         if one_cancer['SL'][idx] == 1: print ('SL 1')
        
# #     # create symmetrical structure
# #     for row in range(shape[0]):
# #         matrix[row, row] = 0
# #         for col in range(row, shape[0]):
# #             # print(row, col, matrix.shape)
# #             # locate valid values
# #             if row != col: 
# #                 miss = one_cancer[(one_cancer['gene1']==row) 
# #                                     & (one_cancer['gene2']==col)
# #                                     & (one_cancer['cancer_type'] == i)].empty
# #                 if not miss:
# #                     count += 1
# #                     locate_valid[row, col] = 1 
# #                     print(col)
# #                     print(one_cancer[(one_cancer['gene1']==row) 
# #                                     & (one_cancer['gene2']==col)
# #                                     & (one_cancer['cancer_type'] == i)])

# #             if matrix[row, col]:
# #                 matrix[col, row] = matrix[row, col]
# #             elif matrix[col, row]:
# #                 matrix[row, col] = matrix[col, row]
    
# #     # save as file, index starts from 1
# #     path = os.path.join(result_root, f'tensor_{i+1}.csv')
# #     tensor = pd.DataFrame(matrix)
# #     # tensor['index'] = index
# #     tensor.to_csv(path)

# #     path = os.path.join(config['root'], f'location/valid_{i+1}.csv')
# #     valid = pd.DataFrame(locate_valid)
# #     valid['index'] = index
# #     valid.to_csv(path)

# # print(count)

           

            
