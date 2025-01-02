import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import datetime, timedelta


class Prayer:
    
    
    
    def __init__(self):
        pass
    
    
    def get_html_content(self, date, type):
        try:
            if type == 'gospels':
                url = f'https://www.vaticannews.va/pt/palavra-do-dia/{date.strftime("%Y/%m/%d")}.html'
            if type == 'saints':
                url = f'https://www.vaticannews.va/pt/santo-do-dia/{date.strftime("%m/%d")}.html'
                
            headers  = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()  # Levanta exceção para status HTTP de erro
            return BeautifulSoup(response.text, 'html.parser')
        
        except Exception as e:
            print(f'\nPrayer >> Erro ao buscar conteúdo em {url} \n\n {e}')
            return None
    
    
    
    def get_gospels_data(self, date):
        try:
            html = self.get_html_content(date, 'gospels')
            if not html:
                print("HTML não foi carregado corretamente.")
                return None
            # Encontra todas as sections pelo class name
            sections = html.findAll('section', class_='section section--evidence section--isStatic')
            data = [section for section in sections]
            
            reading_raw = data[0].find('div', class_='section__content').get_text().strip()
            reading_1 = ' '.join(reading_raw.split('\n')[0].split(' ')[4:]).strip() + ' ' + reading_raw.split('\n')[1].strip()
            reading_2 = '\n\n'.join(reading_raw.split('\n')[2:]).strip()
            
            gospel_raw = data[1].find('div', class_='section__content').get_text().strip()
            gospel_1 = ' '.join(gospel_raw.split('\n')[0].split(' ')[7:]).strip() + ' ' + gospel_raw.split('\n')[1].strip()
            gospel_2 = '\n\n'.join(gospel_raw.split('\n')[2:]).strip()
            
            pope_raw = data[2].find('div', class_='section__content').get_text().replace('\n', '\n\n')
            pope_1 = pope_raw.split('(')[-1][:-1].strip()
            pope_2 = '('.join(pope_raw.split('(')[:-1]).strip()
            
            return [reading_1, reading_2], [gospel_1, gospel_2], [pope_1, pope_2]
        except Exception as e:
            print(f'\nPrayer >> Erro ao extrair readings \n\n {e}')
            return None, None, None
        
        
    
    def get_saints(self, date):
        try:
            html = self.get_html_content(date, 'saints')
            if not html:
                print("HTML não foi carregado corretamente.")
                return None
            saints = html.findAll('section', class_='section section--evidence section--isStatic')
            result = []
            for saint in saints:
                try:
                    name = saint.find('div', class_='section__head').get_text().strip()
                except:
                    name = ''
                try:
                    text = saint.find('div', class_='section__wrapper').get_text().strip().replace('\n', '\n\n')
                except:
                    text = ''
                try:
                    imageUrl = 'https://www.vaticannews.va' + saint.find('img').get('data-original')
                except:
                    imageUrl = ''

                result.append({'name': name, 'text': text, 'imageUrl': imageUrl}) 
            return result
        except Exception as e:
            print(f'\nPrayer >> Erro ao extrair saints \n\n {e}')
            return []
    
    
    
    def save_daily_prayer(self, date):
        API_URL = f'{st.secrets['API_URL']}api/prayer'
        
        saints = []
        for s in st.session_state.get('saints', []):
            saints.append({
                'name': s['name'],
                'summary': s['text'],
                'text': s['text'],
                'imageUrl': s['imageUrl'] if s['imageUrl'] == '' else '',
                'imagePath':'',
                'imageText': 'Vatican News' if s['imageUrl'] == '' else ''
            })
        
        readings = [{
            'text': st.session_state.get('reading', ['', ''])[1], 
            'ref': st.session_state.get('reading', ['', ''])[0]
            }]
        
        gospel = [{
            'text': st.session_state.get('gospel', ['', ''])[1], 
            'ref': st.session_state.get('gospel', ['', ''])[0]
            }]
        
        popeWords = [{
            'text': st.session_state.get('pope', ['', ''])[1], 
            'ref': st.session_state.get('pope', ['', ''])[0]
            }]
        
        payload = {
            'supportUid': st.secrets['SUPPORT_UID'],
            'uid': st.secrets['SUPPORT_UID'],
            "saints": saints,
            "readings": readings,
            "gospel": gospel,
            "popeWords": popeWords,
            "referenceDate": f'{date.year}-{date.month}-{date.day}T00:00:00.000+00:00'
        }
        response = requests.post(API_URL, json=payload)
        return response.status_code == 200
    
    
    
    def rpa(self, n_days=1):
        today = datetime.today()
        for i in range(n_days):
            date = today + timedelta(days=i)
            st.session_state['reading'], st.session_state['gospel'], st.session_state['pope'] = self.get_gospels_data(date)
            st.session_state['saints'] = self.get_saints(date)
            self.save_daily_prayer(date)
        
        
        
    def ui(self):
        st.header("Oração")
        
        col1, col2 = st.columns([1, 4], gap='large')
        
        with col1:
            st.subheader("Parâmetros", divider=True)
            st.slider('Buscar conteúdo para quantos dias?', 1, 7, 3, key='prayer_n_days')
            today = datetime.today()
            st.session_state['prayer_days_list'] = [(today + timedelta(days=i)) for i in range(st.session_state.get('prayer_n_days', 7))]
            
            if st.button('Gerar conteúdo'):
                for date in st.session_state['prayer_days_list']:
                    st.session_state['reading'], st.session_state['gospel'], st.session_state['pope'] = self.get_gospels_data(date)
                    st.session_state['saints'] = self.get_saints(date)
                    self.save_daily_prayer(date)
            
            st.divider()
            
            st.date_input('Data do conteúdo exibido ao lado', value=today, max_value=st.session_state['prayer_days_list'][-1], min_value=today)
            if st.button('Visualizar conteúdo'):
                st.session_state['prayer_status'] = ''

        
        with col2:
            st.subheader("Conteúdo", divider=True)
            
            col21, col22, col23, col24 = st.columns(4)
            
            with col21:
                st.subheader("Santo do dia", divider=True)
                for saint in st.session_state.get('saints', []):
                    st.markdown(f"### {saint['name']}")
                    try:
                        st.image(saint['image'], width=100)
                    except:
                        pass
                    st.markdown(saint['text'])
                    st.divider()
                
            with col22:
                st.subheader("Leitura do dia", divider=True)
                st.markdown('\n\n'.join(st.session_state.get('reading', ['', ''])))
                
            with col23:
                st.subheader("Evangelho do dia", divider=True)
                st.markdown('\n\n'.join(st.session_state.get('gospel', ['', ''])))
                
            with col24:
                st.subheader("Palavras do papa", divider=True)
                st.markdown('\n\n'.join(st.session_state.get('pope', ['', ''])))
                
        
        


