import os
import pandas as pd 

path = 'C:/Users/xiongxiaoji/Desktop/41467_2018_4647_MOESM4_ESM.csv'
data = pd.read_csv(path)

print(data.head())
