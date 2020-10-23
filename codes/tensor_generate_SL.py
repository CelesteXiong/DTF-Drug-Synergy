import os
import pandas as pd 
import numpy as np

path = 'C:/Users/xiongxiaoji/Desktop/41467_2018_4647_MOESM4_ESM.csv'
result_root = 'C:/Users/xiongxiaoji/Documents/GitHub/DTF-Drug-Synergy/data_sets/tensor'
data = pd.read_csv(path)
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

cancer_le = preprocessing.LabelEncoder()
cancer_le.fit(all_cancer_type)
all_info['cancer_type'] = cancer_le.transform(all_info['cancer_type'])

# manipulate duplicate (gene, gene) pair
dedup_info = all_info.drop_duplicates(subset=['gene1', 'gene2', 'cancer_type'])

# create output matrix
shape = (len(gene1), len(gene2))
matrix = np.zeros(shape)
for i in range(len(all_cancer_type)):
        one_cancer = dedup_info[dedup_info['cancer_type'] == all_cancer_type[i]]
        for idx in range(len(all_gene)):
            if idx < len(gene1) and idx < len(gene2):
                matrix[one_cancer['gene1'][idx], one_cancer['gene2'][idx]] = one_cancer['SL'][idx]
            else:
                matrix[one_cancer['gene1'][idx], one_cancer['gene2'][idx]] = one_cancer['SL'][idx]
        for row in range(shape[0]-1):
                for col in range(row+1, shape[0]):
                    if matrix[row, col]:
                        matrix[col, row] = matrix[row, col]
                    elif matrix[col, row]:
                        matrix[row, col] = matrix[col, row]
        matrix[shape[0]-1, shape[0]-1] = 0
        # convert null tp 0
        # matrix[np.where(matrix]

        # save as file 
        path = os.path.join(result_root, f'tensor_{i}.npy')
        np.save(path, matrix)
        
            

            
