import streamlit as st
from streamlit_quill import st_quill
import math
from screeninfo import get_monitors
import os
from streamlit_extras.stylable_container import stylable_container


def usuario_listar():
    
    col1, col2 = st.columns(2)

    with col1:
        st.title("Crie sua publicação aqui")

        toolbar_options = [
            ['bold', 'italic', 'underline', 'strike'],  # Botões de formatação de texto
            ['blockquote', 'code-block'],  # Botões de citação e código
            [{'header': 1}, {'header': 2}],  # Tamanhos de cabeçalhos
            [{'list': 'ordered'}, {'list': 'bullet'}],  # Listas ordenadas e com marcadores
            [{'indent': '-1'}, {'indent': '+1'}],  # Recuo
            [{'color': []}, {'background': []}],  # Cores de texto e fundo
            ['link', 'image'],  # Links e imagens
            ['clean']  # Botão para limpar a formatação
        ]
        content = st_quill(
            placeholder="Escreva aqui...", 
            html=True
        )
        st.write(content, unsafe_allow_html=False)
        

    with col2:
        if content:
            st.markdown("### Pré-visualização do Conteúdo")
            
            st.session_state['pl_diagonal_in_inches'] = 15.5
            
            st.session_state['pl_diagonal_in_inches'] = float(st.text_input(
                    'Tamanho do monitor em polegadas', 
                    help='Necessário apenas para melhor visualização de como ficará a versão impressa da publicidade legal',
                    value = st.session_state['pl_diagonal_in_inches']
                    ).replace(',', '.'))
            st.session_state['pl_n_columns'] = st.radio(
                "Número de colunas",
                (1, 2, 3, 4)
            )

            for monitor in get_monitors():
                width = monitor.width
                height = monitor.height
                
                # Calcula a diagonal em pixels
                diagonal_in_pixels = math.sqrt(width**2 + height**2)
                
                # Calcula PPI
                ppi = diagonal_in_pixels / st.session_state['pl_diagonal_in_inches']
                
                # Convertendo para cm
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

            # Injetar o conteúdo com a formatação
            markdown_str = f"""
                <div style="width: {width_pixels}px; border: 1px solid black; padding: 5px;">
                    {content}
                </div>
                """
            st.markdown(
                markdown_str,
                unsafe_allow_html=True,
            )
            
            st.subheader("Publicar em:")
            st.checkbox("DOU - Diário Oficial da União", value=True, key='publicar_dou')
            st.checkbox("DOE - Diário Oficial do Estado", value=True, key='publicar_doe')
            st.checkbox("Jornal de Grande Circulação - Jornal Sócrates", value=True, key='publicar_jgc')
            
            if st.button("Publicar publicidade legal"):
                st.markdown(f'DOU: {st.session_state['publicar_dou']}')
                st.markdown(f'DOE: {st.session_state['publicar_doe']}')
                st.markdown(f'JGC: {st.session_state['publicar_jgc']}')
            
            
            
            


if __name__ == '__main__':
    usuario_listar()
    
    
    
    
  