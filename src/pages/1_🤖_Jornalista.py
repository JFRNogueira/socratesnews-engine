import streamlit as st

from bot_jornalista.infantil import infantil
from bot_jornalista.previsoes import previsoes

from bot_jornalista.rpa import rpa
from bot_jornalista.fontes_pendentes import fontes_pendentes
from bot_jornalista.mundo import mundo
from bot_jornalista.brasil import brasil
from bot_jornalista.cet import cet
from bot_jornalista.economia import economia
from bot_jornalista.entretenimento import entretenimento
from bot_jornalista.esporte import esporte

from bot_jornalista.teste import teste



def main():
    st.set_page_config(
        page_title="Jornal Sócrates",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    options = ['Teste', 'RPA', 'Fontes pendentes', 'Mundo', 'Brasil', 'C&T', 'Economia', 'Entretenimento', 'Esporte', 'Oração', 'Infantil', 'Previsões', 'Classificados']
    
    if (not 'user' in st.session_state) or (not 'journalist' in st.session_state['user']['roles']):
        st.header('Jornalista', divider=True)
        st.markdown('Área exclusiva para uso de jornalistas e conta com funcionalidades auxiliares à postagem de notícias.')
        st.warning("Acesso negado. Para ter acesso, entre em contato com o suporte através do e-mail `contato@socratesdata.com`.", icon='⛔')
        st.stop()
        
    else:
        st.sidebar.title("Menu")
        menu_option = st.sidebar.radio("Selecione a opção", options)

        if menu_option == "Teste":
            teste()
        if menu_option == "RPA":
            rpa()
        if menu_option == "Fontes pendentes":
            fontes_pendentes()
        if menu_option == "Mundo":
            mundo()
        if menu_option == "Brasil":
            brasil()
        if menu_option == "C&T":
            cet()
        if menu_option == "Economia":
            economia()
        if menu_option == "Entretenimento":
            entretenimento()
        if menu_option == "Esporte":
            esporte()
        if menu_option == "Infantil":
            infantil()
        if menu_option == "Previsões":
            previsoes()

if __name__ == "__main__":
    main()
