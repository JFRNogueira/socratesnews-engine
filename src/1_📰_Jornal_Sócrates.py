import streamlit as st
from auth.sign_in import sign_in
from auth.sign_up import sign_up
from auth.authentication import authentication




# from dotenv import load_dotenv
# import os
# load_dotenv()
# API_URL = os.getenv("API_URL")


def main():
    st.set_page_config(
        page_title="Jornal Sócrates",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    st.secrets['API_URL']
    st.header('Jornal Sócrates', divider=True)
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.subheader('Painel administrativo', divider=True, help='Faça login para saber a quais funcionalidades você tem acesso')
        st.markdown('''
                    Seja bem vindo ao Painel Administrativo do Jornal Sócrates. De acordo com o seu nível de permissão, você será capaz de:
                    - [ ] Realizar publicações legais no Jornal Sócrates
                    - [ ] Realizar publicações legais no Diário Oficial da União (DOU)
                    - [ ] Realizar publicações legais nos diários oficial dos estados (DOE's)
                    - [ ] Gerenciar Seções do Jornal
                    - [ ] Gerenciar Notícias do Jornal
                    - [ ] Gerenciar Usuários
                    
                    Nosso time de suporte está disponível de segunda a sexta das 9h às 18h (horário de Brasília) através do e-mail `contato@socratesdata.com`
                    ''')
    with col2:
        authentication()
    

if __name__ == "__main__":
    main()
