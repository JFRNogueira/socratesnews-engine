# login.py
import streamlit as st
import requests
import time





def sign_up_service(name, email):
    API_URL = f'https://socratesnews-dev-1aaab5bd4746.herokuapp.com/api/user'
    payload = {
        'name': name,
        'email': email,
        '__t': 'nonexistent'
    }
    response = requests.post(API_URL, json=payload)
    return response.status_code == 200

        
    


def sign_up():
    st.subheader('Cadastrar', divider=True, help='Se você é novo por aqui, cadastre-se na plataforma')

    # Campos de entrada para o cadastro
    st.text_input("Nome", key='auth_sign_up_name', value=st.session_state.get('auth_sign_up_name', ''))
    st.text_input("E-mail", key='auth_sign_up_email', value=st.session_state.get('auth_sign_up_email', ''))
    st.text_input("Celular com DDD (apenas números)", key='auth_sign_up_phone', value=st.session_state.get('auth_sign_up_phone', ''))

    # Botão de cadastro
    if 'auth_sign_up_name' in st.session_state and len(st.session_state['auth_sign_up_name']) >= 3:
        if st.button("Solicitar acesso"):
            if sign_up_service(st.session_state['auth_sign_up_name'], st.session_state['auth_sign_up_email']):
                keys_to_remove = ['auth_sign_up_name', 'auth_sign_up_email', 'auth_sign_up_phone']
                for key in keys_to_remove:
                    if key in st.session_state:
                        st.session_state.pop(key)
                st.success("Seu acesso será avaliado e você terá um retorno nas próximas horas. Fique atento ao seu e-mail.", icon='🎉')
                time.sleep(5)
                st.rerun()
            else:
                st.error("Algo deu errado. Contate o suporte", icon='😢')
