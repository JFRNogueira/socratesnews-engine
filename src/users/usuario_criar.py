import streamlit as st


def usuario_criar():
    
    st.text_input('Nome', help='Nome que será exibido para no app', key='user_name', value=st.session_state.get('user_name', ''))
    st.text_input('E-mail', help='E-mail cadastrado no Firebase', key='user_email', value=st.session_state.get('user_email', ''))
        
    st.text_input('UID', help='UID gerado no console do Firebase', key='user_uid', value=st.session_state.get('user_uid', ''))
    st.text_input('URL da imagem', help='Essa URL de imagem será chamada todas as vezes que o usuário for exibido no app', key='user_image_url', value=st.session_state.get('user_image_url', ''))
    
    st.text_input('Bio', help='Pequeno texto de até 200 caracteres que serve como uma introdução do usuário', max_chars=180, key='user_bio', value=st.session_state.get('user_bio', ''))
    
    st.multiselect('Permissões', options=['admin', 'journalist', 'reader'], help='Permissões de acesso do usuário', key='user_roles', default=st.session_state.get('user_roles', []))
    if 'journalist' in st.session_state.user_roles:
        st.multiselect('Seções permitidas', options=['Mundo', 'Brasil', 'Negócios'], help='Seções que podem ser editadas pelo usuário', key='user_journalist_sections', default=st.session_state.get('user_journalist_sections', []))
        
    if st.button('Criar usuário'):
        st.success('Usuário criado', icon='🎉')
        keys_to_remove = ['user_name', 'user_email', 'user_uid', 'user_image_url', 'user_bio', 'user_roles', 'user_journalist_sections']
        for key in keys_to_remove:
            if key in st.session_state:
                st.session_state.pop(key)
        st.rerun()
        

if __name__ == '__main__':
    usuario_criar()
    
    
    
    
