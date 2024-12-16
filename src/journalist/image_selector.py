import time
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from journalist.google_news_ui import GoogleNewsUi
from journalist.writer_news import WriterNews
from sources.google_news import GoogleNews, GoogleNewsCluster
from streamlit_image_select import image_select
from streamlit_image_select import image_select



class ImageSelector:
    
    
    
    def __init__(self):
        pass
    
    
    
    def get_no_image_news(self):
        try:
            url = f'{st.secrets['API_URL']}api/noimagenews'
            payload = {
                "uid": st.secrets['SUPPORT_UID'],
                "supportUid": st.secrets['SUPPORT_UID'],
            }
            response = requests.get(url, json=payload)
            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
                return None
            return response.json()

        except Exception as e:
            print("Problema ao salvar notícia:", e)
    
    
    
    def ui(self):
        st.header('Seletor de imagens')
        
        col1, col2 = st.columns([1, 3], gap='large')
        
        with col1:
            st.subheader('Google News', divider=True)
            
            if st.button('Buscar notícias'):
                st.session_state['no_image_news'] = self.get_no_image_news()
                st.json(st.session_state.get('no_image_news', {}))
 
        with col2:
            st.subheader('Selecionar imagem', divider=True)
            
            col21, col22 = st.columns(2)
            
            with col21:
                st.text_input('Fonte da imagem', key='image_source')
            with col22:
                st.file_uploader('Upload de imagem', key='image_upload')
            
            st.session_state['image_source_df'] = pd.DataFrame(st.session_state.get('no_image_news', {}).get('referenceNews', []))
            st.dataframe(st.session_state['image_source_df'])
            
                
            # st.json(
            #     [x['imageUrl'] for x in st.session_state.get('no_image_news', {}).get('referenceNews', [])]
            # )
            
            
            
            
            
            
            