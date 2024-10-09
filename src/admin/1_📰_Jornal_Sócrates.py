# main.py
import streamlit as st
from auth.login import login
from create_news import create_news
from list_news import list_news
from edit_news import edit_news
from printed_version import printed_version

# Inicializar o estado da sessão
if not 'authenticated' in st.session_state:
    st.session_state.authenticated = False

# Função principal para gerenciar a navegação
def main():
    st.set_page_config(
        page_title="Jornal Sócrates",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )
    
    if st.session_state.authenticated:
    # if not st.session_state.authenticated:
        login()
    else:
        st.sidebar.title("Menu")
        menu_option = st.sidebar.radio("Selecione a opção", ["Criar Notícia", "Listar Notícias", "Editar Notícia", "Bot Mundo", "Versão impressa", "Logout"])

        if menu_option == "Criar Notícia":
            create_news()
        elif menu_option == "Listar Notícias":
            list_news()
        elif menu_option == "Editar Notícia":
            edit_news()
        elif menu_option == "Versão impressa":
            printed_version()
        elif menu_option == "Logout":
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
