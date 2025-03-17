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




class RPAStart:



    def __init__(self, section, n_news):
        self.section = section
        self.n_news = n_news
        self.clusters_urls = self.get_clusters()
        self.save_started_news()



    def get_section_url(self):
        if self.section == 'Mundo':
            return 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
        elif self.section == 'Brasil':
            return 'https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNREUxWm5JU0JYQjBMVUpTS0FBUAE?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
        elif self.section == 'CeT':
            return 'https://news.google.com/topics/CAAqLAgKIiZDQkFTRmdvSkwyMHZNR1ptZHpWbUVnVndkQzFDVWhvQ1FsSW9BQVAB?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
        elif self.section == 'Economia':
            return 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
        elif self.section == 'Entretenimento':
            return 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNREpxYW5RU0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
        elif self.section == 'Esporte':
            return 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JYQjBMVUpTR2dKQ1VpZ0FQAQ/sections/CAQiS0NCQVNNZ29JTDIwdk1EWnVkR29TQlhCMExVSlNHZ0pDVWlJT0NBUWFDZ29JTDIwdk1ESjJlRFFxQ3dvSkVnZEdkWFJsWW05c0tBQSouCAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JYQjBMVUpTR2dKQ1VpZ0FQAVAB?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
        return 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'



    def get_clusters(self):
        # Buscar URL e conteúdo da página principal
        section_url =  self.get_section_url()
        browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
        html_content = requests.get(section_url, headers=browsers, timeout=20)
        soup = BeautifulSoup(html_content.text, 'html.parser')
        news_blocks = soup.find_all('a')
        time.sleep(5)
            
        # Identificar clusters de notícias
        result = []
        for nb in news_blocks:
            try:
                if nb.get('aria-label') == "Cobertura completa":
                    cluster_url = 'https://news.google.com' + nb.get('href')[1:]
                    result.append(cluster_url)
            except:
                print('Erro ao buscar páginas de notícias')
        
        return result



    def get_reference_news_data(self, srcUrl):
        reference_news_urls = []
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        try:
            driver.get(srcUrl)
            WebDriverWait(driver, 15) # Aguardar até 15 segundos
            articles = driver.find_elements(By.CSS_SELECTOR, "article")
            
            n_articles = len(articles)
            curr_article = 0
            n_articles_got = 0
            
            # Buscar pelas notícias (limitado a 20)
            while n_articles_got < 20 and curr_article < n_articles:
                a = articles[curr_article]
                try:
                    title = a.find_element(By.CSS_SELECTOR, "h4").text
                    share_btn = a.find_element(By.CSS_SELECTOR, '[data-tooltip="Compartilhar"]')
                    share_btn.click()
                    copy_link_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Copiar link"]')))
                    copy_link_btn.click()
                    close_dialog_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Fechar caixa de diálogo"]')))
                    close_dialog_btn.click()
                    url = pyperclip.paste()
                    reference_news_urls.append({'title': title, 'url': url})
                    n_articles_got += 1
                except:
                    pass
                curr_article += 1
            
        except Exception as e:
            print(f'Problema na coleta dos dados da página {srcUrl} >> ', e)
        driver.quit()
        
        return reference_news_urls



    def save_started_news(self):
        counter = 0
        for cluster_url in self.clusters_urls:
            try:
                reference_news = self.get_reference_news_data(cluster_url)
                url = f'{st.secrets['API_URL']}api/news'
                payload = {
                    "uid": st.secrets['SUPPORT_UID'],
                    "supportUid": st.secrets['SUPPORT_UID'],
                    "referenceNews": reference_news,
                    "sectionName": self.section
                }
                response = requests.post(url, json=payload)
                if response.status_code != 200:
                    print(f'Erro: {response.status_code}')
                counter += 1
                if counter >= self.n_news:
                    break
            except Exception as e:
                print("Problema ao salvar notícia:", e)





