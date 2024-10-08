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
            st.text_input('Nome', help='Nome que será exibido para no app')
            st.text_input('URL da imagem', help='Essa URL de imagem será chamada todas as vezes que o usuário for exibido no app')
        
        with col12:
            st.text_input('UID', help='UID gerado no console do Firebase')
            st.text_input('E-mail', help='E-mail cadastrado no Firebase')
        
        st.text_area('Bio', help='Pequeno texto de até 200 caracteres que serve como uma introdução do usuário', max_chars=200)
        
        st.button('Criar usuário')
        

    with col2:
            
        st.subheader("Publicar em:")
        st.checkbox("DOU - Diário Oficial da União", value=True, key='publicar_dou')
        st.checkbox("DOE - Diário Oficial do Estado", value=True, key='publicar_doe')
        st.checkbox("Jornal de Grande Circulação - Jornal Sócrates", value=True, key='publicar_jgc')




if __name__ == '__main__':
    usuario_criar()
    
    
    
    
