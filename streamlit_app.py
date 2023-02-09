import pandas as pd
from pyvis.network import Network

df = pd.read_csv('data/results.csv').fillna('')
print(df)
