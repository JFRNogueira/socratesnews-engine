import requests
# from bs4 import BeautifulSoup
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


class GoogleNews:

    def __init__(self, sections):
        self.sections = sections
        # self.get_themes()



#     def get_google_news_url(self, section):
#         if section == 'Mundo':
#             return 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
#         elif section == 'Brasil':    
#             return 'https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNREUxWm5JU0JYQjBMVUpTS0FBUAE?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
#         elif section == 'C&T':
#             return 'https://news.google.com/topics/CAAqLAgKIiZDQkFTRmdvSkwyMHZNR1ptZHpWbUVnVndkQzFDVWhvQ1FsSW9BQVAB?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
#         elif section == 'Economia':
#             return 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
#         elif section == 'Entretenimento':
#             return 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNREpxYW5RU0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
#         elif section == 'Esporte':
#             return 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JYQjBMVUpTR2dKQ1VpZ0FQAQ/sections/CAQiS0NCQVNNZ29JTDIwdk1EWnVkR29TQlhCMExVSlNHZ0pDVWlJT0NBUWFDZ29JTDIwdk1ESjJlRFFxQ3dvSkVnZEdkWFJsWW05c0tBQSouCAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JYQjBMVUpTR2dKQ1VpZ0FQAVAB?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
#         return 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'



#     def get_themes(self):
#         for section in self.sections:
#             # Buscar URL e conteúdo da página principal
#             google_news_url =  self.get_google_news_url(section)
#             browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
#             html_content = requests.get(google_news_url, headers=browsers, timeout=20)
#             soup = BeautifulSoup(html_content.text, 'html.parser')
#             news_blocks = soup.find_all('a')
#             time.sleep(5)
            
#             # Identificar URLs dos clusters
#             result = []
#             for nb in news_blocks:
#                 try:
#                     if nb.get('aria-label') == "Cobertura completa":
#                         all_news = 'https://news.google.com' + nb.get('href')[1:]
#                         result.append({'url': all_news})
#                 except:
#                     print('Erro ao buscar páginas de notícias')
            
#             # Adicionar nome do cluster
#             for r in result:
#                 news = requests.get(r['url'], headers=browsers, timeout=20)
#                 soup = BeautifulSoup(news.text, 'html.parser')
#                 try:
#                     title = soup.find('h1').getText()
#                 except:
#                     title = 'N/A'
#                 r['title'] = title if len(title) >= 3 else 'N/A'
            
#             # Salvar os dados na sessão
#             result = pd.DataFrame(result)
#             result['create'] = False
#             result = result[['create', 'title', 'url']]
#             st.session_state[f'{section.lower()}_themes'] = result





# class GoogleNewsCluster:
    
#     def __init__(self, sections):
#         self.sections = sections
#         self.text = ''
#         self.title = ''
#         self.summary = ''
#         self.imageUrl = ''
#         self.imageText = ''



#     def get_selected_themes_df(self, section):
#         return st.session_state[f'{section.lower()}_themes_selection']


#     def get_all_references(self):
#         for section in self.sections:
#             selected_themes = self.get_selected_themes_df(section)
#             counter = 1
#             for index, t in selected_themes.iterrows():
#                 if t['create']:
#                     all_news, reference_news, reference_images = self.get_reference_news(t['url'])
#                     print(reference_news)
                    
#                     reference_news['n_words'] = reference_news['text'].apply(lambda x: len(x.split()))
#                     reference_news = reference_news.sort_values(by='n_words', ascending=False)
#                     reference_news['acc'] = reference_news['n_words'].cumsum()
#                     reference_news['source'] = reference_news['acc'] <= 3000
#                     reference_news = reference_news[['source', 'n_words', 'acc', 'url', 'title', 'text']]
                    
#                     st.session_state[f'{section.lower()}_news_{counter}_all_news'] = all_news
#                     st.session_state[f'{section.lower()}_news_{counter}_reference_news'] = reference_news
#                     st.session_state[f'{section.lower()}_news_{counter}_reference_images'] = reference_images
#                     counter += 1
                
                
                
                
#     def get_reference_news(self, srcUrl):
#         reference_news = []
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#         try:
#             driver.get(srcUrl)
#             WebDriverWait(driver, 15) # Aguardar até 15 segundos
#             articles = driver.find_elements(By.CSS_SELECTOR, "article")
            
#             n_articles = len(articles)
#             curr_article = 0
#             n_articles_got = 0
            
#             # Buscar pelas notícias (limitado a 20)
#             while n_articles_got < 20 and curr_article < n_articles:
#                 a = articles[curr_article]
#                 try:
#                     title = a.find_element(By.CSS_SELECTOR, "h4").text
#                     share_btn = a.find_element(By.CSS_SELECTOR, '[data-tooltip="Compartilhar"]')
#                     share_btn.click()
#                     copy_link_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Copiar link"]')))
#                     copy_link_btn.click()
#                     close_dialog_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Fechar caixa de diálogo"]')))
#                     close_dialog_btn.click()
#                     url = pyperclip.paste()
#                     reference_news.append({'title': title, 'url': url})
#                     n_articles_got += 1
#                 except:
#                     pass
#                 curr_article += 1
            
#         except Exception as e:
#             print(f'Problema na coleta dos dados da página {srcUrl} >> ', e)
#         driver.quit()
        
#         all_news = []
#         all_news_aux = []
#         for r in reference_news:
#             news_data = News(r['url'])
#             all_news_aux.append(news_data)
#         for r in all_news_aux:
#             all_news.append({'url': r.url, 'title': r.title, 'text': r.text, 'imageUrl': r.imageUrl, 'imageText': r.imageText})
        
#         reference_news = []
#         reference_news_aux = [news for news in all_news_aux if (news.title != None) and (news.text != None)]
#         for r in reference_news_aux:
#             reference_news.append({'url': r.url, 'title': r.title, 'text': r.text, 'imageUrl': r.imageUrl, 'imageText': r.imageText})
        
#         reference_images = []
#         reference_images_aux = [news for news in all_news_aux if (news.imageUrl != None) or (news.imageText != None)]
#         for r in reference_images_aux:
#             reference_images.append({'url': r.url, 'title': r.title, 'text': r.text, 'imageUrl': r.imageUrl, 'imageText': r.imageText})
        
#         return pd.DataFrame(all_news), pd.DataFrame(reference_news), pd.DataFrame(reference_images)



    