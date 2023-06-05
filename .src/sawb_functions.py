import pandas as pd
import numpy as np
import xarray as xr
from scipy import stats as st
import glob
from PIL import Image

# Standardized Precipitation Index Function - Polygon with .nc
def spi(ds, thresh, dimension):
    # Original function script from https://github.com/jeffjay88/Climate_Indices
    # ds - data ; thresh - time interval / scale; dimension - dimension as a string

    # Rolling Mean / Moving Averages
    ds_ma = ds.rolling(time=thresh, center=False).mean(dim=dimension)

    # Natural log of moving averages
    ds_In = np.log(ds_ma)
    ds_In = ds_In.where(np.isinf(ds_In) == False)  # = np.nan  #Change infinity to NaN

    #ds_mu = ds_ma.mean(dimension)

    # Overall Mean of Moving Averages
    ds_mu = ds_ma.mean(dimension)

    # Summation of Natural log of moving averages
    ds_sum = ds_In.sum(dimension)

    # Computing essentials for gamma distribution
    n = ds_In[thresh - 1:, :, :].count(dimension)  # size of data
    A = np.log(ds_mu) - (ds_sum / n)  # Computing A
    alpha = (1 / (4 * A)) * (1 + (1 + ((4 * A) / 3)) ** 0.5)  # Computing alpha  (a)
    beta = ds_mu / alpha  # Computing beta (scale)

    # Gamma Distribution (CDF)
    gamma_func = lambda data, a, scale: st.gamma.cdf(data, a=a, scale=scale)
    gamma = xr.apply_ufunc(gamma_func, ds_ma, alpha, beta)

    # Standardized Precipitation Index   (Inverse of CDF)
    norminv = lambda data: st.norm.ppf(data, loc=0, scale=1)
    norm_spi = xr.apply_ufunc(norminv, gamma)  # loc is mean and scale is standard dev.

    return ds_ma, ds_In, ds_mu, ds_sum, n, A, alpha, beta, gamma, norm_spi


# Standardized Precipitation Index Function - Point with .csv
def spi_point(ds, thresh):
    # ds - data ; thresh - time interval / scale

    # Rolling Mean / Moving Averages
    ds_ma = ds.rolling(thresh, center=False).mean()

    # Natural log of moving averages
    ds_In = np.log(ds_ma)
    ds_In[np.isinf(ds_In) == True] = np.nan  # Change infinity to NaN

    # Overall Mean of Moving Averages
    ds_mu = np.nanmean(ds_ma)

    # Summation of Natural log of moving averages
    ds_sum = np.nansum(ds_In)

    # Computing essentials for gamma distribution
    n = len(ds_In[thresh - 1:])  # size of data
    A = np.log(ds_mu) - (ds_sum / n)  # Computing A
    alpha = (1 / (4 * A)) * (1 + (1 + ((4 * A) / 3)) ** 0.5)  # Computing alpha  (a)
    beta = ds_mu / alpha  # Computing beta (scale)

    # Gamma Distribution (CDF)
    gamma = st.gamma.cdf(ds_ma, a=alpha, scale=beta)

    # Standardized Precipitation Index   (Inverse of CDF)
    norm_spi = st.norm.ppf(gamma, loc=0, scale=1)  # loc is mean and scale is standard dev.

    return ds_ma, ds_In, ds_mu, ds_sum, n, A, alpha, beta, gamma, norm_spi

def year_range_eval(data_time, year_min, year_max):
    year_min_data = data_time.min().values
    year_min_data = pd.to_datetime(year_min_data).year
    year_max_data = data_time.max().values
    year_max_data = pd.to_datetime(year_max_data).year
    if year_min_data > year_min:
        print('\nAttention: your enter minimum year value %d has changed for %d' %(year_min, year_min_data))
        year_min = year_min_data
    if year_max_data < year_max:
        print('Attention: your enter maximum year value %d has changed for %d' %(year_max, year_max_data))
        year_max = year_max_data
    return year_min, year_max


# Gif creation
def make_gif(frame_folder, key_name, file_ext):
    key_name_c = '*' + key_name + '*' + file_ext
    frame_len = len(glob.glob(f'{frame_folder}/{key_name_c}'))
    print('Frames: %d' %frame_len)
    seconds_frame = 2
    duration = frame_len * seconds_frame * 60  # miliseconds
    frames = [Image.open(image) for image in glob.glob(f'{frame_folder}/{key_name_c}')]
    frame_one = frames[0]
    frame_one.save(frame_folder+key_name+'.gif', format='GIF', append_images=frames, save_all=True, duration=duration, loop=0)


# Function for print and show results in a log file
def print_log(file_log, txt_print, on_screen=True, center_div=False):
    if on_screen:
        print(txt_print)
    if center_div:
        file_log.write('\n<div align="center">\n' + '\n')
    file_log.write(txt_print + '\n')
    if center_div:
        file_log.write('\n</div>\n' + '\n')