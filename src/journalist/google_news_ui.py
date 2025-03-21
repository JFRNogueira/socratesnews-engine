import streamlit as st
from journalist.writer_news import WriterNews
from sources.google_news import GoogleNews, GoogleNewsCluster
from streamlit_image_select import image_select



class GoogleNewsUi:
    
    
    
    def __init__(self, sectionName):
        self.sectionName = sectionName
        self.sectionNameLower = sectionName.lower()
        pass
    
    
    
    # Renderizar o editor de dados depois das métricas
    def render_editor(self, n_news = 0):
        df = st.session_state[f"{self.sectionNameLower}_themes"].copy()
        valid_titles = df[df['title'] != 'N/A']
        st.session_state[f'{self.sectionNameLower}_themes'] 
        indices_to_mark = valid_titles.index[:n_news]
        df.loc[indices_to_mark, 'create'] = True
        st.session_state[f'{self.sectionNameLower}_themes_selection'] = df
        
        st.session_state[f'{self.sectionNameLower}_themes_selection'] = st.data_editor(
            st.session_state[f'{self.sectionNameLower}_themes_selection'] if f'{self.sectionNameLower}_themes_selection' in st.session_state else st.session_state[f'{self.sectionNameLower}_themes'], 
            column_config={
                "create": st.column_config.CheckboxColumn(
                    "Criar?",
                ),
                "title": st.column_config.TextColumn(
                    "Título",
                    max_chars=100,
                    disabled=True
                ),
                "url": st.column_config.LinkColumn(
                    "Link", display_text="Link",
                    disabled=True
                ),
            },
            hide_index=True
        )
        df = st.session_state[f'{self.sectionNameLower}_themes'].copy()
        valid_rows = df[df["title"] != "N/A"].head(4).index  # Seleciona os índices válidos
        df.loc[valid_rows, "create"] = True  # Marca as linhas selecionadas
        st.session_state[f'{self.sectionNameLower}_themes_selection'] = df
    
    
    
    def create_reference_news_df(self, n_news): # n_news > 0
        return st.data_editor(
            st.session_state[f'{self.sectionNameLower}_news_{n_news}_reference_news'], 
            column_config={
                "create": st.column_config.CheckboxColumn("Criar?"),
                "url": st.column_config.LinkColumn(
                "Link", display_text="Link",disabled=True),
                "title": st.column_config.TextColumn("Título",max_chars=100,disabled=True),
            },
            hide_index=True
        )

    
    
    def ui(self):
        col1, col2 = st.columns(2)

        with col1:
            st.title(f'Bot {self.sectionName}')
            st.subheader('Notícias de referência')
            
            # Look for references in Google News
            if st.button(f'Buscar {self.sectionName} no Google News'):
                st.markdown("Buscando temas no Google News...")
                GoogleNews([f'{self.sectionName}'])
                
            # If references are loaded
            if f'{self.sectionNameLower}_themes' in st.session_state:
                
                self.render_editor()
                
                if f'{self.sectionNameLower}_themes_selection' in st.session_state and (st.session_state[f'{self.sectionNameLower}_themes_selection']['create'] == True).sum() > 0:
                    if st.button("Buscar fontes para notícias"):
                        st.markdown("Buscando fontes para notícias...")
                        GoogleNewsCluster([self.sectionName]).get_all_references()
                    
                if any(f'{self.sectionNameLower}_news_{i}_image_text' in st.session_state for i in range(1, 10)):
                    if st.button(f"Gerar todas as notícias"):
                        for i in range(1, 20):
                            # TODO: Encontrar uma melhor maneira de avaliar o item abaixo de modo a não depender de iagem
                            st.session_state[f'{self.sectionNameLower}_news_{i}_reference_news_selected'] = self.create_reference_news_df(i)
                            st.session_state[f'{self.sectionNameLower}_news_{i}_final'] = WriterNews(self.sectionName, 
                                selection[selection['source'] == True]['text'].tolist(),
                                selection[selection['source'] == True]['title'].tolist(),
                                st.session_state[f'{self.sectionNameLower}_news_{i}_image_url'],
                                st.session_state[f'{self.sectionNameLower}_news_{i}_image_text'],
                                st.session_state[f'{self.sectionNameLower}_news_{i}_reference_news_selected']
                                )

                            


        with col2:
            
            # If there is at least one selected theme
            if f'{self.sectionNameLower}_themes_selection' in st.session_state:
                n_news = st.session_state[f'{self.sectionNameLower}_themes_selection'].shape[0]
                n_expected = (st.session_state[f'{self.sectionNameLower}_themes_selection']['create'] == True).sum()

                # Exibir as métricas acima do editor
                col11, col12 = st.columns(2)
                col11.metric("# Temas", n_news)
                col12.metric("Temas selecionados", n_expected)
            else:
                st.header("")



            st.subheader('Gerador de notícias')
            if f'{self.sectionNameLower}_themes_selection' in st.session_state and (st.session_state[f'{self.sectionNameLower}_themes_selection']['create'] == True).sum() > 0:
                selected_themes = st.session_state[f'{self.sectionNameLower}_themes_selection'][st.session_state[f'{self.sectionNameLower}_themes_selection']['create'] == True]

                tabs = st.tabs([f"N {i}" for i in range(1, n_expected+1)])
                for n_tab, tab in enumerate(tabs, start=1):
                    with tab:
                        st.write(f"**Tema {n_tab}: {selected_themes['title'].iloc[n_tab-1]}**")

                        if f'{self.sectionNameLower}_news_{n_tab}_reference_news' in st.session_state:

                            # Input de imageText
                            st.session_state[f'{self.sectionNameLower}_news_{n_tab}_image_text'] = st.text_input(
                                f'Texto da imagem da notícia {n_tab}', 
                                value = st.session_state[f'{self.sectionNameLower}_news_{n_tab}_image_text'] if f'{self.sectionNameLower}_news_{n_tab}_image_text' in st.session_state else ''
                            )
                            st.write(f'{len(st.session_state[f'{self.sectionNameLower}_news_{n_tab}_image_text'])} caracteres')

                            # Input de imageUrl
                            try:
                                st.session_state[f'{self.sectionNameLower}_news_{n_tab}_image_url'] = image_select(
                                    "",
                                    images = st.session_state[f'{self.sectionNameLower}_news_{n_tab}_reference_images']['imageUrl'].tolist(),
                                    captions = st.session_state[f'{self.sectionNameLower}_news_{n_tab}_reference_images']['imageText'].tolist(),
                                )
                            except Exception as e:
                                st.error(f"Erro ao carregar imagens: {e}")

                            # Show dataframe with references
                            if st.checkbox(f'Ver referências para notícia {n_tab}', value = True):
                                self.create_reference_news_df(n_tab)

                            if f'{self.sectionNameLower}_news_{n_tab}_reference_news_selected' in st.session_state:
                                if st.button(f'Gerar notícia {n_tab}'):
                                    if f'{self.sectionNameLower}_news_{n_tab}_image_text' in st.session_state:
                                        selection = st.session_state[f'{self.sectionNameLower}_news_{n_tab}_reference_news_selected']
                                        st.session_state[f'{self.sectionNameLower}_news_{n_tab}_final'] = WriterNews(self.sectionName, 
                                            selection[selection['source'] == True]['text'].tolist(),
                                            selection[selection['source'] == True]['title'].tolist(),
                                            st.session_state[f'{self.sectionNameLower}_news_{i}_image_url'],
                                            st.session_state[f'{self.sectionNameLower}_news_{i}_image_text'])
                                        
                                
                                
                            if f'{self.sectionNameLower}_news_{n_tab}_final' in st.session_state:
                                st.write(f"**Título:** {st.session_state[f'{self.sectionNameLower}_news_{n_tab}_final'].title}")
                                st.write(f"**Resumo:** {st.session_state[f'{self.sectionNameLower}_news_{n_tab}_final'].summary}")
                                st.write(f"**Imagem:** {st.session_state[f'{self.sectionNameLower}_news_{n_tab}_final'].imageUrl}")
                                st.write(f"**Texto da imagem:** {st.session_state[f'{self.sectionNameLower}_news_{n_tab}_final'].imageText}")
                                st.write(f"**Texto:** {st.session_state[f'{self.sectionNameLower}_news_{n_tab}_final'].text}")



