import streamlit as st

from usuarios.usuario_criar import usuario_criar
from usuarios.usuario_listar import usuario_listar
from usuarios.usuario_editar import usuario_editar




def main():
    st.set_page_config(
        page_title="Usuários",
        page_icon="👤",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )
    options = ['Criar', 'Editar', 'Listar', 'Sair']
    
    if st.session_state.authenticated:
    # if not st.session_state.authenticated:
        login()
    else:
        st.sidebar.title("Menu")
        menu_option = st.sidebar.radio("Selecione a opção", options)

        if menu_option == "Criar":
            usuario_criar()
        if menu_option == "Editar":
            usuario_editar()
        if menu_option == "Listar":
            usuario_listar()
        elif menu_option == "Logout":
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
