import time
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from journalist.google_news_ui import GoogleNewsUi
from journalist.writer_news import WriterNews
from sources.google_news import GoogleNews, GoogleNewsCluster
from streamlit_image_select import image_select



class RPAWriter:
    
    
    
    def __init__(self):
        pass
    
    
    
    def ui(self):
        st.header('Robô Escritor')
        
        col1, col2, col3, col4 = st.columns(4, gap='large')
        
        with col1:
            st.subheader('Google News', divider=True)
            st.slider('Mundo', 0, 10, 4, key='rpa_counter_mundo')
            st.slider('Brasil', 0, 10, 4, key='rpa_counter_brasil')
            st.slider('C&T', 0, 10, 4, key='rpa_counter_cet')
            st.slider('Economia', 0, 10, 4, key='rpa_counter_economia')
            st.slider('Entretenimento', 0, 10, 4, key='rpa_counter_entretenimento')
            st.slider('Esporte', 0, 10, 4, key='rpa_counter_esporte')
            st.slider('Cidades primárias', 0, 10, 4, key='rpa_counter_cidades_primarias')
            st.slider('Cidades secundárias', 0, 10, 2, key='rpa_counter_cidades_secundarias')
            st.slider('Cidades terciárias', 0, 10, 1, key='rpa_counter_cidades_terciarias')
            
        with col2:
            st.subheader('Seções secundárias', divider=True)
            st.checkbox('Oração', value=True)
            st.checkbox('Infantil', value=True)
            st.checkbox('Horóscopo', value=True)
            st.checkbox('Previsão do tempo', value=True)
            st.subheader('Classificados', divider=True)
            st.checkbox('Veículos', value=True)
            st.checkbox('Concursos', value=True)
            st.checkbox('Licitações', value=True)
            
        with col3:
            st.subheader('Acompanhamento', divider=True)
            if st.button('Escrever'):
                
                if st.session_state.get("rpa_counter_mundo", 0) > 0:
                    GoogleNews(['Mundo'])
                    GoogleNewsUi('Mundo').render_editor(n_news=st.session_state.get("rpa_counter_mundo", 0))
                    GoogleNewsCluster(['Mundo']).get_all_references()
            # if st.button('Marcar'):
            #     GoogleNews(['Mundo'])
                
            st.progress(0.5, 'Notícias gerais')
            st.progress(0.5, 'Cidades primárias')
            st.progress(0.5, 'Cidades secundárias')
            st.progress(0.5, 'Cidades terciárias')
            st.progress(0.5, 'Seções secundárias')
            st.progress(0.5, 'Classificados')

            
        


