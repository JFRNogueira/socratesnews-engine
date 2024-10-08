import streamlit as st

from publicidade_legal.pl_criar import pl_criar




def main():
    st.set_page_config(
        page_title="Publicidade Legal",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )
    options = ['Criar']
    
    if st.session_state.authenticated:
    # if not st.session_state.authenticated:
        login()
    else:
        st.sidebar.title("Menu")
        menu_option = st.sidebar.radio("Selecione a opção", options)

        if menu_option == "Criar":
            pl_criar()
        elif menu_option == "Logout":
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
