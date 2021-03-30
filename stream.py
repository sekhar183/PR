#impoerting necessary libraries
import pandas as pd
import numpy as np 
import datetime as dt
from datetime import datetime,timedelta
from tqdm import tqdm
from requests import get
from datetime import date
import warnings
warnings.filterwarnings('ignore') #to ignore warnings

#history_file
df=pd.read_csv(r'C:\Users\kvsekhar\veera\Neha work\all_data\temphum_all.csv')

#past data is already collected(cleaned) and stored in csv file.
#new data is collected and cleaned and merged with past file.

#to get last date in history file
df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
last_sample=df.sort_values(by=['time'],ascending=False).reset_index(drop=True).iloc[0]
last_sample_date=last_sample['time'].strftime('%Y-%m-%d')
date_list=pd.date_range(last_sample_date,datetime.today()) #creates a list of dates where data needs to be extracted

#authorization and required rooms
req_temp_ids=[149,150,151,152,153,154,155]
url="https://water-iq.herokuapp.com/api/iq/sensors/"
Token='Token token=AC6b88d2d5fc648a1527cedb4b6c21f0'
auth = {'Authorization': Token}

#initiating Empty dataframe
df_api=pd.DataFrame(columns=['sensor_id', 'sensor_type', 'prev_page', 'current_page', 'next_page',
       'id', 'amb_temp', 'obj_temp', 'batt', 'time', 'count1', 'count2',
       'humid', 'status', 'triggered', 'tslice'])

#extracting data from api
for ids in tqdm(req_temp_ids,position=0):
    for dates in date_list:
        dat = get('https://water-iq.herokuapp.com/api/iq/sensors/'+str(ids)+'/sensor_logs?search[created_at_lteq]='+str(dates),headers=auth)
        df2 =pd.DataFrame(dat.json())
        df1=pd.json_normalize(df2['logs'])
        df3=pd.concat([df2,df1],axis=1).drop('logs',1)
        df_api=df_api.append(df3)

# mapping room id with room name
room_dict={149: 'PR Home - OFC',150: 'PR Home - MBE',151: 'PR Home - MBW',152: 'PR Home - MWR',153: 'PR Home - LRM',154: 'PR Home - KIT',155: 'PR Home - LVR'}
df_api['location']=df_api['sensor_id'].map(room_dict)

#our required locations
req_loc=['PR Home - MBW','PR Home - KIT','PR Home - LVR','PR Home - MWR','PR Home - OFC','PR Home - LRM','PR Home - MBE']
df_api=df_api[df_api['location'].isin(req_loc)]

# cleaning
df_api['time']=df_api['time'].apply(lambda x:x.replace('T'," "))
df_api['time']=df_api['time'].apply(lambda x:x.replace('Z',""))

#transforming into date time format and sorting
df_api['time'] = pd.to_datetime(df_api['time'], format='%Y-%m-%d %H:%M:%S')
df_api=df_api.sort_values(by=['time']).reset_index(drop=True)

#splitting time components
df_api['month'] = df_api.time.dt.month
df_api['weekday']=df_api['time'].dt.weekday
df_api=df_api.drop_duplicates(subset='id')

#removing duplicates
live_data=df.append(df_api)
live_data=live_data.drop_duplicates(subset='id')

#summary
print("past data: {}".format(df.shape))
print("api data: {}".format(df_api.shape))
print("Full data: {}".format(live_data.shape))

#saving data in streamlit folder
live_data.to_csv(r'C:\Users\kvsekhar\veera\Neha work\all_data\temphum_all.csv',index=False,header=live_data.columns)