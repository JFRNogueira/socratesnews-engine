# login.py
import streamlit as st
from streamlit_image_select import image_select
import utils.services as services
import pandas as pd
import numpy as np
import plotly.graph_objects as go

import streamlit as st

class HoroscopePrediction():
    
    def signs(self):
        return [
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

class WetherForecast():
    
    def cities_counter(self, selected_cities):
        # Contar número de linhas com default=True em selected_cities
        indicator_value = selected_cities['default'].sum()
        
        st.markdown(f"**{indicator_value}** cidades selecionadas")
        target_value = 12
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=indicator_value,
            title={'text': "Indicator Value"},
            gauge={
                'axis': {'range': [0, 24], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue" if indicator_value == target_value else "red"},
                'steps': [
                    {'range': [0, 12], 'color': "lightcoral"},
                    {'range': [12, 24], 'color': "lightgreen"}],
                'threshold': {
                    'line': {'color': "green", 'width': 4},
                    'thickness': 0.75,
                    'value': target_value}}))

        st.plotly_chart(fig)      
        
        
    
    def show_cities(self):
        cities = [
            { "apiId": 1,  "city": "São Paulo", "default": True },
            { "apiId": 2,  "city": "Campinas", "default": True },
            { "apiId": 3,  "city": "São José dos Campos", "default": True },
            { "apiId": 4,  "city": "Rio de Janeiro", "default": True },
            { "apiId": 5,  "city": "Fortaleza", "default": True },
            { "apiId": 6,  "city": "Pacajús", "default": True },
            { "apiId": 7,  "city": "Horizonte", "default": True },
            { "apiId": 8,  "city": "Crato", "default": True },
            { "apiId": 9,  "city": "Barbalha", "default": True },
            { "apiId": 10, "city": "Piracanjuba", "default": True },
            { "apiId": 11, "city": "Goiânia", "default": True },
            { "apiId": 12, "city": "Aparecida", "default": True },
            { "apiId": 13, "city": "Cascavel", "default": False },
            { "apiId": 14, "city": "Porto Alecre", "default": False },
            { "apiId": 15, "city": "Vitória", "default": False },
            { "apiId": 16, "city": "Salvador", "default": False },
            { "apiId": 17, "city": "Recife", "default": False },
            { "apiId": 18, "city": "Aracaju", "default": False },
            { "apiId": 19, "city": "Maceió", "default": False },
            { "apiId": 20, "city": "Natal", "default": False }
        ]
        cities_df = pd.DataFrame(cities)

        # Armazenar o DataFrame editado em uma variável temporária
        edited_df = st.data_editor(
            cities_df[['default', 'city', 'apiId']],
            column_config={
                "default": st.column_config.CheckboxColumn(
                    "Considerar?", help="Selecione 12 cidades que terão sua previsão do tempo disponibilizada"
                ),
                "city": st.column_config.TextColumn(
                    "Cidade", help="Nome da cidade",
                    disabled=True
                ),
                "apiId": st.column_config.TextColumn(
                    "Chave de API", help="Apenas para referência junto ao serviço meteorológico",
                    disabled=True
                ),
            },
            hide_index=True
        )

        self.cities_counter(edited_df)






def previsao():
    st.header('Previsões')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader('Horóscopo', divider=True)
        
        for sign in HoroscopePrediction().signs():
            if st.toggle(label=sign['name']):
                st.markdown(sign['fromTo'])
    
    with col2:
        st.subheader('Previsão do tempo', divider=True)
        WetherForecast().show_cities()
        
    with col3:
        st.subheader('Versão impressa', divider=True)
        st.button('Pré-visualizar')
        