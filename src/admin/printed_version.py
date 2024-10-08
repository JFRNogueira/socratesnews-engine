# list_news.py
import streamlit as st
import pandas as pd
import requests

def get_pages_view():
    pages = [
        {'page': 1,  'sectionName': 'Capa', '#news': 4},
        {'page': 2,  'sectionName': 'Opinião', '#news': 4},
        {'page': 3,  'sectionName': 'Mundo', '#news': 4},
        {'page': 4,  'sectionName': 'Mundo', '#news': 4},
        {'page': 5,  'sectionName': 'Brasil', '#news': 4},
        {'page': 6,  'sectionName': 'Brasil', '#news': 4},
        {'page': 7,  'sectionName': 'Estado', '#news': 4},
        {'page': 8,  'sectionName': 'Estado', '#news': 4},
        {'page': 9,  'sectionName': 'Cidades', '#news': 4},
        {'page': 10, 'sectionName': 'Cidades', '#news': 4},
        {'page': 11, 'sectionName': 'Ciência e Tecnologia', '#news': 4},
        {'page': 12, 'sectionName': 'Ciência e Tecnologia', '#news': 4},
        {'page': 13, 'sectionName': 'Entretenimento', '#news': 4},
        {'page': 13, 'sectionName': 'Entretenimento', '#news': 4},
        {'page': 13, 'sectionName': 'Oração', '#news': 4},
        {'page': 14, 'sectionName': 'Infantil', '#news': 4},
        {'page': 15, 'sectionName': 'Previsão', '#news': 4},
        {'page': 16, 'sectionName': 'Turismo', '#news': 4},
        {'page': 17, 'sectionName': 'Publicidade legal', '#news': 4},
        {'page': 18, 'sectionName': 'Publicidade legal', '#news': 4},
        {'page': 19, 'sectionName': 'Publicidade legal', '#news': 4},
        {'page': 20, 'sectionName': 'Publicidade legal', '#news': 4},
    ]
    result = pd.DataFrame(pages)
    sections = result['sectionName'].tolist()
    sections = list(dict.fromkeys(sections))
    return result, sections



def printed_version():
    col1, col2 = st.columns(2)
    
    pages, sections = get_pages_view()
    
    with col1:
        st.title("Versão impressa")
        st.subheader('Definição da seção')
        state = st.selectbox('Estado', ['AC', 'AL', 'BA', 'SP'])
        section = st.selectbox('Seção', sections)
        st.dataframe(pages, hide_index=True)
        if st.button("Secionar notícias"):
            st.success(f"Página gerada com sucesso!")
    
    with col2:
        st.title("")
        st.subheader('Definição das notícias')
        page = st.number_input('Página', step=1, min_value=1)
        news = st.multiselect('Notícias', ['AC', 'AL', 'BA', 'CE', 'PB', 'PE', 'SP'])
        if st.button("Gerar página"):
            st.success(f"Página gerada com sucesso!")
