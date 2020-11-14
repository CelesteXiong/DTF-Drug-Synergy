from config import config
import pandas as pd
import os

path = 'C:/Users/xiongxiaoji/Desktop/41467_2018_4647_MOESM4_ESM.csv'
suppressor_path = 'C:/Users/xiongxiaoji/Desktop/Manitoba/Shuangyu/meeting1/Human_TSGs.csv'
result_root = config['tensor_root']

data = pd.read_csv(path)
gene1 = set(data['gene1'])
gene2 = set(data['gene2'])
print(f'legnth of gene1: {len(gene1)}, legnth of gene2: {len(gene2)}')

suppressor = pd.read_csv(suppressor_path)
sup_gene1 = set(suppressor['GeneSymbol'])
print(f'length of suppressor gene: {len(sup_gene1)}')
map_gene1 = sup_gene1 & gene1
print(f'length of mapped gene: {len(map_gene1)}')

# save mapped gene_a-gene_b-cancer_type-SL pairs
suppress_df = data[data['gene1'].isin(sup_gene1) ]
suppress_df = suppress_df.reset_index(drop=True)
print(f'original data df shape: {data.shape}')
print(f'suppressed df shape: {suppress_df.shape}')
print(f'suppressed rows: {data.shape[0] - suppress_df.shape[0]}')
print(suppress_df.head())

## save
path = os.path.join(config['root'], 'suppress', 'suppress.csv')
# path = 'C:/Users/xiongxiaoji/Documents/GitHub/DTF-Drug-Synergy/data_sets/suppress/suppress.csv'
suppress_df.to_csv(path)

## check
# print(pd.read_csv(path, index_col = 0).head())