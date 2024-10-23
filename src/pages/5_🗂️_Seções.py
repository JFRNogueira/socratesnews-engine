import streamlit as st

from secoes.secao_criar import secao_criar
from secoes.secao_editar import secao_editar


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
    options = ['Criar', 'Editar']
    
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio("Selecione a opção", options)

    if menu_option == "Criar":
        secao_criar()
    if menu_option == "Editar":
        secao_editar()

if __name__ == "__main__":
    main()
