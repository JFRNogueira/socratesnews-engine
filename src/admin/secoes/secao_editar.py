import streamlit as st
import requests
import pandas as pd

def get_section_service():
    API_URL = f'{st.secrets['API_URL']}api/section/alldata'
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()  # Converte o corpo da resposta em JSON
        df = pd.DataFrame(data)  # Cria o DataFrame a partir dos dados JSON
        st.session_state['secoes_lista'] = df[['active', 'sectionName', 'fromDate', 'toDate', 'priority', 'sectionId']]
        st.session_state['secoes_lista_editor'] = st.session_state['secoes_lista'].copy()
        return df
    else:
        st.error(f"Erro na requisição: {response.status_code}")
        return pd.DataFrame()

def update_section_service(df):
    try:
        API_URL = f'{st.secrets['API_URL']}api/section'
        for index, row in df.iterrows():
            payload = {
                'supportUid': 'aKwP8Bwx34fW18Rkqr4u31uYoQ23',
                'uid': 'aKwP8Bwx34fW18Rkqr4u31uYoQ23'
            }
            # Apenas adiciona os campos modificados ao payload
            for col in ['active', 'sectionName', 'fromDate', 'toDate', 'priority']:
                if row[col] is not None and not pd.isna(row[col]):
                    payload[col] = row[col]
            
            payload['sectionId'] = row['sectionId']
            response = requests.patch(API_URL, json=payload)
            st.write(f'Status code para sectionId {row["sectionId"]}: {response.status_code}')
        
        return True
    
    except Exception as e:
        st.error(f"Erro na requisição: {e}")
        return False

def secao_editar():
    st.title("Editar seções")
    
    # Carregar e mostrar o DataFrame original
    if st.button("Listar seções") or 'secoes_lista' not in st.session_state:
        get_section_service()
    
    # Exibir editor para o DataFrame clonado
    edited_df = st.data_editor(
        st.session_state['secoes_lista_editor'],
        hide_index=True,
        column_config={'sectionId': st.column_config.TextColumn(disabled=True)}
    )
    
    # Verificar mudanças entre o DataFrame original e o editado
    if not edited_df.equals(st.session_state['secoes_lista']):
        st.subheader("Alterações realizadas")
        changed_rows = edited_df[edited_df != st.session_state['secoes_lista']].dropna(how='all')
        
        # Atualizar o `sectionId` dos registros alterados
        changed_rows['sectionId'] = st.session_state['secoes_lista'].loc[changed_rows.index, 'sectionId']
        
        st.dataframe(changed_rows)
        
        # Salvar alterações
        if st.button("Salvar alterações"):
            if update_section_service(changed_rows):
                st.success("Seções atualizadas com sucesso!", icon='🎉')
                # Atualizar o DataFrame original com as alterações para manter o editor ativo
                st.session_state['secoes_lista'].update(changed_rows)
                st.session_state['secoes_lista_editor'] = st.session_state['secoes_lista'].copy()
                st.rerun()
            else:
                st.error("Erro ao atualizar seções", icon='⚠️')

if __name__ == '__main__':
    secao_editar()
