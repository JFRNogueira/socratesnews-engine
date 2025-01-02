import math
import random
import time
import streamlit as st
import pandas as pd
import requests
from streamlit_image_select import image_select



class ImageSelector:
    
    
    
    def __init__(self):
        pass
    
    
    
    def get_no_image_news(self):
        try:
            url = f'{st.secrets["API_URL"]}api/noimagenews'
            params = {
                "uid": st.secrets['SUPPORT_UID'],
                "supportUid": st.secrets['SUPPORT_UID'],
            }
            response = requests.get(url, params=params)

            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
                return None, None, None, None

            newsId = response.json()['newsId']
            referenceNews = pd.DataFrame(response.json()['referenceNews'])
            referenceNewsListUrl = referenceNews[referenceNews['imageUrl'].notna()]['imageUrl'].tolist()
            referenceNewsListText = referenceNews[referenceNews['imageUrl'].notna()]['imageText'].tolist()
            
            return newsId, referenceNews, referenceNewsListUrl, referenceNewsListText

        except Exception as e:
            print("Problema ao buscar notícia:", e)
            return None, None, None, None
    
    
    
    def update_image_news(self, newsId, imageUrl):
        try:
            url = f'{st.secrets["API_URL"]}api/news/{newsId}'
            payload = {
                "uid": st.secrets['SUPPORT_UID'],
                "supportUid": st.secrets['SUPPORT_UID'],
                "imageUrl": imageUrl,
            }
            response = requests.patch(url, json=payload)

            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
                return None

            # Garantir que a resposta é uma lista
            return response.json()

        except Exception as e:
            print("Problema ao buscar notícia:", e)
            return None
    
    
    
    def ui(self):
        st.header('Seletor de imagens')
        
        col1, col2 = st.columns([1, 3], gap='large')
        
        with col1:
            st.subheader('Google News', divider=True)
            
            if st.button('Buscar notícias'):
                a, b, c, d = self.get_no_image_news()
                st.session_state['no_image_news_newsid'] = a
                st.session_state['no_image_news_df'] = b
                st.session_state['image_src_list_url'] = c
                st.session_state['image_src_list_text'] = d
                st.session_state['aleatory_key'] = str(random.randint(1, 1000000))
                
            if st.checkbox('Todas as notícias', value=False):
                st.dataframe(st.session_state['no_image_news_df'])
            if st.checkbox('Notícias com imagens', value=False):
                # st.dataframe(st.session_state['image_src_list_url'])
                st.markdown(st.session_state['image_src_list_url'])
 
        with col2:
            st.subheader('Selecionar imagem', divider=True)
            
            col21, col22 = st.columns(2)
            
            with col21:
                if st.button('Salvar imagem', type='primary'):
                    # Verificar se a lista não está vazia
                    if st.session_state['image_src_list_url']:
                        # Garantir que o índice selecionado é válido
                        if st.session_state.get(f'image_source_url_{st.session_state['aleatory_key']}', 0) < len(st.session_state['image_src_list_url']):
                            st.session_state['image_source_url_selected'] = st.session_state['image_src_list_url'][st.session_state.get(f'image_source_url_{st.session_state['aleatory_key']}', 0)]

                            # Chamar a função de atualização
                            self.update_image_news(
                                st.session_state['no_image_news_newsid'],
                                st.session_state.get('image_source_url_selected', '')
                            )
                            st.success('Imagem salva com sucesso!')
                        else:
                            st.error("Índice selecionado inválido!")
                    else:
                        st.error("Nenhuma imagem disponível para salvar!")
                        
            with col22:
                st.file_uploader('Upload de imagem', key='image_upload')
        
            try:
                image_select(
                    "",
                    images = st.session_state['image_src_list_url'],
                    captions = st.session_state['image_src_list_text'],
                    key=f'image_source_url_{st.session_state['aleatory_key']}'
                )
            
            
            except Exception as e:
                st.error(f"Erro ao carregar imagens: {e}")
            
            

            
            
            
            
            