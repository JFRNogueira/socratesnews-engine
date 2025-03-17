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
                        'text': news_data.text if news_data.text != None else 'N/A',
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
            url = f'{st.secrets['API_URL']}api/startednews'
            payload = {
                "uid": st.secrets['SUPPORT_UID'],
                "supportUid": st.secrets['SUPPORT_UID']
            }
            response = requests.get(url, json=payload)
            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
            return response.json()
        except Exception as e:
            print("Problema ao buscar notícia:", e)



    def save_searched_news(self, newsId):
        try:
            url = f'{st.secrets['API_URL']}api/news/{newsId}'
            payload = {
                "uid": st.secrets['SUPPORT_UID'],
                "supportUid": st.secrets['SUPPORT_UID'],
                "referenceNews": self.reference_news,
                "__t": "searched"
            }
            response = requests.patch(url, json=payload)
            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
            return response
        except Exception as e:
            print("Problema ao salvar notícia em save_searched_news:", e)



