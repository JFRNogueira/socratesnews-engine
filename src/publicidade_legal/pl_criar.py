import streamlit as st
import streamlit.components.v1 as components
from streamlit_quill import st_quill
import math
from screeninfo import get_monitors
import os
from streamlit_extras.stylable_container import stylable_container
import requests



def create_pl(payload):
    try:
        API_URL = f'http://localhost:3000/api/news'
        res = requests.post(API_URL, json=payload)
    except:
        return False



def pl_criar():
    
    st.title("Nova publicidade legal")
    col1, col2, col3 = st.columns(3, gap='large')

    with col1:
        st.subheader('Editor de texto', divider=True)
        st.selectbox("Instituição", options=['Instituição que vem do perfil'], index=0, disabled=True)
        content = st_quill(
            placeholder="Escreva aqui...", 
            html=True
        )
        

    with col2:
        st.subheader('Pré-visualização', divider=True)
            
        if len(content) == 0 or content == '<p><br></p>':
            st.markdown('Escreva algo no editor de texto ao lado')
        else:
            st.session_state['pl_diagonal_in_inches'] = 15.5
            
            st.session_state['pl_diagonal_in_inches'] = float(st.text_input(
                    'Tamanho do monitor em polegadas', 
                    help='Necessário para melhor visualizar como ficará a versão impressa da publicidade legal',
                    value = st.session_state['pl_diagonal_in_inches']
                    ).replace(',', '.'))
            st.session_state['pl_n_columns'] = 1

            for monitor in get_monitors():
                width = monitor.width
                height = monitor.height
                
                # Calcula a diagonal em pixels
                diagonal_in_pixels = math.sqrt(width**2 + height**2)
                
                # Calcula PPI
                ppi = diagonal_in_pixels / st.session_state['pl_diagonal_in_inches']
                
                # Convertendo pixels para cm
                width_cm = (width / ppi) * 2.54
                height_cm = (height / ppi) * 2.54
            
            width_pixels = width * 5 * st.session_state['pl_n_columns'] / width_cm
            
            css_file_path = os.path.join(os.getcwd(), 'src', 'admin', 'publicidade_legal', 'ql_editor.css')

            # Ler o conteúdo do arquivo CSS e verificar se o arquivo existe
            if os.path.exists(css_file_path):
                with open(css_file_path) as f:
                    quill_css = f"<style>{f.read()}</style>"
                    st.markdown(quill_css, unsafe_allow_html=True)
            else:
                st.error(f"CSS file not found: {css_file_path}")
            
            st.write('Caso deseje alterar algo, utilize o editor de texto')

            # Injetar o conteúdo com a formatação
                # <div id="pl_content" style="width: {width_pixels}px; border: 1px solid black; padding: 0px; margin: 0">
            markdown_str = f"""
                <div style="width: {width_pixels}px; border: 1px solid black">
                    <div id="pl_content" style="margin:-15px 0px">
                        {content}
                    </div>
                </div>
                <script>
                    window.addEventListener('load', function() {{
                        const element = document.getElementById('pl_content');
                        let elHeight = element.offsetHeight / {ppi} * 2.54;
                        elHeight = Math.ceil(elHeight * 10) / 10;
                        document.getElementById('height-info').innerText = 'Altura aproximada em centímetros: ' + elHeight.toFixed(1) + ' cm';
                    }});
                </script>
                <div id="height-info"></div>
                """
            st.markdown(markdown_str, unsafe_allow_html=True)
            components.html(markdown_str)
            
        with col3:
            st.subheader("Publicar em:", divider=True)
            if len(content) == 0 or content == '<p><br></p>':
                st.markdown('Escreva algo no editor de texto ao lado')
            else:
                st.checkbox("DOU - Diário Oficial da União", value=True, key='publicar_dou')
                st.checkbox("DOE - Diário Oficial do Estado", value=True, key='publicar_doe')
                st.checkbox("Jornal de Grande Circulação - Jornal Sócrates", value=True, key='publicar_jgc')
                
                if st.button("Publicar publicidade legal"):
                    # st.markdown(f'DOU: {st.session_state['publicar_dou']}')
                    # st.markdown(f'DOE: {st.session_state['publicar_doe']}')
                    if st.session_state['publicar_jgc']:
                        st.markdown("Publicidade legal publicada com sucesso no Jornal Sócrates")
                        payload = {
                            'supportUid': 'aKwP8Bwx34fW18Rkqr4u31uYoQ23',
                            'uid': 'aKwP8Bwx34fW18Rkqr4u31uYoQ23',
                            "h1": 'Instituição que vem do perfil',
                            "text": content,
                            # autor e publishedAt
                            # "imageUrl": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                            "sectionName": "Publicidade Legal"
                            }
                        st.json(payload)
                        create_pl(payload)
                    else:
                        st.markdown("Não há o que publicar")
                
                
            
            


if __name__ == '__main__':
    pl_criar()
    
    
    
    
  