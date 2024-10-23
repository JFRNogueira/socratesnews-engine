import streamlit as st

from analytics.an_coverage import an_coverage




def main():
    st.set_page_config(
        page_title="Jornal Sócrates",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    menu_options = ['Cobertura']
    
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio("Selecione a opção", menu_options)

    if menu_option == "Cobertura":
        an_coverage()
    elif menu_option == "Gerenciar":
        an_coverage()

if __name__ == "__main__":
    main()
