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
st.markdown("""<style>.big-head {font-size:45px !important;text-align:center;text-decoration: underline;font-family: TimesNewRoman;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-head">PR SENSOR DATA</p>', unsafe_allow_html=True)
#note
st.write("*Note: All figures are filtered by 'start and end date' filters except for distribution plot*")
st.write("*Note: data is available from nov13, 2020 to mar30, 2021*")
st.write("*Note: page will take longer time to load figures as you increase date range*")
st.write("*Note: dotted lines in figures represent that there is no data during that period*")

#Loading data
zf = zipfile.ZipFile('temphum_all.zip') 
dataframe = pd.read_csv(zf.open('temphum_all.csv'))
dataframe['humid']=dataframe['humid'].replace(99,np.nan)

#Filtering data using filters(only considering 'time' for now)
def filt(dataframe,start_date,end_date):
	df=dataframe[(dataframe['time']<=str(end_date+timedelta(1)))&(dataframe['time']>=str(start_date))]
	return df

#Filters

start_date = st.sidebar.date_input('start date', date.today()-timedelta(3),min_value=datetime.datetime(2020,11,13),max_value=date.today())#start date
end_date = st.sidebar.date_input('end date', date.today(),max_value=date.today())#end date
ft=filt(dataframe,start_date,end_date)

#filtering data using filters
st.markdown("""<style>.big-font2 {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-font2">Filtered DataFrame</p>', unsafe_allow_html=True)
st.dataframe(ft)#showing data frame in App
st.write(ft.shape)
with st.beta_expander("code"):
     st.code('''def filt(dataframe,start_date,end_date):
	df=dataframe[(dataframe['time']<=str(end_date+timedelta(1)))&(dataframe['time']>=str(start_date))]
	return df

#Filters

start_date = st.sidebar.date_input('start date', date.today()-timedelta(5),min_value=datetime.datetime(2020,11,13),max_value=date.today())#start date
end_date = st.sidebar.date_input('end date', date.today(),max_value=date.today())#end date
ft=filt(dataframe,start_date,end_date)

#filtering data using filters
st.markdown("""<style>.big-font2 {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-font2">Filtered DataFrame</p>', unsafe_allow_html=True)
st.dataframe(ft)''', language="python")

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
     st.code('''st.markdown("""<style>.big-font {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-font">STATS</p>', unsafe_allow_html=True)

result_df=ft[['location','obj_temp','humid']].groupby(['location']).describe()
result_cols=result_df.columns
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
with st.beta_expander("code"):
	st.code('''st.markdown("""<style>.big-temp {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-temp">Temperature Distribution Plot</p>', unsafe_allow_html=True)

temp_dist=px.violin(dataframe,x='location',y='obj_temp')
temp_dist.update_layout(showlegend=False,hovermode="x",template='simple_white')
st.plotly_chart(temp_dist,sharing='streamlit',use_container_width=True)''', language="python")
#HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
st.write('-'*300)
st.markdown("""<style>.big-hum {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-hum">Humidity Distribution Plot</p>', unsafe_allow_html=True)

hum_dist=px.violin(dataframe,x='location',y='humid')
hum_dist.update_layout(showlegend=False,hovermode="x",template='simple_white')
st.plotly_chart(hum_dist,sharing='streamlit',use_container_width=True)
with st.beta_expander("code"):
	st.code('''st.markdown("""<style>.big-hum {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-hum">Humidity Distribution Plot</p>', unsafe_allow_html=True)

hum_dist=px.violin(dataframe,x='location',y='humid')
hum_dist.update_layout(showlegend=False,hovermode="x",template='simple_white')
st.plotly_chart(hum_dist,sharing='streamlit',use_container_width=True)''', language="python")
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
with st.beta_expander("code"):
	st.code('''st.markdown("""<style>.big-ofc {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
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

st.plotly_chart(fig_ofc, sharing='streamlit',use_container_width=True)''', language="python")

#11111111111111111111---------------------------------------OFFICE ROOM------------------------------------------------------------------1111111111111111111111
st.write('-'*300)
st.markdown("""<style>.big-mbw {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-mbw">Master Bedroom</p>', unsafe_allow_html=True)

fig_mbw= make_subplots(specs=[[{"secondary_y": True}]])
fig_mbw.add_trace(go.Scatter(x=ft_mbw.time, y=ft_mbw.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_mbw.add_trace(go.Scatter(x=ft_mbw.time, y=ft_mbw.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_mbw.add_trace(go.Scatter(x=ft_mbw.time, y=ft_mbw.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_mbw.add_trace(go.Scatter(x=ft_mbw.time, y=ft_mbw.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_mbw.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_mbw['location'].unique()[0],title_x=0.44)
fig_mbw.update_xaxes(title_text="time")

fig_mbw.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_mbw.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_mbw, sharing='streamlit',use_container_width=True)
with st.beta_expander("code"):
     st.code('''st.markdown("""<style>.big-mbw {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-mbw">Master Bedroom</p>', unsafe_allow_html=True)

fig_mbw= make_subplots(specs=[[{"secondary_y": True}]])
fig_mbw.add_trace(go.Scatter(x=ft_mbw.time, y=ft_mbw.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_mbw.add_trace(go.Scatter(x=ft_mbw.time, y=ft_mbw.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_mbw.add_trace(go.Scatter(x=ft_mbw.time, y=ft_mbw.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_mbw.add_trace(go.Scatter(x=ft_mbw.time, y=ft_mbw.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_mbw.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_mbw['location'].unique()[0],title_x=0.44)
fig_mbw.update_xaxes(title_text="time")

fig_mbw.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_mbw.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_mbw, sharing='streamlit',use_container_width=True)''', language="python")

#11111111111111111111---------------------------------------OFFICE ROOM------------------------------------------------------------------1111111111111111111111

st.write('-'*300)
st.markdown("""<style>.big-kit {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-kit">Kitchen</p>', unsafe_allow_html=True)

fig_kit= make_subplots(specs=[[{"secondary_y": True}]])
fig_kit.add_trace(go.Scatter(x=ft_kit.time, y=ft_kit.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_kit.add_trace(go.Scatter(x=ft_kit.time, y=ft_kit.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_kit.add_trace(go.Scatter(x=ft_kit.time, y=ft_kit.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_kit.add_trace(go.Scatter(x=ft_kit.time, y=ft_kit.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_kit.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_kit['location'].unique()[0],title_x=0.44)
fig_kit.update_xaxes(title_text="time")

fig_kit.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_kit.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_kit, sharing='streamlit',use_container_width=True)
with st.beta_expander("code"):
     st.code('''st.markdown("""<style>.big-kit {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-kit">Kitchen</p>', unsafe_allow_html=True)

fig_kit= make_subplots(specs=[[{"secondary_y": True}]])
fig_kit.add_trace(go.Scatter(x=ft_kit.time, y=ft_kit.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_kit.add_trace(go.Scatter(x=ft_kit.time, y=ft_kit.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_kit.add_trace(go.Scatter(x=ft_kit.time, y=ft_kit.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_kit.add_trace(go.Scatter(x=ft_kit.time, y=ft_kit.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_kit.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_kit['location'].unique()[0],title_x=0.44)
fig_kit.update_xaxes(title_text="time")

fig_kit.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_kit.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_kit, sharing='streamlit',use_container_width=True)''', language="python")
#11111111111111111111---------------------------------------OFFICE ROOM------------------------------------------------------------------1111111111111111111111
st.write('-'*300)
st.markdown("""<style>.big-lvr {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-lvr">Living Room</p>', unsafe_allow_html=True)

fig_lvr= make_subplots(specs=[[{"secondary_y": True}]])
fig_lvr.add_trace(go.Scatter(x=ft_lvr.time, y=ft_lvr.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_lvr.add_trace(go.Scatter(x=ft_lvr.time, y=ft_lvr.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_lvr.add_trace(go.Scatter(x=ft_lvr.time, y=ft_lvr.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_lvr.add_trace(go.Scatter(x=ft_lvr.time, y=ft_lvr.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_lvr.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_lvr['location'].unique()[0],title_x=0.44)
fig_lvr.update_xaxes(title_text="time")

fig_lvr.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_lvr.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_lvr, sharing='streamlit',use_container_width=True)
with st.beta_expander("code"):
     st.code('''st.markdown("""<style>.big-lvr {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-lvr">Living Room</p>', unsafe_allow_html=True)

fig_lvr= make_subplots(specs=[[{"secondary_y": True}]])
fig_lvr.add_trace(go.Scatter(x=ft_lvr.time, y=ft_lvr.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_lvr.add_trace(go.Scatter(x=ft_lvr.time, y=ft_lvr.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_lvr.add_trace(go.Scatter(x=ft_lvr.time, y=ft_lvr.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_lvr.add_trace(go.Scatter(x=ft_lvr.time, y=ft_lvr.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_lvr.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_lvr['location'].unique()[0],title_x=0.44)
fig_lvr.update_xaxes(title_text="time")

fig_lvr.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_lvr.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_lvr, sharing='streamlit',use_container_width=True)''', language="python")
#11111111111111111111---------------------------------------OFFICE ROOM------------------------------------------------------------------1111111111111111111111
st.write('-'*300)
st.markdown("""<style>.big-mwr {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-mwr">Main Washroom</p>', unsafe_allow_html=True)

fig_mwr= make_subplots(specs=[[{"secondary_y": True}]])
fig_mwr.add_trace(go.Scatter(x=ft_mwr.time, y=ft_mwr.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_mwr.add_trace(go.Scatter(x=ft_mwr.time, y=ft_mwr.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_mwr.add_trace(go.Scatter(x=ft_mwr.time, y=ft_mwr.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_mwr.add_trace(go.Scatter(x=ft_mwr.time, y=ft_mwr.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_mwr.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_mwr['location'].unique()[0],title_x=0.44)
fig_mwr.update_xaxes(title_text="time")

fig_mwr.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_mwr.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_mwr, sharing='streamlit',use_container_width=True)
with st.beta_expander("code"):
     st.code('''st.markdown("""<style>.big-mwr {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-mwr">Main Washroom</p>', unsafe_allow_html=True)

fig_mwr= make_subplots(specs=[[{"secondary_y": True}]])
fig_mwr.add_trace(go.Scatter(x=ft_mwr.time, y=ft_mwr.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_mwr.add_trace(go.Scatter(x=ft_mwr.time, y=ft_mwr.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_mwr.add_trace(go.Scatter(x=ft_mwr.time, y=ft_mwr.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_mwr.add_trace(go.Scatter(x=ft_mwr.time, y=ft_mwr.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_mwr.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_mwr['location'].unique()[0],title_x=0.44)
fig_mwr.update_xaxes(title_text="time")

fig_mwr.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_mwr.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_mwr, sharing='streamlit',use_container_width=True)''', language="python")
#11111111111111111111---------------------------------------OFFICE ROOM------------------------------------------------------------------1111111111111111111111
st.write('-'*300)
st.markdown("""<style>.big-lrm {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-lrm">Laundry Room</p>', unsafe_allow_html=True)

fig_lrm= make_subplots(specs=[[{"secondary_y": True}]])
fig_lrm.add_trace(go.Scatter(x=ft_lrm.time, y=ft_lrm.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_lrm.add_trace(go.Scatter(x=ft_lrm.time, y=ft_lrm.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_lrm.add_trace(go.Scatter(x=ft_lrm.time, y=ft_lrm.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_lrm.add_trace(go.Scatter(x=ft_lrm.time, y=ft_lrm.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_lrm.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_lrm['location'].unique()[0],title_x=0.44)
fig_lrm.update_xaxes(title_text="time")

fig_lrm.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_lrm.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_lrm, sharing='streamlit',use_container_width=True)
with st.beta_expander("code"):
     st.code('''st.markdown("""<style>.big-lrm {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-lrm">Laundry Room</p>', unsafe_allow_html=True)

fig_lrm= make_subplots(specs=[[{"secondary_y": True}]])
fig_lrm.add_trace(go.Scatter(x=ft_lrm.time, y=ft_lrm.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_lrm.add_trace(go.Scatter(x=ft_lrm.time, y=ft_lrm.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_lrm.add_trace(go.Scatter(x=ft_lrm.time, y=ft_lrm.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_lrm.add_trace(go.Scatter(x=ft_lrm.time, y=ft_lrm.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_lrm.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_lrm['location'].unique()[0],title_x=0.44)
fig_lrm.update_xaxes(title_text="time")

fig_lrm.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_lrm.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_lrm, sharing='streamlit',use_container_width=True)''', language="python")

#11111111111111111111---------------------------------------OFFICE ROOM------------------------------------------------------------------1111111111111111111111
st.write('-'*300)
st.markdown("""<style>.big-mbe {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-mbe">Master Bedroom Ensuite</p>', unsafe_allow_html=True)

fig_mbe= make_subplots(specs=[[{"secondary_y": True}]])
fig_mbe.add_trace(go.Scatter(x=ft_mbe.time, y=ft_mbe.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_mbe.add_trace(go.Scatter(x=ft_mbe.time, y=ft_mbe.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_mbe.add_trace(go.Scatter(x=ft_mbe.time, y=ft_mbe.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_mbe.add_trace(go.Scatter(x=ft_mbe.time, y=ft_mbe.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_mbe.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_mbe['location'].unique()[0],title_x=0.44)
fig_mbe.update_xaxes(title_text="time")

fig_mbe.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_mbe.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_mbe, sharing='streamlit',use_container_width=True)
with st.beta_expander("code"):
     st.code('''st.markdown("""<style>.big-mbe {font-size:30px !important;text-align:center;text-decoration: underline;font-family: fantasy;background-color:#31333F;color:white}</style>""", unsafe_allow_html=True)
st.markdown('<p class="big-mbe">Master Bedroom Ensuite</p>', unsafe_allow_html=True)

fig_mbe= make_subplots(specs=[[{"secondary_y": True}]])
fig_mbe.add_trace(go.Scatter(x=ft_mbe.time, y=ft_mbe.obj_temp,
                             mode='markers',name='Temperature',marker=dict(color='#FF1D00',size=2),
         					 connectgaps=False),secondary_y=False)
fig_mbe.add_trace(go.Scatter(x=ft_mbe.time, y=ft_mbe.humid,
                             mode='markers',name='Humidity',marker=dict(color='#136EFF',size=2),
                             connectgaps=False),secondary_y=True)
fig_mbe.add_trace(go.Scatter(x=ft_mbe.time, y=ft_mbe.obj_temp,hoverinfo='skip',
                             mode='lines',line=dict(color="#FF1D00",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=False)
fig_mbe.add_trace(go.Scatter(x=ft_mbe.time, y=ft_mbe.humid,hoverinfo='skip',
                             mode='lines',line=dict(color="#136EFF",width=.5,dash='dash'),
                             line_shape='spline',line_smoothing=1.3,connectgaps=True),secondary_y=True)

fig_mbe.update_layout(showlegend=False,hovermode="x",title_font_family='Droid Serif',template='simple_white',title_text=ft_mbe['location'].unique()[0],title_x=0.44)
fig_mbe.update_xaxes(title_text="time")

fig_mbe.update_yaxes(title_text="Temperature", secondary_y=False,range=[14,27])
fig_mbe.update_yaxes(title_text="Humidity", secondary_y=True,range=[16,57])

st.plotly_chart(fig_mbe, sharing='streamlit',use_container_width=True)''', language="python")
