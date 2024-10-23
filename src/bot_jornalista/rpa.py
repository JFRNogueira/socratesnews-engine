import time
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from bot_jornalista.writer_news import WriterNews
from sources.google_news import GoogleNews, GoogleNewsCluster
from streamlit_image_select import image_select

def select_themes(section):
    slider_value = st.session_state[f'rps_{section.lower()}_slider_value']
    df = st.session_state[f'{section.lower()}_themes_selection'].copy()
    counter = 0
    for index, t in df.iterrows():
        check1 = counter < slider_value
        check2 = t['title'] != 'N/A'
        if check1 and check2:
            df.at[index, 'create'] = True
            counter += 1
        else:
            df.at[index, 'create'] = False
    st.session_state[f'{section.lower()}_themes_selection'] = df



def rpa():
    sections = ['Mundo', 'Brasil', 'Economia', 'C&T', 'Entretenimento', 'Esporte']
    
    col1, col2 = st.columns(2)

    with col1:
        st.title("Bot RPA")
        # if 'rpa_themes_selected' not in st.session_state:
        #     default_themes = []
        # else:
        #     default_themes = st.session_state['rpa_themes_selected']
        st.session_state['rpa_themes_selected'] = st.multiselect("Selecione os temas", sections, default=sections)
        
        if st.button("Buscar temas no Google News"):
            GoogleNews(st.session_state['rpa_themes_selected'])
        
        for s in st.session_state['rpa_themes_selected']:
            if f'rps_{s.lower()}_slider_value' not in st.session_state:
                st.session_state[f'rps_{s.lower()}_slider_value'] = 8
        
        for s in st.session_state['rpa_themes_selected']:
            if f'{s.lower()}_themes_selection' in st.session_state:
                st.slider(
                    f'Notícias na seção {s}', 
                    min_value=0, 
                    max_value=st.session_state[f'{s.lower()}_themes_selection'].shape[0], 
                    value=min(8, st.session_state[f'{s.lower()}_themes_selection'].shape[0]), 
                    key=f'rps_{s.lower()}_slider_value',
                    on_change=select_themes(s)
                    )



    with col2:
        st.header("")
        if st.button("Buscar fontes para notícias"):
            GoogleNewsCluster(st.session_state['rpa_themes_selected']).get_all_references()
            st.write(st.session_state['rpa_themes_selected'])
            
        
        # # If there is at least one selected theme
        # if 'brasil_themes_selection' in st.session_state:
        #     n_news = st.session_state['brasil_themes_selection'].shape[0]
        #     n_expected = (st.session_state['brasil_themes_selection']['create'] == True).sum()

        #     # Exibir as métricas acima do editor
        #     col11, col12 = st.columns(2)
        #     col11.metric("# Temas", n_news)
        #     col12.metric("Temas selecionados", n_expected)
        # else:
        #     st.header("")



        # st.subheader('Gerador de notícias')
        # if 'brasil_themes_selection' in st.session_state and (st.session_state['brasil_themes_selection']['create'] == True).sum() > 0:
        #     selected_themes = st.session_state['brasil_themes_selection'][st.session_state['brasil_themes_selection']['create'] == True]

        #     tabs = st.tabs([f"N {i}" for i in range(1, n_expected+1)])
        #     for n_tab, tab in enumerate(tabs, start=1):
        #         with tab:
        #             st.write(f"**Tema {n_tab}: {selected_themes['title'].iloc[n_tab-1]}**")

        #             if f'brasil_news_{n_tab}_reference_news' in st.session_state:

        #                 # Input de imageText
        #                 st.session_state[f'brasil_news_{n_tab}_image_text'] = st.text_input(
        #                     f'Texto da imagem da notícia {n_tab}', 
        #                     value = st.session_state[f'brasil_news_{n_tab}_image_text'] if f'brasil_news_{n_tab}_image_text' in st.session_state else ''
        #                 )
        #                 st.write(f'{len(st.session_state[f'brasil_news_{n_tab}_image_text'])} caracteres')

        #                 # Input de imageUrl
        #                 try:
        #                     st.session_state[f'brasil_news_{n_tab}_image_url'] = image_select(
        #                         "",
        #                         images = st.session_state[f'brasil_news_{n_tab}_reference_images']['imageUrl'].tolist(),
        #                         captions = st.session_state[f'brasil_news_{n_tab}_reference_images']['imageText'].tolist(),
        #                     )
        #                 except Exception as e:
        #                     st.error(f"Erro ao carregar imagens: {e}")

        #                 # Show dataframe with references
        #                 if st.checkbox(f'Ver referências para notícia {n_tab}', value = True):
        #                     st.session_state[f'brasil_news_{n_tab}_reference_news_selected'] = st.data_editor(
        #                         st.session_state[f'brasil_news_{n_tab}_reference_news'], 
        #                         column_config={
        #                             "create": st.column_config.CheckboxColumn(
        #                                 "Criar?",
        #                             ),
        #                             "url": st.column_config.LinkColumn(
        #                                 "Link", display_text="Link",
        #                                 disabled=True
        #                             ),
        #                             "title": st.column_config.TextColumn(
        #                                 "Título",
        #                                 max_chars=100,
        #                                 disabled=True
        #                             ),
        #                         },
        #                         hide_index=True
        #                     )

        #                 if f'brasil_news_{n_tab}_reference_news_selected' in st.session_state:
        #                     if st.button(f'Gerar notícia {n_tab}'):
        #                         if f'brasil_news_{n_tab}_image_text' in st.session_state:
        #                             selection = st.session_state[f'brasil_news_{n_tab}_reference_news_selected']
        #                             st.session_state[f'brasil_news_{n_tab}_final'] = WriterNews('Brasil', 
        #                                 selection[selection['source'] == True]['text'].tolist(),
        #                                 selection[selection['source'] == True]['title'].tolist(),
        #                                 st.session_state[f'brasil_news_{i}_image_url'],
        #                                 st.session_state[f'brasil_news_{i}_image_text'])
                                    
                            
                            
        #                 if f'brasil_news_{n_tab}_final' in st.session_state:
        #                     st.write(f"**Título:** {st.session_state[f'brasil_news_{n_tab}_final'].title}")
        #                     st.write(f"**Resumo:** {st.session_state[f'brasil_news_{n_tab}_final'].summary}")
        #                     st.write(f"**Imagem:** {st.session_state[f'brasil_news_{n_tab}_final'].imageUrl}")
        #                     st.write(f"**Texto da imagem:** {st.session_state[f'brasil_news_{n_tab}_final'].imageText}")
        #                     st.write(f"**Texto:** {st.session_state[f'brasil_news_{n_tab}_final'].text}")



if __name__ == '__main__':
    rpa()


