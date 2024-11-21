# login.py
import streamlit as st
import requests
from auth.sign_in import sign_in
from auth.sign_up import sign_up
        


def printed_version():
    st.subheader('Autenticação', divider=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'user' in st.session_state:
            st.markdown(f'Bem-vindo, \n {st.session_state['user']['name']}')
            st.text_input("E-mail", value=st.session_state['user']['email'])
            st.text_area("Bio", value=st.session_state['user']['bio'])
            st.button('Sair', on_click=lambda: st.session_state.pop('user'))
        else:
            st.checkbox(
                "Já sou cadastrado", 
                key='checkbox_sign_in',
                help='Caso já tenha recebido suas credenciais de acesso por e-mail, marque o checkbox',
                value=True)
        
            if st.session_state['checkbox_sign_in']:
                sign_in()
            else:
                sign_up()
    
    with col2:
        st.markdown('Suas permissões:')
        
        if not 'user' in st.session_state:
            st.warning("Faça login ao lado para visualizar suas permissões.")
        else:
            
            if 'admin' in st.session_state['user']['roles']:
                st.markdown('- [x] Administrador')
            else:
                st.markdown('- [ ] Administrador')
                
            if 'journalist' in st.session_state['user']['roles']:
                st.markdown('- [x] Jornalista')
            else:
                st.markdown('- [ ] Jornalista')
                
            if 'legal_ads' in st.session_state['user']['roles']:
                st.markdown('- [x] Publicidade Legal')
            else:
                st.markdown('- [ ] Publicidade Legal')
                
            if 'support' in st.session_state['user']['roles']:
                st.markdown('- [x] Suporte')
            else:
                st.markdown('- [ ] Suporte')
                
            if 'reader' in st.session_state['user']['roles']:
                st.markdown('- [x] Leitor')
            else:
                st.markdown('- [ ] Leitor')


