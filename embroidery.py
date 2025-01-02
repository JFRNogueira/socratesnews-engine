import cv2
import numpy as np
from PIL import Image
import os
import streamlit as st


class Embroidery:
    
    
    
    def __init__(self):
        pass
    
    
    
    def extract_main_silhouette(self):
        threshold1_value = st.session_state['threshold1']
        threshold2_value = st.session_state['threshold2']
        blurred_value = st.session_state['blurred']
        area_threshold_value = st.session_state['area_threshold']
        
        input_image_path = 'perfil-jn-input.png'
        output_image_path = 'perfil-jn-output.png'
        
        # Verificar se o arquivo existe
        if not os.path.exists(input_image_path):
            raise FileNotFoundError(f"O arquivo não foi encontrado: {input_image_path}")
        
        # Carregar a imagem
        img = cv2.imread(input_image_path)
        if img is None:
            raise ValueError(f"Erro ao carregar a imagem: {input_image_path}")
        
        # Converter para escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Aplicar um desfoque para reduzir detalhes menores
        blurred = cv2.GaussianBlur(gray, (blurred_value, blurred_value), 0)
        
        # Detectar bordas usando Canny
        edges = cv2.Canny(blurred, threshold1=threshold1_value, threshold2=threshold2_value)
        
        # Fechar lacunas nas bordas (dilatação seguida de erosão)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        # Salvar o resultado das bordas para análise (opcional)
        cv2.imwrite("debug_edges.jpg", closed_edges)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Verificar quantos contornos foram encontrados
        print(f"Número de contornos encontrados: {len(contours)}")
        
        # Criar uma imagem em branco para desenhar os contornos
        silhouette = np.zeros_like(gray)
        
        # Filtrar e desenhar contornos (área mínima ajustável)
        area_threshold = area_threshold_value  # Ajuste inicial para evitar perder contornos
        for contour in contours:
            if cv2.contourArea(contour) > area_threshold:
                # Desenhar contornos preenchidos
                cv2.drawContours(silhouette, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        
        # Suavizar os traços da silhueta
        silhouette = cv2.GaussianBlur(silhouette, (5, 5), 0)
        
        # Salvar a imagem final
        cv2.imwrite(output_image_path, silhouette)
        
    
    
    def ui(self):
        st.set_page_config(
            page_title="Embroidery",
            page_icon="🪡",
            layout="wide",
            initial_sidebar_state="expanded",
        )
            
        st.title("🪡 Embroidery")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader('Imagem original', divider=True)
            st.image("perfil-jn-input.png", use_container_width=True)
        
        with col2:
            st.subheader('Parâmetros', divider=True)
            st.slider("threshold1", min_value=1, max_value=200, value=50, step=1, key="threshold1", on_change=self.extract_main_silhouette)
            st.slider("threshold2", min_value=1, max_value=200, value=150, step=1, key="threshold2", on_change=self.extract_main_silhouette)
            st.slider("blurred", min_value=1, max_value=50, value=5, step=2, key="blurred", on_change=self.extract_main_silhouette)
            st.slider("area_threshold", min_value=1, max_value=200, value=10, step=1, key="area_threshold", on_change=self.extract_main_silhouette)
            
            if st.button("Processar"):
                self.extract_main_silhouette()
            
                with col3:
                    st.subheader('Imagem tratada', divider=True)
                    st.image("perfil-jn-output.png", use_container_width=True)
        



if __name__ == "__main__":
    Embroidery().ui()