# login.py
import base64
import shutil
import streamlit as st
from streamlit_image_select import image_select
import os
import utils.services as services
import pandas as pd
import subprocess
import json

from PIL import Image, ImageDraw
import requests
from io import BytesIO

import printedversion.layouts.src_builder as src_builder





def create_tex_src():
    if st.session_state['printed_version_layout'] == 0:
        src_builder.SrcBuilder().model1()
    elif st.session_state['printed_version_layout'] == 1:
        src_builder.SrcBuilder().model2()
    elif st.session_state['printed_version_layout'] == 2:
        src_builder.SrcBuilder().model3()



def display_pdf(file_path):
    # Abrir o PDF usando um iframe
    with open(file_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    
    # Exibir o PDF em um iframe
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="450" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)



def save_content():
    img = st.session_state['printed_version_news_adaption_img']
    index = st.session_state['printed_version_news_adaption_index']
    img_cropped = img.crop([
        st.session_state.get('printed_version_news_adaption_image_x', 10), 
        st.session_state.get('printed_version_news_adaption_image_y', 20), 
        st.session_state.get('printed_version_news_adaption_image_x', 10) + st.session_state.get('printed_version_news_adaption_image_size', 30), 
        st.session_state.get('printed_version_news_adaption_image_y', 20) + st.session_state.get('printed_version_news_adaption_image_size', 30)])
    img_cropped.save(f'./src/printedversion/pages/{st.session_state['printed_version_page_number'].replace('Página ', '') }/news{index+1}.png')
    
    # Abrir arquivo json, alterar o valor da chave 'imageUrl' e salvar novamente
    json_file = f'./src/printedversion/pages/{st.session_state["printed_version_page_number"].replace("Página ", "")}/src.json'
    if not os.path.exists(json_file):
        try:
            path_template = f'./src/printedversion/pages/params/src.json'
            shutil.copy(path_template, json_file)
        except Exception as e:
            print(f"An error occurred: {e}")
            
    with open(json_file, 'r', encoding='utf8') as f:
        src_json = json.load(f)
        src_json['news'][index]['title'] = st.session_state['printed_version_news_adaption_title']
        src_json['news'][index]['summary'] = st.session_state['printed_version_news_adaption_summary']
        src_json['news'][index]['text'] = st.session_state['printed_version_news_adaption_text']
        src_json['news'][index]['imagePath'] = f'./src/printedversion/pages/{st.session_state['printed_version_page_number'].replace('Página ', '') }/news{index+1}.png'
        f.close()
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(src_json, f, ensure_ascii=False, indent=4)
        f.close()



def cut_image(url, index):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    st.session_state['printed_version_news_adaption_img'] = img
    width, height = img.size
    initial_x = (width - min(width, height))//2
    initial_y = (height - min(width, height))//2
    
    st.slider('X inicial', min_value=0, max_value=width, step=1, value=initial_x, key='printed_version_news_adaption_image_x')
    st.slider('Y inicial', min_value=0, max_value=height, step=1, value=initial_y, key='printed_version_news_adaption_image_y')
    st.slider('Tamanho', min_value=0, max_value=min(width, height), value=min(width, height), step=1, key='printed_version_news_adaption_image_size')
    
    img_with_square = img.copy()
    draw = ImageDraw.Draw(img_with_square)
    draw.rectangle(
        [st.session_state.get('printed_version_news_adaption_image_x', 10), 
        st.session_state.get('printed_version_news_adaption_image_y', 20), 
        st.session_state.get('printed_version_news_adaption_image_x', 10) + st.session_state.get('printed_version_news_adaption_image_size', 30), 
        st.session_state.get('printed_version_news_adaption_image_y', 20) + st.session_state.get('printed_version_news_adaption_image_size', 30)], 
        outline="red", width=3)
    st.image(img_with_square, use_column_width=True)



def get_header(header, index):
    st.text_input('Header da notícia', value=header, key=f'printed_version_news_adaption_header')
    if st.button('Salvar'):
        st.success(f'`news_{index}.png` salvo com sucesso!', icon='✅')



def get_image_files_from_directory(directory='C:/jn/news/socratesnews-engine/src/printedversion/layouts', extensions=[".png", ".jpg", ".jpeg"]):
    images = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in extensions]
    image_paths = [os.path.join(directory, img) for img in images]
    return image_paths



def pagination():
   
    if 'printed_version_news' not in st.session_state:
        st.session_state['printed_version_news'] = pd.DataFrame()
    
    sections = services.Services.get_sections()
    sections_str = [section['sectionName'] for section in sections]

    if 'h1_str' not in st.session_state:
        st.session_state['h1_str'] = ['']

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader('Parâmetros', divider=True)
        st.date_input('Data da edição', key='printed_version_date')
        st.selectbox('Número da página', options=[f'Página {i}' for i in range(1, 41)], key='printed_version_page_number')
        st.text_input('Título da página', key='printed_version_page_title')
        image_select(
            "Layout", 
            images=get_image_files_from_directory(),
            use_container_width=False,
            key='printed_version_layout',
        )
        
        
        
    with col2:
        st.subheader('Seleção de conteúdos', divider=True)
        
        if st.button('Reiniciar'):
            st.session_state['printed_version_news'] = pd.DataFrame()

        st.selectbox('Seção', options=sections_str, key='printed_version_section')
        if st.button('Buscar conteúdo'):
            sectionId = [section['sectionId'] for section in sections if section['sectionName'] == st.session_state['printed_version_section']][0]
            news = services.Services.get_news_by_section(sectionId)
            st.session_state['h1_str'] = news['h1'].tolist()
            st.session_state['news_df'] = news  # Armazenar o DataFrame com as notícias encontradas
        
        st.selectbox('Conteúdo', options=st.session_state['h1_str'], key='printed_version_h1')
        if st.button('Adicionar'):
            h1_news = st.session_state['news_df'].loc[st.session_state['news_df']['h1'] == st.session_state['printed_version_h1']]
            st.session_state['printed_version_news'] = pd.concat([st.session_state['printed_version_news'], h1_news])
            st.session_state['printed_version_news'].reset_index(drop=True, inplace=True)
        
        st.markdown('Lista de notícias da página:')
        st.dataframe(st.session_state['printed_version_news'])
    
    
    
    with col3:
        st.subheader('Adaptação de conteúdos', divider=True)
        st.selectbox('Conteúdo', options=st.session_state['printed_version_news']['h1'].tolist(), key='printed_version_news_adaption')
        news_adaption = st.session_state['printed_version_news'].loc[st.session_state['printed_version_news']['h1'] == st.session_state['printed_version_news_adaption']]
        st.session_state['printed_version_news_adaption_index'] = news_adaption.index[0]
        
        tab1, tab2, tab3, tab4 = st.tabs(["Header", "Preâmbulo", "Texto", "Imagem"])
        
        with tab1:
            st.text_area('Título da notícia', value=news_adaption['h1'].tolist()[0], key=f'printed_version_news_adaption_title')
        with tab2:
            st.text_area('Preâmbulo', value=news_adaption['summary'].tolist()[0], key=f'printed_version_news_adaption_summary')
        with tab3:
            news_text = services.Services.get_news_by_id(news_adaption['newsId'].tolist()[0])['text']
            st.text_area('Texto', value=news_text, key=f'printed_version_news_adaption_text')
        with tab4:
            cut_image(news_adaption['imageUrl'].tolist()[0], news_adaption.index[0])
        
        if st.button('Salvar'):
            save_content()
            st.success(f'Notícia {news_adaption.index[0]+1} salva com sucesso!', icon='✅')


    
    
    
    with col4:
        st.subheader('Pré-visualização', divider=True)
        if st.button('Pré-visualizar'):
            try:
                create_tex_src()
                tex_path = f'{os.getcwd()}/src/printedversion/pages/{st.session_state['printed_version_page_number'].replace('Página ', '')}/page_src.tex'
                pdf_path = f'{os.getcwd()}/src/printedversion/pages/{st.session_state['printed_version_page_number'].replace('Página ', '')}/'
                result = subprocess.run(f"pdflatex -synctex=1 -interaction=nonstopmode -output-directory={pdf_path} {tex_path}")
                result = subprocess.run(f"pdflatex -synctex=1 -interaction=nonstopmode -output-directory={pdf_path} {tex_path}")
                
                # Exibe logs de compilação
                if result.returncode == 0:
                    display_pdf(pdf_path + 'page_src.pdf')
                    st.toast("Compilação bem-sucedida!", icon='🎉')
                    
                else:
                    st.error("Erro na compilação!")
                    st.text(result.stderr)
            
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
    
    
                
    
    
    