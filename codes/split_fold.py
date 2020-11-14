import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn import preprocessing
from config import config
import os

path = 'C:/Users/xiongxiaoji/Desktop/41467_2018_4647_MOESM4_ESM.csv'
result_root = config['tensor_root']
# result_root = 'C:/Users/xiongxiaoji/Documents/GitHub/DTF-Drug-Synergy/data_sets/tensor'
data = pd.read_csv(path)[['gene1', 'gene2', 'cancer_type', 'SL']]
print(data.head())

# explore
cancer_type = data['cancer_type']
all_cancer_type = list(set(cancer_type))
print(f'length of all cancer type: {len(all_cancer_type)}')

gene1 = set(data['gene1'])
gene2 = set(data['gene2'])
print(f'legnth of gene1: {len(gene1)}, legnth of gene2: {len(gene2)}')

all_gene = list(gene1 | gene2)
print(f'length of all gene: {len(all_gene)}')
all_info = data

# encode
# Encode target labels with value between 0 and n_classes-1.
gene_le = preprocessing.LabelEncoder()
gene_le.fit(all_gene)
all_info['gene1'] = gene_le.transform(all_info['gene1'])
all_info['gene2'] = gene_le.transform(all_info['gene2'])

cancer_le = preprocessing.LabelEncoder()
cancer_le.fit(all_cancer_type)
all_info['cancer_type'] = cancer_le.transform(all_info['cancer_type'])

# split dataset 
X = all_info[['gene1', 'gene2', 'cancer_type']].values
y = all_info['SL'].values
skf = StratifiedKFold(n_splits=5)
skf.get_n_splits(X, y)

print(skf)

for idx, (train_index, test_index) in enumerate(skf.split(X, y)):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    # split
    num_train = len(train_index)
    len_fold = int(num_train / 4)
    fold_1 = X_train[:len_fold]
    label_1 = y_train[:len_fold]
    index_1 = train_index[:len_fold]

    fold_2 = X_train[len_fold:len_fold*2]
    label_2 = y_train[len_fold:len_fold*2]
    index_2 = train_index[len_fold:len_fold*2]

    fold_3 = X_train[len_fold*2:len_fold*3]
    label_3 = y_train[len_fold*2:len_fold*3]
    index_3 = train_index[len_fold*2:len_fold*3]

    fold_4 = X_train[len_fold*3:len_fold*4]
    label_4 = y_train[len_fold*3:len_fold*4]
    index_4 = train_index[len_fold*3:len_fold*4]

    fold_0 = X_test
    label_0 = y_test
    index_0 = test_index
    
    # save
    # for i in range(5):
    path1 = os.path.join(config['root'], f'fold/1/X.csv')
    path2 = os.path.join(config['root'], f'fold/2/X.csv')
    path3 = os.path.join(config['root'], f'fold/3/X.csv')
    path4 = os.path.join(config['root'], f'fold/4/X.csv')
    path0 = os.path.join(config['root'], f'fold/0/X.csv')

    pd.DataFrame(fold_1).to_csv(path1, index=False)
    pd.DataFrame(fold_2).to_csv(path2, index=False)
    pd.DataFrame(fold_3).to_csv(path3, index=False)
    pd.DataFrame(fold_4).to_csv(path4, index=False)
    pd.DataFrame(fold_0).to_csv(path0, index=False)

    path1 = os.path.join(config['root'], f'fold/1/y.csv')
    path2 = os.path.join(config['root'], f'fold/2/y.csv')
    path3 = os.path.join(config['root'], f'fold/3/y.csv')
    path4 = os.path.join(config['root'], f'fold/4/y.csv')
    path0 = os.path.join(config['root'], f'fold/0/y.csv')
    

    pd.DataFrame(label_1).to_csv(path1, index=False)
    pd.DataFrame(label_2).to_csv(path2, index=False)
    pd.DataFrame(label_3).to_csv(path3, index=False)
    pd.DataFrame(label_4).to_csv(path4, index=False)
    pd.DataFrame(label_0).to_csv(path0, index=False)

    path1 = os.path.join(config['root'], f'fold/1/index.csv')
    path2 = os.path.join(config['root'], f'fold/2/index.csv')
    path3 = os.path.join(config['root'], f'fold/3/index.csv')
    path4 = os.path.join(config['root'], f'fold/4/index.csv')
    path0 = os.path.join(config['root'], f'fold/0/index.csv')
    

    pd.DataFrame(index_1).to_csv(path1, index=False)
    pd.DataFrame(index_2).to_csv(path2, index=False)
    pd.DataFrame(index_3).to_csv(path3, index=False)
    pd.DataFrame(index_4).to_csv(path4, index=False)
    pd.DataFrame(index_0).to_csv(path0, index=False)




