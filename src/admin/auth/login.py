# login.py
import streamlit as st
import requests

def authenticate(email, uid):
    API_URL = f'https://socratesnews-dev-1aaab5bd4746.herokuapp.com/api/useruid/{uid}'
    response = requests.get(API_URL)
    res_email = response.json()['email']
    return email == res_email
        


def login():
    st.title("Login")

    # Campos de entrada para o login
    email = st.text_input("E-mail")
    uid = st.text_input("ID")
    security_word = st.text_input("Palavra de segurança")

    # Botão de login
    if st.button("Entrar"):
        # Lógica de autenticação simples (substitua pela sua lógica)
        if authenticate(email, uid):
            st.session_state.authenticated = True
            st.session_state.uid = uid
            st.success("Login bem-sucedido!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
