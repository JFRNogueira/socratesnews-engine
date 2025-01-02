import streamlit as st

from analytics.found_sites import FoundSites
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


class Analytics:
    
    
    
    def __init__(self):
        pass
    
    
    
    def ui(self):

        options = ['Sites buscados', 'Sites pendentes']
        
        st.sidebar.title("Menu")
        menu_option = st.sidebar.radio("Selecione a opção", options)

        if menu_option == "Sites buscados":
           FoundSites().ui()
        if menu_option == "Sites pendentes":
            GoogleNewsUi('Mundo').ui()



