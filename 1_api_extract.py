# %%
from src.libraries.extract import (
    generate_month_dates_as_strings,
    fetch_data_to_dataframe,
    save_df_to_json_in_dir)
import pandas as pd
import os



# %%
init_month='2024-01'
list_days=generate_month_dates_as_strings(init_month) 
final_df=pd.DataFrame()
for date in list_days:
    url=f'http://api.tvmaze.com/schedule/web?date={date}'
    print(f'Extracting from URL : {url}')
    df=fetch_data_to_dataframe(url, method='GET')
    print(f'DF Extracted with {len(df)} rows')
    final_df = pd.concat([df, final_df])
final_df


# %%
final_df = final_df.reset_index(drop=True)
final_df.to_csv('output_raw_data.csv')

# %%
directory_name = 'src/json_output/'
json_file_name = 'output_raw_data.json'

save_df_to_json_in_dir(final_df, json_file_name, directory_name)


# %%



