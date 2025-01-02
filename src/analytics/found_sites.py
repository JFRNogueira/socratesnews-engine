import math
import streamlit as st
import pandas as pd



class FoundSites:
    
    
    
    def __init__(self):
        pass
    
    
    
    def fontes_pendentes(self):
        file_src = 'src/journalist/bots_health_status.csv'
        src_df = pd.read_csv(file_src)
        src_df['ts'] = pd.to_datetime(src_df['ts'])
        src_df['date'] = src_df['ts'].dt.date
        src_df['src'] = src_df['url'].str.split('/').str[2]
        return src_df
    
    
    
    def highlight_not_100(self, val):
        return "background-color: #FF8383" if val != 100 else "background-color: #868FF6"
    
    
    
    def ui(self):
        
        df = self.fontes_pendentes()
        df = df.round(2)

        st.header('Sites encontrados')
        
        col1, col2 = st.columns([1, 2], gap='large')
        
        with col1:
            st.subheader('Parâmetros de análise', divider=True)
            slider = st.slider('Número de dias', 0, 28, 7)
        
        with col2:
            st.subheader('Fontes', divider=True)
            df_grouped = df.groupby('src')[['title', 'summary', 'text', 'imageUrl', 'imageText']].mean() * 100
            
            styled_df = df_grouped.style.applymap(self.highlight_not_100, subset=["title", "summary", "text", "imageUrl", "imageText"])
            
            st.dataframe(df_grouped)
        
        

