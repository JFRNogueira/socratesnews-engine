import streamlit as st
from streamlit_quill import st_quill
import math
from screeninfo import get_monitors
import os
from streamlit_extras.stylable_container import stylable_container


def usuario_criar():
    
    col1, col2 = st.columns(2)

    with col1:
        st.title("Criar usuário")
        st.subheader('Passo 1')
        st.markdown('Criar usuário com e-mail e senha no console do Firebase e anotar o UID gerado')
        st.subheader('Passo 2')
        
        col11, col12 = st.columns(2)
        
        with col11:
            st.text_input('Nome', help='Nome que será exibido para no app', key='user_name')
            st.text_input('URL da imagem', help='Essa URL de imagem será chamada todas as vezes que o usuário for exibido no app', key='user_image_url')
        
        with col12:
            st.text_input('UID', help='UID gerado no console do Firebase', key='user_uid')
            st.text_input('E-mail', help='E-mail cadastrado no Firebase', key='user_email')
        
        st.text_area('Bio', help='Pequeno texto de até 200 caracteres que serve como uma introdução do usuário', max_chars=200, key='user_bio')
        
        st.multiselect('Permissões', options=['admin', 'journalist', 'reader'], help='Permissões de acesso do usuário', key='user_roles')
        if 'journalist' in st.session_state.user_roles:
            st.multiselect('Seções permitidas', options=['Mundo', 'Brasil', 'Negócios'], help='Seções que podem ser editadas pelo usuário', key='user_journalist_sections')
        
        st.button('Criar usuário')
        

    with col2:
            
        st.subheader("Publicar em:")
        st.checkbox("DOU - Diário Oficial da União", value=True, key='publicar_dou')
        st.checkbox("DOE - Diário Oficial do Estado", value=True, key='publicar_doe')
        st.checkbox("Jornal de Grande Circulação - Jornal Sócrates", value=True, key='publicar_jgc')




if __name__ == '__main__':
    usuario_criar()
    
    
    
    
