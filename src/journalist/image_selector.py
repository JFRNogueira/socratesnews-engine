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
            response = requests.get(url, json=params)
            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
            st.markdown(url)

            if response.status_code != 200:
                print(f'Erro: {response.status_code}')
                return None, None, None, None

            newsId = response.json()['newsId']
            referenceNews = pd.DataFrame(response.json()['referenceNews'])
            referenceNews['imageUrl'] = referenceNews['imageUrl'].astype(str)
            referenceNews = referenceNews[referenceNews['imageUrl'].str.startswith('http')]
            referenceNews = pd.concat([referenceNews, pd.DataFrame([{'imageUrl': 'https://storage.googleapis.com/socrates-news.appspot.com/images/no_no_image.png', 'imageText': 'Sem imagem'}])], ignore_index=True)
            referenceNewsListUrl = referenceNews['imageUrl'].tolist()
            referenceNewsListText = referenceNews['imageText'].tolist()
            
            return newsId, referenceNews, referenceNewsListUrl, referenceNewsListText

        except Exception as e:
            print("Problema ao buscar notícia:", e)
            return None, None, None, None
    
    
    
    def show_no_image_news(self):
        news_id, news_df, url_list, text_list = self.get_no_image_news()
        st.session_state['no_image_news_newsid'] = news_id
        st.session_state['no_image_news_df'] = news_df
        st.session_state['image_src_list_url'] = url_list
        st.session_state['image_src_list_text'] = text_list
        st.session_state['aleatory_key'] = str(random.randint(1, 1000000))

        
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
        st.header('Seletor de magens')
        
        col1, col2 = st.columns([1, 5], gap='large')
        
        with col1:
            st.subheader('Buscador', divider=True)
            
            if st.button('Buscar', type='primary'):
                self.show_no_image_news()
                
            if st.checkbox('Apenas notícias com imagens', value=False):
                if 'image_src_list_url' in st.session_state and st.session_state['image_src_list_url'] != None:
                    st.markdown(st.session_state['image_src_list_url'])
                else:
                    st.warning('Não há notícias a serem listadas')
            else:
                if 'no_image_news_df' in st.session_state and st.session_state['no_image_news_df'] != None:
                    st.markdown(st.session_state['no_image_news_df'])
                else:
                    st.warning('Não há notícias com imagens a serem listadas')



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
                st.text_input('URL')
                        
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
            
            

            
            
            
            
            