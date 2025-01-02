import streamlit as st
# from auth.sign_in import sign_in
# from auth.sign_up import sign_up
# from auth.authentication import authentication
from analytics.analytics import Analytics
from authentication import Authentication
from pathlib import Path

from journalist.journalist import Journalist
from users.users import Users


# Interface principal protegida
def app():
    logo_path = Path(__file__).parent / "assets" / "logo.png"
    if logo_path.exists():
        st.sidebar.image(str(logo_path), use_container_width=True)
    else:
        st.sidebar.error("Logo não encontrada no caminho especificado.")
    
    pages = ["📰 Jornalista", "👤 Usuários", "🏫 Escolas", "📊 Analytics"]
    selected_page = st.sidebar.selectbox("Página", pages)


    if selected_page == "📰 Jornalista":
        Journalist().ui()
    
    if selected_page == "👤 Usuários":
        Users().ui()
    elif selected_page == "📊 Analytics":
        Analytics().ui()
        # Schools().ui()
    elif selected_page == "Sair":
        Authentication().logout()






def main():
    st.set_page_config(
        page_title="Jornal Sócrates",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # Se usuário não está autenticado
    if not st.session_state.get("authenticated", False):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None

        # Ocultar o menu padrão do Streamlit
        hide_menu = """
            <style>
                [data-testid="stSidebarNav"] { display: none; }
            </style>
        """
        st.markdown(hide_menu, unsafe_allow_html=True)

    if st.session_state["authenticated"]:
        app()
    else:
        st.header('Jornal Sócrates', divider=True)
        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.subheader('Visão geral', divider=True, help='Faça login para saber a quais funcionalidades você tem acesso')
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
            Authentication().login_ui()
    

if __name__ == "__main__":
    main()
