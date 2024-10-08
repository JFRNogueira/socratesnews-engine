# list_news.py
import streamlit as st
import pandas as pd
import requests

def get_news(page=1):
    API_URL = f'https://socratesnews-dev-1aaab5bd4746.herokuapp.com/api/news?page={page}'
    response = requests.get(API_URL)
    result = pd.DataFrame(response.json())
    return result



def list_news():
    st.title("Notícias disponíveis")
    
    news = get_news()

    if not news.empty:
            st.dataframe(
                news,
                column_config={
                    "imageUrl": st.column_config.ImageColumn(
                        "Preview Image", help="Streamlit app preview screenshots"
                    )
                },
                hide_index=True
            )
    else:
        st.write("Nenhuma notícia disponível no momento.")
