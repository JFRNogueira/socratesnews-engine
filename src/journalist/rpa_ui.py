import time
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from journalist.google_news_ui import GoogleNewsUi
from journalist.prayer import Prayer
from journalist.rpa_search import RPASearch
from journalist.rpa_starter import RPAStart
from journalist.rpa_writer import RPAWriter
from journalist.writer_news import WriterNews
from sources.google_news import GoogleNews, GoogleNewsCluster
from streamlit_image_select import image_select

# Etapas
# 1. Identificar a URL da seção
# 2. Identificar a URL do cluster de notícias
# 3. Itentificar as URLs das notícias
# 4. Salvar como notícia inicial
# 5. Buscar os dados das notícias
# 6. Salvar como notícia pesquisada
# 7. Criar notícia completa
# 8. Salvar como notícia completa



class RPANews:
    
    
    
    def __init__(self):
        pass
    
    
    
    def ui(self):
        st.header('Robô Escritor')
        
        col1, col2, col3 = st.columns(3, gap='large')
        
        with col1:
            st.subheader('Google News', divider=True)
            
            list_sections = [
                {"sectionName": 'Mundo', "sectionkey": 'rpa_counter_mundo'},
                {"sectionName": 'Brasil',"sectionkey": 'rpa_counter_brasil'},
                {"sectionName": 'CeT',"sectionkey": 'rpa_counter_cet'},
                {"sectionName": 'Economia',"sectionkey": 'rpa_counter_economia'},
                {"sectionName": 'Entretenimento',"sectionkey": 'rpa_counter_entretenimento'},
                {"sectionName": 'Esporte',"sectionkey": 'rpa_counter_esporte'}
                ]
            
            for l in list_sections:
                st.slider(l['sectionName'], 0, 10, 4, key=l['sectionkey'])
            
            st.slider('Cidades primárias', 0, 10, 4, key='rpa_counter_cidades_primarias')
            st.slider('Cidades secundárias', 0, 10, 2, key='rpa_counter_cidades_secundarias')
            st.slider('Cidades terciárias', 0, 10, 1, key='rpa_counter_cidades_terciarias')
            
        with col2:
            st.subheader('Seções secundárias', divider=True)
            st.checkbox('Oração', value=True, key='rpa_oracao_checker')
            st.checkbox('Infantil', value=True)
            st.checkbox('Horóscopo', value=True)
            st.checkbox('Previsão do tempo', value=True)
            st.subheader('Classificados', divider=True)
            st.checkbox('Veículos', value=True)
            st.checkbox('Concursos', value=True)
            st.checkbox('Licitações', value=True)
            
        with col3:
            st.subheader('Acompanhamento', divider=True)
            
            if st.button('Iniciar'):
                for l in list_sections:
                    if st.session_state.get(l['sectionkey'], 0) > 0:
                        RPAStart(l['sectionName'], st.session_state.get(l['sectionkey'], 0))
            if st.button('Pesquisar'):
                RPASearch()
            if st.button('Finalizar'):
                should_continue = True
                while should_continue:
                    try:
                        RPAWriter()
                    except Exception as e:
                        print('Erro ao criar notícia:', e)
                        should_continue = False
            if st.button('Escrever tudo'):
                for l in list_sections:
                    if st.session_state.get(l['sectionkey'], 0) > 0:
                        RPAStart(l['sectionName'], st.session_state.get(l['sectionkey'], 0))
                RPASearch()
                should_continue = True
                while should_continue:
                    try:
                        RPAWriter()
                    except Exception as e:
                        print('Erro ao criar notícia:', e)
                        should_continue = False
                


