import streamlit as st
import pandas as pd
import requests
import openai
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os
import time
from journalist.previsoes_sec import HoroscopoSec
from journalist.infantil_sec import InfantilThemes, InfantilSec



def previsoes():
    col1, col2 = st.columns(2)
    
    if 'forecast_dt' not in st.session_state:
        st.session_state['forecast_dt'] = None

    with col1:
        st.title("Previsões")
        st.subheader("Horóscopo")
        
        if st.button('Gerar horóscopo'):
             horoscopos = HoroscopoSec().create_daily_horoscope()
             for h in horoscopos:
                 st.write(h)
             

    with col2:
        st.title("")
        st.subheader("Previsão do tempo")

        if st.button('Buscar cidades'):
            st.subheader("Falta implementar")


if __name__ == '__main__':
    previsoes()
    
    