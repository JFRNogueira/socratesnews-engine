import requests
import openai
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import time

import ipywidgets as widgets
from IPython.display import display, Image, clear_output

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import pyperclip

%run "./news_source/news.ipynb" import News


load_dotenv()
API_URL = os.getenv("API_URL")
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))


class GoogleNews:

    def __init__(self, srcUrl, sectionName):
        self.srcUrl = srcUrl
        self.sectionName = sectionName
        self.allRererenceNews, self.referenceNews, self.referenceImages = self.get_reference_news()
        self.text = self.create_news_text()
        self.title = self.create_news_title()
        self.summary = self.create_news_summary()
        self.imageUrl = ''
        self.imageText = ''
        
        
        
    def get_reference_news(self):
        reference_news = []
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        try:
            driver.get(self.srcUrl)
            WebDriverWait(driver, 15)
            articles = driver.find_elements(By.CSS_SELECTOR, "article")
            
            n_articles = len(articles)
            curr_article = 0
            n_articles_got = 0
            while n_articles_got < 10 and curr_article < n_articles:
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
                    reference_news.append({'title': title, 'url': url})
                    n_articles_got += 1
                except:
                    pass
                curr_article += 1
            
        except Exception as e:
            print(f'Problema na coleta dos dados da página {self.srcUrl} >> ', e)
        driver.quit()

        all_news = []
        for r in reference_news:
            news_data = News(r['url'])
            all_news.append(news_data)
        
        referenceNews = [news for news in all_news if (news.title != None) and (news.text != None)]
        referenceImages = [news for news in all_news if (news.imageUrl != None) or (news.imageText != None)]
        return all_news, referenceNews, referenceImages



    def create_news_text(self):
        
        references = '\n\n'
        for n in self.referenceNews:
            references += f'{n.title}\n{n.text}\n\n'
        
        content = f'Escreva um texto jornalístico que será publicado na seção "{self.sectionName}" de um jornal de grande circulação.\n'
        content += f'Considere como referêcia exclusivamente o que foi extraído de alguns sites de prestígio:{references}'
        content += f'Crie o texto sem enrolação e apenas com informações relevantes. Escreva estritamente a notícia a ser publicada, sem necessidade de dar um título (manchete) ao texto.\n\n'
        content += f'O texto da notícia deve possui obrigatoriamente entre 700 e 800 palavras.\n'
        content += f'Se a quantidade de palavras não estiver de acordo com o solicitado, ajuste o campo para atender ao requisito antes de finalizar a resposta.\n'
        content += f'Reforço que deve ser apenas o texto, não incluindo manchete, autor preâmbulo ou qualquer coisa diferente do corpo da notícia.\n'

        message = [{
            'role': 'user',
            'content': content
        }]

        response = client.chat.completions.create(
            messages=message, 
            model="gpt-4o-mini", 
            max_tokens=10000, 
            temperature=0, 
        )
        news_text = response.choices[0].message.content

        return news_text



    def create_news_title(self):
        
        try:        
            references = '\n\n'
            for n in self.referenceNews:
                references += f'{n.title}\n'
            
            content = f'Escreva um preâmbulo para o texto jornalístico abaixo, que será publicado na seção "{self.sectionName}" de um jornal de grande circulação.\n\n'
            content += f'{self.text}\n\n'
            content += f'Pode considerar como referência de bons títulos a lista a seguir, extraída de jornais de prestígio:\n{references}\n\n\n'
            content += f'Escreva apenas o título da matéria, que deve conter entre 70 e 100 caracteres.\n'
            content += f'Reforço que deve ser apenas o título, não incluindo texto, autor, preâmbulo ou qualquer coisa diferente do título da notícia.\n'
            content += f'Se a quantidade de caracteres não estiver de acordo com o solicitado, ajuste o campo para atender ao requisito antes de finalizar a resposta.'

            message = [{
                'role': 'user',
                'content': content
            }]

            response = client.chat.completions.create(
                messages=message, 
                model="gpt-4o-mini", 
                max_tokens=10000, 
                temperature=0, 
            )
            news_title = response.choices[0].message.content

            return news_title
        except Exception as e:
            print(f'Erro em create_news_title: {e}')
            return 'N/A'



    def create_news_summary(self):
        try:
            references = '\n\n'
            for n in self.referenceNews:
                references += f'{n.title}\n'
            
            content = f'Escreva um título para o texto jornalístico abaixo, que será publicado na seção "{self.sectionName}" de um jornal de grande circulação.\n\n'
            content += f'{self.text}\n\n'
            content += f'Escreva apenas o preâmbulo da matéria, que deve conter entre 190 e 220 caracteres.\n'
            content += f'Reforço que deve ser apenas o preâmbulo, não incluindo texto, autor, título ou qualquer coisa diferente do preâmbulo da notícia.\n'
            content += f'Se a quantidade de caracteres não estiver de acordo com o solicitado, ajuste o campo para atender ao requisito antes de finalizar a resposta.'

            message = [{
                'role': 'user',
                'content': content
            }]

            response = client.chat.completions.create(
                messages=message, 
                model="gpt-4o-mini", 
                max_tokens=10000, 
                temperature=0, 
            )
            news_summary = response.choices[0].message.content

            return news_summary
        except Exception as e:
            print(f'Erro em create_news_create_news_summary: {e}')
            return 'N/A'



    def create_news_image(self):
        try:
            counter = 1
            for n in self.referenceImages:
                display(Image(url=n.imageUrl,height=200))
                print(f'{counter} >> {n.imageText}')
                counter += 1
            time.sleep(2)
            imageInput = input("#|Fonte:?????")
            clear_output() 
            imageNumber = int(imageInput.split("|")[0]) - 1
            imageText = imageInput.split("|")[1]
            
            self.imageUrl = self.referenceImages[imageNumber].imageUrl
            self.imageText = f'Fonte: {imageText}'

        except Exception as e:
            print("Problema na seleção da imagem:", e)
            return 'N/A', 'N/A'



    def save_news(self):
        try:
            url = f'{API_URL}/api/news'
            payload = {
                "uid": "johannesadmin",
                "supportUid": "johannesadmin",
                "h1": self.title,
                "h2": self.title,
                "summary": self.summary,
                "text": self.text,
                "imageUrl": self.imageUrl,
                "imageText": self.imageText,
                "sectionName": self.sectionName,
                "__t": "published",
            }
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
        except Exception as e:
            print("Problema ao salvar notícia:", e)



