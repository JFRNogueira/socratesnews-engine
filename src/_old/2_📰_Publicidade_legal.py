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
    
    if (not 'user' in st.session_state) or (not 'legal_ads' in st.session_state['user']['roles']):
        st.header('Publicidade Legal', divider=True)
        st.markdown('Área exclusiva para instituções que possuem contrato de publicidade legal com o Jornal Sócrates.')
        st.warning("Acesso negado. Para ter acesso, entre em contato com o suporte através do e-mail `contato@socratesdata.com`.", icon='⛔')
        st.stop()
        
    else:
        st.sidebar.title("Menu")
        menu_options = ['Criar', 'Gerenciar']
        menu_option = st.sidebar.radio("Selecione a opção", menu_options)

        if menu_option == "Criar":
            pl_criar()
        elif menu_option == "Gerenciar":
            pl_gerenciar()

if __name__ == "__main__":
    main()
