import os
import time
import argparse

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--csv', help='csv help')
args = parser.parse_args()

print(args.csv)

# csv_filename = None

# df = pd.read_csv(csv_filename, index_col='Date', 
#                 encoding='utf8'
#                 )
# df = df.fillna(0)

# shift = '_DS'
# df_day =  df.loc[:, df.columns.str.contains(shift)]
# df_day.columns = df_day.columns.str.replace(shift, '')
# df_day.index = pd.to_datetime([date + ' 06:00' for date in df_day.index])

# shift = '_NS'
# df_night =  df.loc[:, df.columns.str.contains(shift)]
# df_night.columns = df_night.columns.str.replace(shift, '')
# df_night.index = pd.to_datetime([date + ' 18:00' for date in df_night.index])

# concat_df = pd.concat([df_day,df_night]).sort_index().transpose()

# concat_df.to_csv(csv_filename.replace('.csv','') + 'TRANSPOSED.csv', float_format='%g')