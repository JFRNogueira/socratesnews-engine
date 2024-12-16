import streamlit as st

from journalist.google_news_ui import GoogleNewsUi
from journalist.image_selector import ImageSelector
from journalist.infantil import infantil
from journalist.previsoes import previsoes

from journalist.rpa import RPAWriter
from journalist.fontes_pendentes import fontes_pendentes
from journalist.mundo import mundo
from journalist.brasil import brasil
from journalist.cet import cet
from journalist.economia import economia
from journalist.entretenimento import entretenimento
from journalist.esporte import esporte

from journalist.teste import teste


class Journalist:
    
    
    
    def __init__(self):
        pass
    
    
    
    def ui(self):

        # options = ['Teste', 'RPA', 'Fontes pendentes''Oração', 'Infantil', 'Previsões', 'Classificados']
        options = ['RPA - Escritor', 'Mundo', 'Brasil', 'CeT', 'Economia', 'Entretenimento', 'Esporte', 'Selecionar imagem']
        
        st.sidebar.title("Menu")
        menu_option = st.sidebar.radio("Selecione a opção", options)

        if menu_option == "RPA - Escritor":
           RPAWriter().ui()
        if menu_option == "Mundo":
            GoogleNewsUi('Mundo').ui()
        if menu_option == "Brasil":
            GoogleNewsUi('Brasil').ui()
        if menu_option == "CeT":
            GoogleNewsUi('CeT').ui()
        if menu_option == "Economia":
            GoogleNewsUi('Economia').ui()
        if menu_option == "Entretenimento":
            GoogleNewsUi('Entretenimento').ui()
        if menu_option == "Esporte":
            GoogleNewsUi('Esporte').ui()
        if menu_option == "Selecionar imagem":
            ImageSelector().ui()

        # if menu_option == "Teste":
        #     teste()
        # if menu_option == "RPA":
        #     rpa()
        # if menu_option == "Fontes pendentes":
        #     fontes_pendentes()
        # if menu_option == "CeT":
        #     cet()
        # if menu_option == "Economia":
        #     economia()
        # if menu_option == "Entretenimento":
        #     entretenimento()
        # if menu_option == "Esporte":
        #     esporte()
        # if menu_option == "Infantil":
        #     infantil()
        # if menu_option == "Previsões":
        #     previsoes()


