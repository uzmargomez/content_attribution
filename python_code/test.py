from MarkovAttribution import MarkovAttribution
from MarkovDB import MarkovDB
from MarkovMatrix import MarkovMatrix
from google.oauth2 import service_account
from google.cloud import bigquery
from pathlib import Path
import pandas as pd

# query = Path('../examples/query.bqsql').read_text()

# client = bigquery.Client()

# dataframe = (
#     client.query(query)
#     .result()
#     .to_dataframe()
# )

# test_data = dataframe.to_dict('records')

# marka = MarkovAttribution(
#   dataset=test_data,
#   var_path='PAGE_PATH',  
#   var_conv='OPP_COUNT',
#   var_value='OPP_AMOUNT',
#   separator=' > ')

# print(marka.df_info)


# Preprocessing data 

# https://towardsdatascience.com/marketing-channel-attribution-with-markov-chains-in-python-part-2-the-complete-walkthrough-733c65b23323


df = pd.read_csv('../examples/data/attribution_data.csv')
df = df.sort_values(['cookie', 'time'],
                    ascending=[False, True])
df['visit_order'] = df.groupby('cookie').cumcount() + 1
df_paths = df.groupby('cookie')['channel'].aggregate(lambda x: x.unique().tolist()).reset_index()
df_last_interaction = df.drop_duplicates('cookie', keep='last')[['cookie', 'conversion']]
df_paths = pd.merge(df_paths, df_last_interaction, how='left', on='cookie')
df_paths['path'] = df_paths['channel'].agg(lambda x: ' > '.join(map(str, x)))
df_paths['value'] = 0
df_final = df_paths[['conversion','value','path']].to_dict('records')


# Defining separator
sep = ' > '

B = MarkovAttribution(df_final, 'path', 'conversion', 'value', sep)
print(B.df_info)