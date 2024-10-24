import requests
import openai
import os
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st


class WriterNews:

    def __init__(self, section, referenceNews, referenceTitles, imageUrl, imageText):
        self.section = section # String
        self.referenceNews = referenceNews # Array de strings
        self.referenceTitles = referenceTitles # Array de strings
        self.imageUrl = imageUrl # String
        self.imageText = imageText # String
        
        self.text = self.create_news_text()
        self.title = self.create_news_title()
        self.summary = self.create_news_summary()
        
        self.save_news()





    def create_news_text(self):
        
        references = '\n\n'
        for n in self.referenceNews:
            references += f'{n}\n\n'
        
        content = f'Escreva um texto jornalístico que será publicado na seção "{self.section}" de um jornal de grande circulação.\n'
        content += f'Considere como referêcia exclusivamente o que foi extraído de alguns sites de prestígio:{references}'
        content += f'Crie o texto sem enrolação e apenas com informações relevantes. Escreva estritamente a notícia a ser publicada, sem necessidade de dar um título (manchete) ao texto.\n\n'
        content += f'O texto da notícia deve possui obrigatoriamente entre 700 e 800 palavras.\n'
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
            references = '\n\n'
            for t in self.referenceTitles:
                references += f'{t}\n'
            
            content = f'Escreva um preâmbulo para o texto jornalístico abaixo, que será publicado na seção "{self.section}" de um jornal de grande circulação.\n\n'
            content += f'{self.text}\n\n'
            content += f'Pode considerar como referência de bons títulos a lista a seguir, extraída de jornais de prestígio:\n{references}\n\n\n'
            content += f'Escreva apenas o título da matéria, que deve conter entre 70 e 100 caracteres.\n'
            content += f'Reforço que deve ser apenas o título, não incluindo texto, autor, preâmbulo ou qualquer coisa diferente do título da notícia.\n'
            content += f'Se a quantidade de caracteres não estiver de acordo com o solicitado, ajuste o campo para atender ao requisito antes de finalizar a resposta.'

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
            content = f'Escreva um resumo para o texto jornalístico abaixo, que será publicado na seção "{self.section}" de um jornal de grande circulação.\n\n'
            content += f'{self.text}\n\n'
            content += f'Escreva apenas o preâmbulo da matéria, que deve conter entre 190 e 220 caracteres.\n'
            content += f'Reforço que deve ser apenas o preâmbulo, não incluindo texto, autor, título ou qualquer coisa diferente do preâmbulo da notícia.\n'
            content += f'Se a quantidade de caracteres não estiver de acordo com o solicitado, ajuste o campo para atender ao requisito antes de finalizar a resposta.'

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



    def save_news(self):
        try:
            url = f'{st.secrets['API_URL']}api/news'
            payload = {
                "uid": "aKwP8Bwx34fW18Rkqr4u31uYoQ23",
                "supportUid": "aKwP8Bwx34fW18Rkqr4u31uYoQ23",
                "h1": self.title,
                "h2": self.title,
                "summary": self.summary,
                "text": self.text,
                "imageUrl": self.imageUrl,
                "imageText": self.imageText,
                "sectionName": self.section,
                "__t": "published",
            }
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
        except Exception as e:
            print("Problema ao salvar notícia:", e)




