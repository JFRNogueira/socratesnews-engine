import requests
import openai
import os
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st


class RPAWriter:

    def __init__(self):
        self.searched_news = self.get_searched_news()
        self.text = self.create_news_text()
        self.h1 = self.create_news_title()
        self.h2 = self.h1
        self.summary = self.create_news_summary()
        self.imageUrl = ''
        self.imageText = ''
        
        self.save_complete_news(self.searched_news['newsId'])



    def get_searched_news(self):
        try:
            url = f'https://api-prod.jornalsocrates.com.br/api/searchednews'
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



    def create_news_text(self):
        referenceNews = self.searched_news['referenceNews']
        references = '\n\n'
        for n in referenceNews:
            references += f'{n['text']}\n\n'
        content = f'Escreva um texto jornalístico que será publicado na seção "{self.searched_news['sectionName']}" de um jornal de grande circulação.\n'
        content += f'Considere como referêcia exclusivamente o que foi extraído de alguns sites de prestígio:{references}'
        content += f'Crie o texto sem enrolação e apenas com informações relevantes. Escreva estritamente a notícia a ser publicada, sem necessidade de dar um título (manchete) ao texto.\n\n'
        content += f'O texto da notícia deve possui obrigatoriamente entre 400 e 450 palavras.\n'
        content += f'Se a quantidade de palavras não estiver de acordo com o solicitado, ajuste o campo para atender ao requisito antes de finalizar a resposta.\n'
        content += f'Reforço que deve ser apenas o texto, não incluindo manchete, autor preâmbulo ou qualquer coisa diferente do corpo da notícia.\n'
        message = [{
            'role': 'user',
            'content': content
        }]
        client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
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
            referenceNews = self.searched_news['referenceNews']
            references = '\n\n'
            for t in referenceNews:
                references += f'{t['title']}\n'
            content = f'Escreva um preâmbulo para o texto jornalístico abaixo, que será publicado na seção "{self.searched_news['sectionName']}" de um jornal de grande circulação.\n\n'
            content += f'{self.text}\n\n'
            content += f'Pode considerar como referência de bons títulos a lista a seguir, extraída de jornais de prestígio:\n{references}\n\n\n'
            content += f'Escreva apenas o título da matéria, que deve conter entre 8 e 15 palavras.\n'
            content += f'Reforço que deve ser apenas o título, não incluindo texto, autor, preâmbulo ou qualquer coisa diferente do título da notícia.\n'
            content += f'Se a quantidade de palavras não estiver de acordo com o solicitado, ajuste o campo para atender ao requisito antes de finalizar a resposta.'
            message = [{
                'role': 'user',
                'content': content
            }]
            client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
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
            content = f'Escreva um resumo para o texto jornalístico abaixo, que será publicado na seção "{self.searched_news['sectionName']}" de um jornal de grande circulação.\n\n'
            content += f'{self.text}\n\n'
            content += f'Escreva apenas o preâmbulo da matéria, que deve conter entre 30 e 50 palavras.\n'
            content += f'Reforço que deve ser apenas o preâmbulo, não incluindo texto, autor, título ou qualquer coisa diferente do preâmbulo da notícia.\n'
            content += f'Se a quantidade de palavras não estiver de acordo com o solicitado, ajuste o campo para atender ao requisito antes de finalizar a resposta.'

            message = [{
                'role': 'user',
                'content': content
            }]
            client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
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



    def save_complete_news(self, newsId):
        try:
            url = f'https://api-prod.jornalsocrates.com.br/api/news/{newsId}'
            payload = {
                "uid": 'jvfbEGdoKJYokMi4FgA3AFMI4tO2',
                "supportUid": 'jvfbEGdoKJYokMi4FgA3AFMI4tO2',
                "h1": self.h1,
                "h2": self.h2,
                "summary": self.summary,
                "text": self.text,
                "__t": "published"
            }
            response = requests.patch(url, json=payload)
            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
            return response
        except Exception as e:
            print("Problema ao salvar notícia em save_searched_news:", e)



