import streamlit as st
from users.usuario_criar import usuario_criar


class Users:
    
    
    
    def __init__(self):
        pass
    
    
    
    def ui(self):
        options = ['Visualizar', 'Sair']
        
        st.sidebar.title("Menu", )
        menu_option = st.sidebar.radio("Selecione a opção", options)

        if menu_option == "Visualizar":
            col1, col2 = st.columns([3,1])
            with col1:
                st.header("Usuários", divider=True)
                st.subheader("Visualize e gerencie os usuários do sistema.")
            with col2:
                st.header("Adicionar", divider=True)
                usuario_criar()
        elif menu_option == "Sair":
            st.warning("Em construção", icon='🏗️')



