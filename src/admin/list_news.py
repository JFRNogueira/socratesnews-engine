# list_news.py
import streamlit as st
import pandas as pd
import requests

def get_news_view(page=1):
    API_URL = f'https://socratesnews-dev-1aaab5bd4746.herokuapp.com/api/news?page={page}'
    response = requests.get(API_URL)
    result = pd.DataFrame(response.json())
    result['newsUrl'] = 'https://dev.jornalsocrates.com.br/noticia/' + result["newsId"]
    return result



def list_news():
    st.title("Notícias disponíveis")
    
    news = get_news_view()

    if not news.empty:
            st.dataframe(
                news,
                column_config={
                    "imageUrl": st.column_config.ImageColumn(
                        "Imagem", help="Streamlit app preview screenshots"
                    ),
                    "newsUrl": st.column_config.LinkColumn(
                        "no jornal", display_text="Visualizar"
                    ),
                },
                hide_index=True
            )
    else:
        st.write("Nenhuma notícia disponível no momento.")
