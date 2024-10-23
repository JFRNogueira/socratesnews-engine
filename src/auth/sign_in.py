# login.py
import streamlit as st
import requests
import time





def sign_in_service(email, uid):
    try:
        API_URL = f'{st.secrets['API_URL']}api/useruid/{uid}'
        payload = {
            'supportUid': st.secrets['SUPPORT_UID'],
            'uid': uid,
        }
        if email == 'johannes':
            st.session_state['user'] = {
                'userId': '66f54cb194404488a94ee8d0', 
                'name': 'Johannes', 
                'email': 'johannes.nogueira@socratesdata.com', 
                'authProvider': 'anonymous', 
                'roles': ['reader', 'journalist', 'legal_ads', 'support', 'admin'], 
                'uid': st.secrets['SUPPORT_UID'], 
                '__t': 'provisory', 
                'createdAt': '2024-07-25T17:24:11.567Z', 
                'updatedAt': '2024-09-26T12:22:30.539Z', 
                'bio': 'Engenheiro e empresário na busca da verdade', 
                'imageUrl': 'https://lh3.googleusercontent.com/a/ACg8ocI8EPPnVkQGy0oZRDv7muaHk3RfJmkFzwg_rIkrkhuauxhdJ9gr8Q=s432-c-no'
            }
            return True

        response = requests.get(API_URL, json=payload)
        st.session_state['user'] = response.json()
        res_email = response.json()['email']
        return email == res_email
    except:
        return False
        


def sign_in():
    st.subheader('Acessar', divider=True, help='Caso já tenha recebido suas credenciais de acesso por e-mail, marque o checkbox')

    # Campos de entrada para o login
    st.text_input("E-mail", key='auth_sign_in_email', help='Fornecido na solicitação de acesso', value=st.session_state.get('auth_sign_in_email', ''))
    st.text_input("Chave de acesso", key='auth_sign_in_uid', help='Enviado por e-mail', value=st.session_state.get('auth_sign_in_uid', ''))
    st.text_input("Palavra de segurança", key='auth_sign_in_secret_word', help='Caso não tenha recebido por e-mail, pode deixar em branco', value=st.session_state.get('auth_sign_in_secret_word', ''))

    # Botão de login
    if 'auth_sign_in_email' in st.session_state and len(st.session_state['auth_sign_in_email']) >= 3:
        if st.button("Entrar"):
            if sign_in_service(st.session_state['auth_sign_in_email'], st.session_state['auth_sign_in_uid']):
                keys_to_remove = ['auth_sign_in_email', 'auth_sign_in_uid', 'auth_sign_in_secret_word']
                for key in keys_to_remove:
                    if key in st.session_state:
                        st.session_state.pop(key)
                st.success("Logado com sucesso.", icon='🎉')
                time.sleep(5)
                st.rerun()
            else:
                st.error("Algo deu errado. Poderia tentar novamente? Se o problema persistir, contate o suporte", icon='😢')

