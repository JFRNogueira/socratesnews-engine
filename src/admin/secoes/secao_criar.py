import streamlit as st
import requests
from datetime import datetime



def create_section_service():
    API_URL = f'{st.secrets['API_URL']}api/section'
    
    data_from = st.session_state['section_from_date']
    data_from_str = datetime(data_from.year, data_from.month, data_from.day, 0, 0, 0, 0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+00:00"
    
    data_to = st.session_state['section_to_date']
    data_to_str = datetime(data_to.year, data_to.month, data_to.day, 0, 0, 0, 0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+00:00"
    
    payload = {
        'supportUid': 'aKwP8Bwx34fW18Rkqr4u31uYoQ23',
        'uid': 'aKwP8Bwx34fW18Rkqr4u31uYoQ23',
        "sectionName": st.session_state['section_name'],
        "priority": st.session_state['section_priority'],
        "active": st.session_state['section_active'],
        "fromDate": data_from_str,
        "toDate": data_to_str
    }
    response = requests.post(API_URL, json=payload)
    return response.status_code == 200



def secao_criar():
    
    col1, col2 = st.columns(2)

    with col1:
        st.title("Criar seção")
        col11, col12 = st.columns(2)
        
        with col11:
            st.text_input('Nome', help='Nome que será exibido para no app', key='section_name')
            st.checkbox('Ativar', help='Seção estará ativa após a criação', key='section_active')
        
        with col12:
            st.date_input('De', help='Data inicial de apresentação da seção no Jornal', key='section_from_date')
            st.date_input('Até', help='Data final de apresentação da seção no Jornal', key='section_to_date')
        
        st.select_slider('Prioridade', options=list(range(11)) + [1000], help='ordem crescente de apresentação da seção no Jornal', key='section_priority')
        
        if st.button('Criar seção'):
            service = create_section_service()
            if service:
                st.toast("Seção criada com sucesso", icon='🎉')
                keys_to_remove = ['section_name', 'section_from_date', 'section_to_date', 'section_priority']
                for key in keys_to_remove:
                    if key in st.session_state:
                        st.session_state.pop(key)
            else:
                st.error("Erro ao criar seção", icon='⚠️')
            
        

    with col2:
            
        st.header("Seção a ser criada")
        if 'section_name' in st.session_state:
            st.write(f"Nome: {st.session_state['section_name']}")
        if 'section_from_date' in st.session_state:
            st.write(f"De {st.session_state['section_from_date']} até {st.session_state['section_to_date']}")
        if 'section_priority' in st.session_state:
            st.write(f"Prioridade: {st.session_state['section_priority']}")
        
        st.write("Após criada a seção, os dados poderão ser editados na aba 'Editar'")
        
            



if __name__ == '__main__':
    secao_criar()
    
    
    
    
