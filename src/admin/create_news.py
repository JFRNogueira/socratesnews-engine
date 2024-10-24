# create_news.py
import streamlit as st
import pandas as pd
import requests
from datetime import datetime

def get_sections():
    API_URL = f'{st.secrets['API_URL']}api/section'
    response = requests.get(API_URL)
    sections = []
    for section in response.json():
        sections.append(section['sectionName'])
    sections.remove("Últimas")
    return sections


def publish(title, section, imageSource, imageUrl, publishAtDate, publishAtTime, summary, body, tags):
    API_URL = f'{st.secrets['API_URL']}api/news'
    data = datetime(publishAtDate.year, publishAtDate.month, publishAtDate.day, publishAtTime.hour, publishAtTime.minute, 0, 0)
    formatted_date = data.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+00:00"
    payload = {
        # TODO: Adicionar o suporte ao uid do usuário
        'supportUid': 'aKwP8Bwx34fW18Rkqr4u31uYoQ23',
        'uid': st.session_state.uid,
        "h1": title,
        "h2": title,
        "summary": summary,
        "sectionName": section,
        "text": body,
        "imageText": imageSource,
        "imageUrl": imageUrl,
        "tags": tags.split(";"),
        "publishedAt": formatted_date,
    }
    response = requests.post(API_URL, json=payload)
    return response.status_code, response.json()['newsId']

def open_news(newsId):
    js = f"<script>window.open('https://jornalsocrates.com.br/noticia/{newsId}');</script>"
    st.markdown(js, unsafe_allow_html=True)

def create_news():
    col1, col2 = st.columns(2)
    
    sections = get_sections()
    
    with col1:
        st.title("Criar matéria")
        # Campos de entrada para a notícia
        title = st.text_input("Título")
        section = st.selectbox("Seção:", sections)
        imageSource = st.text_input("Fonte da imagem")
        imageUrl = st.text_input("URL da imagem")
        if st.button("Visualizar"):
            st.image(imageUrl, caption="Imagem da notícia", use_column_width=True)
        publishAtDate = st.date_input("Publicar em")
        publishAtTime = st.time_input("Publicado em hora")
    
    with col2:
        st.title("")
        summary = st.text_area("Resumo")
        body = st.text_area("Matéria")
        body_word_count = len(body.split())
        body_letter_count = len(body)
        st.write(f"{body_word_count} palavras e {body_letter_count} caracteres")
    
        tags = st.text_input("Marcadores (separados por ';')")
        

    if st.button("Publicar"):
        if title and section and imageSource and imageUrl and publishAtDate and publishAtTime and summary and body and tags:
            status, newsId = publish(title, section, imageSource, imageUrl, publishAtDate, publishAtTime, summary, body, tags)
            st.success(f"Status: {status} >> Notícia publicada e disponível em https://dev.jornalsocrates.com.br/noticia/{newsId}")
            open_news(newsId)
        else:
            st.error("Por favor, preencha todos os campos.")
