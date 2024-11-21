import streamlit as st
from bot_jornalista.writer_news import WriterNews
from sources.google_news import GoogleNews
from sources.google_news import GoogleNews, GoogleNewsCluster
from streamlit_image_select import image_select



def teste():
    st.title("Criador de notícias")
    
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.header('Seletor de temas', divider=True)
        
        # Look for references in Google News
        if st.button("Buscar temas no Google News"):
            st.markdown("Buscando temas no Google News...")
        if st.button("Buscar referências dos temas"):
            st.markdown("Buscando referências dos temas...")
            


    with col2:
        st.header('Curador de notícias', divider=True)
        
        col21, col22, col23 = st.columns(3)
        with col21:
            st.selectbox(label='Seção', options=['Mundo', 'Brasil'])
            st.select_slider('Taamanho do título', options=['de 5 a 10', 'de 10 a 15', 'de 15 a 20', 'de 20 a 25', 'de 25 a 30'], value='de 10 a 15')
        with col22:
            st.date_input(label='Data de publicação', format='DD-MM-YYYY')
            st.select_slider('Taamanho do preâmbulo', options=['de 5 a 10', 'de 10 a 15', 'de 15 a 20', 'de 20 a 25', 'de 25 a 30'], value='de 10 a 15')
        with col23:
            st.selectbox(label='Tema', options=['Mundo', 'Brasil'])
            st.select_slider('Taamanho da matéria', options=['de 5 a 10', 'de 10 a 15', 'de 15 a 20', 'de 20 a 25', 'de 25 a 30'], value='de 10 a 15')
        
        st.button('Sugerir matéria', type='primary')
        
        st.text_input('Título', value='Sugestão de título para a notícia')
        st.text_area('Preâmbulo', value='Sugestão de preâmbulo para a notícia')
        st.text_area('Matéria', value='Sugestão de matéria para a notícia')
        
        col21, col22 = st.columns(2)
        with col21:
            st.text_input(label='Fonte da image')
        with col22:
            st.selectbox(label='Autor', options=['Mundo', 'Brasil'])
        
        st.markdown('Selecionar imagem')
        


    with col3:
        st.header('Checagem', divider=True)



if __name__ == '__main__':
    teste()


