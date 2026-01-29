# -*- coding: UTF-8 -*-
# Name:
# Description: this script concatenate multiple .dbf files into an unique .csv file (SAWB.tbx has to be run before this script)
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
ppoi_path = '../.ppoi/1/' # Your local PPOI path
awb_qm_join_file = 'awb_qm.csv' # Joined file name
awb_qm_pivot_file = 'awb_qm_pivot.csv' # Joined average flow file name
awb_aa_pivot_file = 'awb_aa_pivot.csv' # Joined accumulation area file name
awb_dbf_files = glob.glob(ppoi_path + 'awb/qm/' + '*.dbf')
awb_df = pd.DataFrame()
show_plot = False  # Verbose plot

# AWB post-processing
for i in awb_dbf_files:
    print('AWB - Processing: %s' %i)
    awb_dbf = DBF(i)
    awb_data_result = pd.DataFrame(iter(awb_dbf))
    awb_df = pd.concat([awb_df, awb_data_result], ignore_index=False)
awb_year_min = awb_df['year'].min()
awb_year_max = awb_df['year'].max()
year_list = np.linspace(awb_year_min, awb_year_max, (awb_year_max-awb_year_min+1))
print('\nYear list %s\n' %year_list)
awb_df['date'] = pd.to_datetime(awb_df['date'])
awb_df.sort_values(by='date', inplace=True)
print(awb_df.dtypes)
awb_df = awb_df.set_index('date')
print(awb_df)
awb_df.to_csv(ppoi_path+'awb/'+awb_qm_join_file, encoding='utf-8', index=True)
awb_df.plot(y='SUM', figsize=(10,6), title='AWB - Atmospheric monthly average flow serie', ylabel='Qm, m³/s')
plt.savefig(ppoi_path+'awb/graph/awb_qm_serie.png')
if show_plot: plt.show()
awb_df.plot(y='Akm2', figsize=(10,6), title='AWB - Atmospheric monthly accumulation area serie', ylabel='A, km²')
plt.savefig(ppoi_path+'awb/graph/awb_aa_serie.png')
if show_plot: plt.show()
pivot_table_qm = awb_df.pivot_table(index='month', columns='year', values='SUM')
print(pivot_table_qm)
pivot_table_qm.to_csv(ppoi_path+'awb/'+awb_qm_pivot_file, encoding='utf-8', index=True)
pivot_table_qm.plot(y=year_list, figsize=(10,6), title='AWB - Atmospheric monthly average flow by year', ylabel='Qm, m³/s')
plt.savefig(ppoi_path+'awb/graph/awb_qm_monthly.png')
if show_plot: plt.show()
pivot_table_aa = awb_df.pivot_table(index='month', columns='year', values='Akm2')
print(pivot_table_aa)
pivot_table_aa.to_csv(ppoi_path+'awb/'+awb_aa_pivot_file, encoding='utf-8', index=True)
pivot_table_aa.plot(y=year_list, figsize=(10,6), title='AWB - Atmospheric monthly accumulation area by year', ylabel='A, km²')
#plt.xticks(range(len(pivot_table_aa)),labels=range(0, len(pivot_table_aa)))
plt.savefig(ppoi_path+'awb/graph/awb_aa_monthly.png')
if show_plot: plt.show()
plt.close('all')
