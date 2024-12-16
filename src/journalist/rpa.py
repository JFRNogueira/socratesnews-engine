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
    
    
    
    def create_news_from_google(self, sectionName):
        if st.session_state.get(f'rpa_counter_{sectionName.lower()}', 0) > 0:
            GoogleNews([sectionName])
            GoogleNewsUi(sectionName).render_editor(n_news=st.session_state.get(f'rpa_counter_{sectionName.lower()}', 0))
            GoogleNewsCluster([sectionName]).get_all_references()
            
            for i in range(1, st.session_state.get(f'rpa_counter_{sectionName.lower()}', 0)+1):
                st.session_state[f'{sectionName.lower()}_news_{i}_reference_news_selected'] = GoogleNewsUi(sectionName).create_referente_news_df(i)
                selection = st.session_state[f'{sectionName.lower()}_news_{i}_reference_news_selected']
                st.session_state[f'{sectionName.lower()}_news_{i}_final'] = WriterNews(sectionName, 
                    selection[selection['source'] == True]['text'].tolist(),
                    selection[selection['source'] == True]['title'].tolist(),
                    st.session_state.get(f'{sectionName.lower()}_news_{i}_image_url',''),
                    st.session_state.get(f'{sectionName.lower()}_news_{i}_image_text',''),
                    st.session_state[f'{sectionName.lower()}_news_{i}_all_news'].to_dict(orient='records')
                    )

    
    
    
    def ui(self):
        st.header('Robô Escritor')
        
        col1, col2, col3 = st.columns(3, gap='large')
        
        with col1:
            st.subheader('Google News', divider=True)
            
            list_sections = [{"sectionName": 'Mundo', "sectionkey": 'rpa_counter_mundo'},
                {"sectionName": 'Brasil',"sectionkey": 'rpa_counter_brasil'},
                {"sectionName": 'CeT',"sectionkey": 'rpa_counter_cet'},
                {"sectionName": 'Economia',"sectionkey": 'rpa_counter_economia'},
                {"sectionName": 'Entretenimento',"sectionkey": 'rpa_counter_entretenimento'},
                {"sectionName": 'Esporte',"sectionkey": 'rpa_counter_esporte'}]
            
            for l in list_sections:
                st.slider(l['sectionName'], 0, 10, 4, key=l['sectionkey'])
            
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
                for l in list_sections:
                    self.create_news_from_google(l['sectionName'])
                
            # st.progress(0.5, 'Notícias gerais')
            # st.progress(0.5, 'Cidades primárias')
            # st.progress(0.5, 'Cidades secundárias')
            # st.progress(0.5, 'Cidades terciárias')
            # st.progress(0.5, 'Seções secundárias')
            # st.progress(0.5, 'Classificados')

            
        


