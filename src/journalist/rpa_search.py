import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from sources.news import News
import time
import streamlit as st

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import pyperclip



# 1. Buscar uma notícia com status "started"
# 2. Buscar todos os dados para cada uma as notícias de referência
# 3. Salvar notícia com status "searched"


class RPASearch:



    def __init__(self):
        self.reference_news = ['']
        
        while len(self.reference_news) > 0:
            try:
                news = self.get_started_news()
                news_id = news['newsId']
                self.reference_news = news['referenceNews']
                newRef = []
                for ref in self.reference_news:
                    news_data = News(ref['url'])
                    newRef.append({
                        'url': ref['url'] if ref['url'] != None else 'N/A',
                        'title': ref['title'] if ref['title'] != None else 'N/A',
                        'summary': '',
                        'text': news_data.text if news_data.text != None and len(news_data.text) < 2048 else 'N/A',
                        'imageUrl': news_data.imageUrl if news_data.imageUrl != None else 'N/A',
                        'imageText': news_data.imageText if news_data.imageText != None else 'N/A'
                    })
                self.reference_news = newRef
                self.save_searched_news(news_id)
            except Exception as e:
                print("Problema no RPASearch:", e)
                self.reference_news = []



    def get_started_news(self):
        try:
            url = f'https://api-prod.jornalsocrates.com.br/api/startednews'
            payload = {
                "uid": 'jvfbEGdoKJYokMi4FgA3AFMI4tO2',
                "supportUid": 'jvfbEGdoKJYokMi4FgA3AFMI4tO2'
            }
            response = requests.get(url, json=payload)
            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
            return response.json()
        except Exception as e:
            print("Problema ao buscar notícia:", e)



    def save_searched_news(self, newsId):
        try:
            url = f'https://api-prod.jornalsocrates.com.br/api/news/{newsId}'
            payload = {
                "uid": 'jvfbEGdoKJYokMi4FgA3AFMI4tO2',
                "supportUid": 'jvfbEGdoKJYokMi4FgA3AFMI4tO2',
                "referenceNews": self.reference_news,
                "__t": "searched"
            }
            response = requests.patch(url, json=payload)
            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
                print(response.json())
            return response
        except Exception as e:
            print("Problema ao salvar notícia em save_searched_news:", e)







# class RPASearch:
#     def __init__(self):
#         self.reference_news = self.get_reference_news()
        
#     # Buscar notícias ainda não enriquecidas no banco de dados
#     def get_reference_news(self):
#         # Código principal
#         result_example = [
#             {
#                 'url': 'http://g1.globo.com/mundo/noticia/2025/06/14/negociacoes-nucleares-entre-eua-e-ira-sao-canceladas-diz-oma.ghtml',
#                 'title': 'Negociações nucleares entre EUA e Irã são canceladas após ofensiva de Israel',
#                 'summary': 'Anúncio foi feito pelo chanceler de Omã, país que atua como mediador entre Washington e Teerã nas conversas sobre o programa nuclear iraniano.',
#                 'text': 'Texto da matéria jornalística',
#                 'imageUrl': 'https://s2-g1.glbimg.com/s8zhA4beq2ZUbIrb8pnIVOyRSs8=/0x0:6000x4000/1000x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2025/n/Z/0vMYJ9TCyNmLHPuEVA1g/000-629b9tx.jpg',
#                 'imageText': 'Pessoas e socorristas se reúnem em frente a um prédio atingido por um ataque israelense em Teerã — Foto: MEGHDAD MADADI / TASNIM NEWS / AFP'
#             }]
#         return result_example

#     # Buscar notícias ainda não enriquecidas no banco de dados
#     def get_started_news(self):
#         # Código principal
#         result_example = [
#             'http://g1.globo.com/mundo/noticia/2025/06/14/negociacoes-nucleares-entre-eua-e-ira-sao-canceladas-diz-oma.ghtml',
#             'https://noticias.uol.com.br/internacional/ultimas-noticias/2025/06/14/israel-ira-ataques-guerra-bombardeio-o-que-se-sabe.htm',
#             'https://www.cnnbrasil.com.br/internacional/video-antes-e-depois-de-instalacoes-nucleares-do-ira-destruidas-por-israel/',
#             'https://g1.globo.com/mundo/noticia/2025/06/14/ira-e-israel-ja-foram-amigos-e-se-ajudaram-no-passado-saiba-por-que-a-relacao-implodiu.ghtml',
#             'https://www.bbc.com/portuguese/articles/cqxe57nl8d2o'
#             ]
#         return result_example

#     # Salvar notícias enriquecidas em banco de dados dedicado
#     def save_searched_news(self, newsId):
#         # Código principal
#         result_example = {'status': 200, 'message': 'The news item has been successfully saved'}
#         return result_example











