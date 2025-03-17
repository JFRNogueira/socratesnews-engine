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

from youtube_transcript_api import YouTubeTranscriptApi

# Etapas
# 1. Identificar a URL da seção
# 2. Identificar a URL do cluster de notícias
# 3. Itentificar as URLs das notícias
# 4. Salvar como notícia inicial
# 5. Buscar os dados das notícias
# 6. Salvar como notícia pesquisada
# 7. Criar notícia completa
# 8. Salvar como notícia completa



class YTUI:
    
    
    
    def __init__(self):
        pass
    
    def get_video_code(self, url):
        result = url.split('v=')[1]
        result = result.split('&')[0]
        st.text(result)
        st.session_state['yt_video_code'] = result
        return result
    
    def get_video_transcript(self, url):
        video_code = self.get_video_code(url)
        result = YouTubeTranscriptApi.get_transcript(video_code, languages=['pt'])
        st.session_state['yt_video_transcript'] = result
        return result
    
    def get_transcript_text(self, url):
        transcript = self.get_video_transcript(url)
        text = ''
        for t in transcript:
            text += t['text'] + ' '
        st.session_state['yt_video_transcript_text'] = text
        return text
    
    
    
    
    def ui(self):
        st.header('YouTube')
        
        col1, col2, col3 = st.columns(3, gap='large')
        
        with col1:
            st.subheader('Parâmetros', divider=True)
            
            st.text_input('URL do vídeo', value='https://www.youtube.com/watch?v=Q3NqpREvNJw&ab_channel=g1', key='yt_video_url')
            if st.button('Transcrever com YT', type='primary'):
                self.get_transcript_text(st.session_state['yt_video_url'])
            st.markdown(st.session_state.get('yt_video_transcript_text', ''))
        
            
            
        with col2:
            st.subheader('Notícia proposta', divider=True)
            if st.button('Gerar notícia', type='primary'):
                pass
            st.subheader("Título da notícia")
            st.markdown('Aqui vai o preâmbulo da notícia')
            st.markdown('Aqui vai o texto da notícia')
            
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
                


