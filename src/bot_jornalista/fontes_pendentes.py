import time
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from bot_jornalista.writer_news import WriterNews
from sources.google_news import GoogleNews, GoogleNewsCluster
from streamlit_image_select import image_select
import re



def fontes_pendentes():
    file_src = 'src/admin/bot_jornalista/not_found_url_reader.csv'
    
    src_df = pd.read_csv(file_src)
    src_df['ts'] = pd.to_datetime(src_df['ts'])
    src_df['date'] = src_df['ts'].dt.date
    src_df['src'] = src_df['url'].str.split('/').str[2]
    chart_df = src_df.groupby('src').size().reset_index(name='count')
    
    chart_df.sort_values('count', ascending=False, inplace=True)
    st.dataframe(chart_df)
    chart_df.index = range(len(chart_df))
    st.write(chart_df)
    chart_df2 = pd.DataFrame(chart_df)
    
    
    
    
    st.bar_chart(data=chart_df2, x='src', y='count', x_label='Fonte dos dados', y_label='# ocorrências', horizontal=True, stack=False)

if __name__ == '__main__':
    fontes_pendentes()


