import streamlit as st
import requests
import pandas as pd

class Services:
    
    def get_sections():
        url = f'{st.secrets['API_URL']}api/section'
        result = requests.get(url)
        return result.json()
        


    def get_news_by_section(sectionId):
        
        url = f'{st.secrets['API_URL']}api/news?sectionId={sectionId}&page=1'
        payload = {
            'supportUid': st.secrets['SUPPORT_UID'],
            'uid': st.secrets['SUPPORT_UID']
        }
        res = requests.get(url, json=payload)
        res_json = res.json()
        result = pd.DataFrame(res_json)
        return result
        


    def get_news_by_id(newsId):
        
        url = f'{st.secrets['API_URL']}api/news/{newsId}'
        payload = {
            'supportUid': st.secrets['SUPPORT_UID'],
            'uid': st.secrets['SUPPORT_UID']
        }
        res = requests.get(url, json=payload)
        result = res.json()
        return result
        
