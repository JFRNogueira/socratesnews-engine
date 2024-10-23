import streamlit as st

from publicidade_legal.pl_criar import pl_criar
from publicidade_legal.pl_gerenciar import pl_gerenciar




def main():
    st.set_page_config(
        page_title="Jornal Sócrates",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    menu_options = ['Criar', 'Gerenciar']
    
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio("Selecione a opção", menu_options)

    if menu_option == "Criar":
        pl_criar()
    elif menu_option == "Gerenciar":
        pl_gerenciar()

if __name__ == "__main__":
    main()
