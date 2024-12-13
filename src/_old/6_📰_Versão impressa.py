import streamlit as st

from printedversion.pagination import pagination
from printedversion.previsao import previsao



def main():
    st.set_page_config(
        page_title="Jornal Sócrates",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    if (not 'user' in st.session_state) or (not 'admin' in st.session_state['user']['roles']):
        st.header('Versão impressa', divider=True)
        st.markdown('Área exclusiva para criação da versã impressa do jornal.')
        st.warning("Acesso negado. Para ter acesso, entre em contato com o suporte através do e-mail `contato@socratesdata.com`.", icon='⛔')
        st.stop()
        
    else:
        st.sidebar.title("Criador de páginas")
        menu_options = ['Visão geral', 'Paginação', 'Previsão']
        menu_option = st.sidebar.radio("Selecione a opção", menu_options)

        if menu_option == "Paginação":
            pagination()
        if menu_option == "Previsão":
            previsao()

if __name__ == "__main__":
    main()
