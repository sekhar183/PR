import streamlit as st 
import numpy as np 
import pandas as pd 
import datetime
from datetime import date, timedelta
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
import zipfile
st.set_page_config(layout="wide")#sets page wide

#Loading data
zf = zipfile.ZipFile('temphum_all.zip') 
dataframe = pd.read_csv(zf.open('temphum_all.csv'))
dataframe['humid']=dataframe['humid'].replace(99,np.nan)

#Filtering data using filters(only considering 'time' for now)
def filt(dataframe,start_date,end_date):
	df=dataframe[(dataframe['time']<=str(end_date+timedelta(1)))&(dataframe['time']>=str(start_date))]
	return df

#Filters

start_date = st.sidebar.date_input('start date', date.today()-timedelta(5),min_value=datetime.datetime(2020,11,13),max_value=date.today())#start date
end_date = st.sidebar.date_input('end date', date.today(),max_value=date.today())#end date
ft=filt(dataframe,start_date,end_date)

#filtering data using filters
st.markdown("""<style>.big-font2 {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-font2">Filtered DataFrame</p>', unsafe_allow_html=True)
st.dataframe(ft)#showing data frame in App
st.write(ft.shape)
with st.beta_expander("code"):
     st.code('''def filt(dataframe,start_date,end_date):
     	df=dataframe[(dataframe["time"]<=str(end_date+timedelta(1)))&(dataframe["time"]>=str(start_date))]
     	return df''', language="python")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Seperating data
#OFC
ft_ofc=ft[ft['location']=='PR Home - OFC']
#MBW
ft_mbw=ft[ft['location']=='PR Home - MBW']
#KIT
ft_kit=ft[ft['location']=='PR Home - KIT']
#LVR
ft_lvr=ft[ft['location']=='PR Home - LVR']
#MWR
ft_mwr=ft[ft['location']=='PR Home - MWR']
#LRM
ft_lrm=ft[ft['location']=='PR Home - LRM']
#MBE
ft_mbe=ft[ft['location']=='PR Home - MBE']

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

st.markdown("""<style>.big-font {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-font">STATS</p>', unsafe_allow_html=True)

result_df=ft[['location','obj_temp','humid']].groupby(['location']).describe()
result_cols=result_df.columns
#summary_dict={'PR Home - OFC':ft_ofc.shape[0],'PR Home - MBE':ft_mbe.shape[0],'PR Home - MBW':ft_mbw.shape[0],'PR Home - MWR':ft_mwr.shape[0],'PR Home - LRM':ft_lrm.shape[0],'PR Home - KIT':ft_kit.shape[0],'PR Home - LVR':ft_lvr.shape[0]}
#result_df['no.of samples']=result_df.index.map(summary_dict)
#result_cols.insert(0,('samples', 'count'))
st.dataframe(result_df.style.highlight_max(axis=0,color='grey'))
with st.beta_expander("code"):
     st.code('''result_df=ft[['location','obj_temp','humid']].groupby(['location']).describe()
st.dataframe(result_df.style.highlight_max(axis=0,color='grey'))''', language="python")
#st.write(result_cols)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Plotting graphs>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.


#TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
st.write('-'*300)
st.markdown("""<style>.big-temp {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-temp">Temperature Distribution Plot</p>', unsafe_allow_html=True)

temp_dist=px.violin(dataframe,x='location',y='obj_temp')
temp_dist.update_layout(showlegend=False,hovermode="x",template='simple_white')
st.plotly_chart(temp_dist,sharing='streamlit',use_container_width=True)

#HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
st.write('-'*300)
st.markdown("""<style>.big-hum {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-hum">Humidity Distribution Plot</p>', unsafe_allow_html=True)

hum_dist=px.violin(dataframe,x='location',y='humid')
hum_dist.update_layout(showlegend=False,hovermode="x",template='simple_white')
st.plotly_chart(hum_dist,sharing='streamlit',use_container_width=True)
#11111111111111111111---------------------------------------OFFICE ROOM------------------------------------------------------------------1111111111111111111111
st.write('-'*300)
st.markdown("""<style>.big-ofc {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-ofc">Office Room</p>', unsafe_allow_html=True)


fig_ofc= make_subplots(specs=[[{"secondary_y": True}]])
fig_ofc.add_trace(go.Scatter(x=ft_ofc.time, y=ft_ofc.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_ofc.add_trace(go.Scatter(x=ft_ofc.time, y=ft_ofc.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_ofc.add_trace(go.Scatter(x=ft_ofc.time, y=ft_ofc.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_ofc.add_trace(go.Scatter(x=ft_ofc.time, y=ft_ofc.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)


fig_ofc.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text='<b>'+ft_ofc['location'].unique()[0]+'</b>',title_x=0.44)
fig_ofc.update_xaxes(title_text="time")
fig_ofc.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_ofc.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_ofc, sharing='streamlit',use_container_width=True)
