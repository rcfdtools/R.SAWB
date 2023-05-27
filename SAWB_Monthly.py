# -*- coding: UTF-8 -*-
# Name:
# Description: this script concatenate multiple .dbf files into an unique .csv file
# Repository:
# License:
# Requirements:

# Libraries
import glob
import os
import pandas as pd
from dbfread import DBF
import numpy as np
import matplotlib.pyplot as plt

# Variables
path = '.poi/1/' # Your local path
join_file = 'Qm.csv' # Joined file name
pivot_file_qm = 'QmPivot.csv' # Joined average flow file name
pivot_file_aa = 'AaPivot.csv' # Joined accumulation area file name
dbf_files = glob.glob(path + 'qm/' + '*.dbf')
df = pd.DataFrame()
show_plot = False  # Verbose plot

# Procedure
for i in dbf_files:
    print('Processing: %s' %i)
    dbf = DBF(i)
    dataResult = pd.DataFrame(iter(dbf))
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
df.plot(y='SUM', figsize=(10,6), title='AWB - Atmospheric monthly average flow serie', ylabel='Qm, m³/s')
plt.savefig(path + 'Graph/Plot_QmSerie.png')
if show_plot: plt.show()
df.plot(y='Akm2', figsize=(10,6), title='AWB - Atmospheric monthly accumulation area serie', ylabel='A, km²')
plt.savefig(path + 'Graph/Plot_AaSerie.png')
if show_plot: plt.show()
pivot_table_qm = df.pivot_table(index='month', columns='year', values='SUM')
print(pivot_table_qm)
pivot_table_qm.to_csv(path+pivot_file_qm, encoding='utf-8', index=True)
pivot_table_qm.plot(y=year_list, figsize=(10,6), title='AWB - Atmospheric monthly average flow by year', ylabel='Qm, m³/s')
plt.savefig(path + 'Graph/Plot_QmMonthly.png')
if show_plot: plt.show()
pivot_table_aa = df.pivot_table(index='month', columns='year', values='Akm2')
print(pivot_table_aa)
pivot_table_aa.to_csv(path+pivot_file_aa, encoding='utf-8', index=True)
pivot_table_aa.plot(y=year_list, figsize=(10,6), title='AWB - Atmospheric monthly accumulation area by year', ylabel='A, km²')
#plt.xticks(range(len(pivot_table_aa)),labels=range(0, len(pivot_table_aa)))
plt.savefig(path + 'Graph/Plot_AaMonthly.png')
if show_plot: plt.show()
plt.close('all')


# References
# https://stackoverflow.com/questions/41898561/pandas-transform-a-dbf-table-into-a-dataframe
# https://sparkbyexamples.com/pandas/sort-pandas-dataframe-by-date/
# https://www.dataquest.io/blog/plot-dataframe-pandas/
# https://www.geeksforgeeks.org/numpy-linspace-python/