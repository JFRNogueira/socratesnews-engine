import pandas as pd
import os
import openai
from dotenv import load_dotenv
import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
import random
import streamlit as st

load_dotenv()


class HoroscopoSec:
    
    def get_horoscope_prediction_joao_bidu(self, sign):
        try:
            url =  f'https://joaobidu.com.br/horoscopo/signos/previsao-{sign}/'
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            elemento = soup.find('div', class_='theiaPostSlider_preloadedSlide')
            previsao = elemento.find('div', class_='zoxrel left').text.split('\n')[0][7:-1]
        except:
            previsao = ''
        return previsao



    def get_horoscope_prediction_terra(self, sign):
        try:
            url =  f'https://www.terra.com.br/vida-e-estilo/horoscopo/signos/{sign}/'
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            elemento = soup.find('div', class_='horoscope--content__embed')
            previsao = elemento.find('p').text
        except:
            previsao = ''
        return previsao



    def get_horoscope_prediction_uol(self, sign):
        try:
            url =  f'https://www.uol.com.br/universa/horoscopo/{sign}/horoscopo-do-dia/'
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            elemento = soup.find('div', class_='horoscope-open-content')
            previsao = elemento.find('p').text
        except:
            previsao = ''
        return previsao



    def get_horoscope_prediction_personare(self, sign):
        try:
            url =  f'https://www.personare.com.br/horoscopo-do-dia/{sign}'
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            elemento = soup.find('div', class_='styles__Text-sc-1ryixz1-3')
            previsao = elemento.find('p').text
        except:
            previsao = ''
        return previsao



    def get_horoscope_prediction(self, sign):

        previsao_joaobidu = self.get_horoscope_prediction_joao_bidu(sign)
        previsao_terra = self.get_horoscope_prediction_terra(sign)
        previsao_uol = self.get_horoscope_prediction_uol(sign)
        previsao_personare = self.get_horoscope_prediction_personare(sign)
        
        predictions = f'Previsão 1: {previsao_joaobidu}\n\nPrevisão 2: {previsao_terra}\n\nPrevisão 3: {previsao_uol}\n\nPrevisão 4: {previsao_personare}' 

        return predictions



    def save_horoscope(self, sign, prediction, reference):
        API_URL = f'{st.secrets['API_URL']}api/news'
        
        payload1 = {
            "uid": "aKwP8Bwx34fW18Rkqr4u31uYoQ23",
            "supportUid": "aKwP8Bwx34fW18Rkqr4u31uYoQ23",
            "h1": sign,
            "h2": sign,
            "summary": "Previsão do dia",
            "text": prediction,
            "imageUrl": f'https://storage.googleapis.com/socrates-news-dev.appspot.com/icons/horoscope/pequeno_{reference}.png',
            "imageText": "Gerado com apoio de Inteligência Artificial",
            "sectionName": "Horóscopo",
            "publishedAt": datetime.now().strftime('%Y-%m-%dT00:00:00.000+00:00')
        }
        res1 = requests.post(API_URL, json=payload1)



    def create_daily_horoscope(self):
        signos = [
            {"name": "Áries", "fromTo": "21-mar a 20-abr", "reference": "aries"},
            {"name": "Touro", "fromTo": "21-abr a 20-mai", "reference": "touro"},
            {"name": "Gêmeos", "fromTo": "21-mai a 20-jun", "reference": "gemeos"},
            {"name": "Câncer", "fromTo": "21-jun a 21-jul", "reference": "cancer"},
            {"name": "Leão", "fromTo": "22-jul a 22-ago", "reference": "leao"},
            {"name": "Virgem", "fromTo": "23-ago a 22-set", "reference": "virgem"},
            {"name": "Libra", "fromTo": "23-set a 22-out", "reference": "libra"},
            {"name": "Escorpião", "fromTo": "23-out a 21-nov", "reference": "escorpiao"},
            {"name": "Sagitário", "fromTo": "22-nov a 21-dez", "reference": "sagitario"},
            {"name": "Capricórnio", "fromTo": "22-dez a 20-jan", "reference": "capricornio"},
            {"name": "Aquário", "fromTo": "21-jan a 19-fev", "reference": "aquario"},
            {"name": "Peixes", "fromTo": "20-fev a 20-mar", "reference": "peixes"}
        ]
        
        startWith = [
            "hoje",
            "aproveite o momento para",
            "concentre-se em",
            "é o momento perfeito para",
            "preste atenção",
            "busque o equilíbrio em suas relações e tome decisões ponderadas.",
            "um período de",
            "novas aventuras e oportunidades estão prestes a surgir.",
            "trabalhe com",
            "sua",
            "permita-se",
        ]
        
        result = []
        for s in signos:
            reference = self.get_horoscope_prediction(s["reference"])
            content = f'Qual o horóscopo de {s["name"].lower()} para hoje? Escreva um texto entre 35 e 40 palavras que será publicado em um jornal. Se necessário, considere a referêcia existente em alguns sites de prestígio \n\n{reference}\n\nComece com: "{s["name"]}, {random.choice(startWith)}"'
            message = [{
                'role': 'user',
                'content': content
            }]
            
            client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                messages=message, 
                model="gpt-4o-mini", 
                max_tokens=1000, 
                temperature=0, 
                )
            prediction = response.choices[0].message.content
            self.save_horoscope(s["name"], prediction, s["reference"])
            result.append({"sign": s["name"], "prediction": prediction})
        
        return result




