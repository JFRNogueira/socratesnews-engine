import streamlit as st
import pandas as pd
import requests
import openai
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os
import time
from journalist.infantil_sec import InfantilThemes, InfantilSec


def get_child_theme(date_str, options):
    # Adicionar a opção "Personalizar"
    options.append("Personalizar")
    # options = ["Opção 1", "Opção 2", "Opção 3", "Personalizar"]

    # Cria o selectbox
    st.selectbox("Escolha uma opção", options, key=f'infantil_news_{date_str}')

    # Verifica se a opção "Personalizar" foi selecionada
    if selected_option == "Personalizar":
        # Abre um campo de input para valor personalizado
        custom_value = st.text_input("Digite seu valor personalizado")
        
        # Exibe o valor personalizado na tela (para confirmar)
        if custom_value:
            st.write(f"Valor personalizado: {custom_value}")
    else:
        # Caso contrário, exibe a opção escolhida
        st.write(f"Opção selecionada: {selected_option}")



def infantil():
    col1, col2 = st.columns(2)
    
    # Inicializando o estado da sessão
    if 'infantil_news_status' not in st.session_state:
        st.session_state['themes'] = None
        st.session_state['from_dt'] = None
        st.session_state['to_dt'] = None
        st.session_state['infantil_news_status'] = 'r'

    with col1:
        st.title("Infantil")
        
        # Definindo o intervalo de datas
        from_dt = st.date_input('Data de início')
        to_dt = st.date_input('Data de fim')

        # Botão para visualizar os temas
        if st.button('Ver temas'):
            st.session_state['from_dt'] = from_dt
            st.session_state['to_dt'] = to_dt

        # Exibindo e editando o DataFrame apenas se os temas estiverem no estado
        if st.session_state['from_dt'] is not None:
            unique_days = pd.date_range(start=st.session_state['from_dt'], end=st.session_state['to_dt']).to_list()
            
            result_df = pd.DataFrame(columns=["dia", "descricao"])
            for day in unique_days:
                descriptions = InfantilThemes().get_themes_by_day(day)
                selected_description = st.selectbox(f"Tema para o dia {day.strftime('%d-%m-%y')}", descriptions)
                result_df = pd.concat([result_df, pd.DataFrame({"dia": [day], "descricao": [selected_description]})])
            
            # Botão para gerar notícias
            if st.button('Gerar notícias'):
                st.session_state['infantil_news_status'] = ''
                for index, row in result_df.iterrows():
                    InfantilSec(row['dia'], row['descricao'])
                    st.markdown(f'{row["dia"].strftime("%d-%m-%y")} >> {row['descricao']}')

    with col2:
        st.title("")
        st.text(st.session_state['infantil_news_status'])

# Testando a função infantil
if __name__ == '__main__':
    infantil()
    
    