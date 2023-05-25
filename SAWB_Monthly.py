# -*- coding: UTF-8 -*-
# Name: CNEStationCSVJoin.py
# Description: this script uncompress and join multiple .zip files get manually from http://dhime.ideam.gov.co/atencionciudadano/ into a single .csv file.
# Repository: https://github.com/rcfdtools/R.LTWB/tree/main/Section03/CNEStationDatasetDownload
# License: https://github.com/rcfdtools/R.LTWB/wiki/License
# Requirements: Python 3+, Pandas,

# Libraries
import glob
import os
import pandas as pd
from dbfread import DBF
import numpy as np
import matplotlib.pyplot as plt

# Procedure
path = '.temp/qm/' # Your local .dbf
join_file = '_Qm.csv' # Joined file name
pivot_file_qm = '_QmPivot.csv' # Joined average flow file name
pivot_file_aa = '_AaPivot.csv' # Joined accumulation area file name
if os.path.isfile(path + join_file):
    os.remove(path + join_file)
dbf_files = glob.glob(path + '*.dbf')
df = pd.DataFrame()
for i in dbf_files:
    print('Processing: %s' %i)
    dbf = DBF(i)
    dataResult = pd.DataFrame(iter(dbf))
    #print(dataResult)
    df = pd.concat([df, dataResult], ignore_index=False)
min_year = df['year'].min()
max_year = df['year'].max()
year_list = np.linspace(min_year, max_year, (max_year-min_year+1))
print('\nYear list %s\n' %year_list)
df['date'] = pd.to_datetime(df['date'])
df.sort_values(by='date', inplace = True)
print(df.dtypes)
df = df.set_index('date')
print(df)
df.to_csv(path+join_file, encoding='utf-8', index=True)
df.plot(y='SUM', figsize=(9,6), title='Atmospheric monthly average flow serie', ylabel='Qm, m³/s')
plt.show()
df.plot(y='Akm2', figsize=(9,6), title='Atmospheric monthly accumulation area serie', ylabel='A, km²')
plt.show()
pivot_table_qm = df.pivot_table(index='month', columns='year', values='SUM')
print(pivot_table_qm)
pivot_table_qm.to_csv(path+pivot_file_qm, encoding='utf-8', index=True)
pivot_table_qm.plot(y=year_list, figsize=(9,6), title='Atmospheric monthly average flow by year', ylabel='Qm, m³/s')
plt.show()
pivot_table_aa = df.pivot_table(index='month', columns='year', values='Akm2')
print(pivot_table_aa)
pivot_table_aa.to_csv(path+pivot_file_aa, encoding='utf-8', index=True)
pivot_table_aa.plot(y=year_list, figsize=(9,6), title='Atmospheric monthly accumulation area by year', ylabel='A, km²')
#plt.xticks(range(len(pivot_table_aa)),labels=range(0, len(pivot_table_aa)))
plt.show()


# References
# https://stackoverflow.com/questions/41898561/pandas-transform-a-dbf-table-into-a-dataframe
# https://sparkbyexamples.com/pandas/sort-pandas-dataframe-by-date/
# https://www.dataquest.io/blog/plot-dataframe-pandas/
# https://www.geeksforgeeks.org/numpy-linspace-python/