# edit_news.py
import streamlit as st
import pandas as pd

def edit_news():
    st.title("Editar Notícia")

    if st.session_state.news_data.empty:
        st.info("Nenhuma notícia disponível para editar.")
        return

    # Selecionar a notícia pelo ID
    news_ids = st.session_state.news_data['ID'].tolist()
    selected_id = st.selectbox("Selecione o ID da notícia para editar", news_ids)

    # Obter a notícia selecionada
    news_item = st.session_state.news_data.loc[st.session_state.news_data['ID'] == selected_id]

    # Campos para editar
    title = st.text_input("Título", news_item['Título'].values[0])
    body = st.text_area("Corpo", news_item['Corpo'].values[0])

    if st.button("Atualizar"):
        # Atualizar os valores no DataFrame
        st.session_state.news_data.loc[st.session_state.news_data['ID'] == selected_id, 'Título'] = title
        st.session_state.news_data.loc[st.session_state.news_data['ID'] == selected_id, 'Corpo'] = body
        st.success("Notícia atualizada com sucesso!")
