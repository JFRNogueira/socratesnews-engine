import streamlit as st
from usuarios.usuario_criar import usuario_criar


def main():
    st.set_page_config(
        page_title="Jornal Sócrates",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    if (not 'user' in st.session_state) or (not 'admin' in st.session_state['user']['roles']):
        st.header('Usuários', divider=True)
        st.markdown('Área exclusiva para gerenciamento de permissões e acessos.')
        st.warning("Acesso negado. Para ter acesso, entre em contato com o suporte através do e-mail `contato@socratesdata.com`.", icon='⛔')
        st.stop()
        
    else:
        options = ['Criar', 'Editar']
    
        st.sidebar.title("Menu", )
        menu_option = st.sidebar.radio("Selecione a opção", options)

        if menu_option == "Criar":
            usuario_criar()
        elif menu_option == "Editar":
            st.warning("Em construção", icon='🏗️')
        # if menu_option == "Listar":
        #     usuario_listar()

if __name__ == "__main__":
    main()
