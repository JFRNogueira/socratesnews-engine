import streamlit as st
# from bot_jornalista.writer_news import WriterNews
# from sources.google_news import GoogleNews, GoogleNewsCluster
from streamlit_image_select import image_select



def mundo():
    col1, col2 = st.columns(2)

    with col1:
        st.title("Bot Mundo")
        st.subheader('Notícias de referência')
        
        # Look for references in Google News
        if st.button("Buscar temas no Google News"):
            st.markdown("Buscando temas no Google News...")
            # GoogleNews(['Mundo'])
            
        # If references are loaded
        if 'mundo_themes' in st.session_state:
            
            # Renderizar o editor de dados depois das métricas
            st.session_state['mundo_themes_selection'] = st.data_editor(
                st.session_state['mundo_themes_selection'] if 'mundo_themes_selection' in st.session_state else st.session_state['mundo_themes'], 
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
            
            if 'mundo_themes_selection' in st.session_state and (st.session_state['mundo_themes_selection']['create'] == True).sum() > 0:
                if st.button("Buscar fontes para notícias"):
                    st.markdown("Buscando fontes para notícias...")
                    # GoogleNewsCluster(['Mundo']).get_all_references()
                
            if any(f'mundo_news_{i}_image_text' in st.session_state for i in range(1, 10)):
                if st.button(f"Gerar todas as notícias"):
                    for i in range(1, 20):
                        if f'mundo_news_{i}_image_text' in st.session_state:
                            selection = st.session_state[f'mundo_news_{i}_reference_news_selected']
                            # st.session_state[f'mundo_news_{i}_final'] = WriterNews('Mundo', 
                            #     selection[selection['source'] == True]['text'].tolist(),
                            #     selection[selection['source'] == True]['title'].tolist(),
                            #     st.session_state[f'mundo_news_{i}_image_url'],
                            #     st.session_state[f'mundo_news_{i}_image_text'])

                        


    with col2:
        
        # If there is at least one selected theme
        if 'mundo_themes_selection' in st.session_state:
            n_news = st.session_state['mundo_themes_selection'].shape[0]
            n_expected = (st.session_state['mundo_themes_selection']['create'] == True).sum()

            # Exibir as métricas acima do editor
            col11, col12 = st.columns(2)
            col11.metric("# Temas", n_news)
            col12.metric("Temas selecionados", n_expected)
        else:
            st.header("")



        st.subheader('Gerador de notícias')
        if 'mundo_themes_selection' in st.session_state and (st.session_state['mundo_themes_selection']['create'] == True).sum() > 0:
            selected_themes = st.session_state['mundo_themes_selection'][st.session_state['mundo_themes_selection']['create'] == True]

            tabs = st.tabs([f"N {i}" for i in range(1, n_expected+1)])
            for n_tab, tab in enumerate(tabs, start=1):
                with tab:
                    st.write(f"**Tema {n_tab}: {selected_themes['title'].iloc[n_tab-1]}**")

                    if f'mundo_news_{n_tab}_reference_news' in st.session_state:

                        # Input de imageText
                        st.session_state[f'mundo_news_{n_tab}_image_text'] = st.text_input(
                            f'Texto da imagem da notícia {n_tab}', 
                            value = st.session_state[f'mundo_news_{n_tab}_image_text'] if f'mundo_news_{n_tab}_image_text' in st.session_state else ''
                        )
                        st.write(f'{len(st.session_state[f'mundo_news_{n_tab}_image_text'])} caracteres')

                        # Input de imageUrl
                        try:
                            st.session_state[f'mundo_news_{n_tab}_image_url'] = image_select(
                                "",
                                images = st.session_state[f'mundo_news_{n_tab}_reference_images']['imageUrl'].tolist(),
                                captions = st.session_state[f'mundo_news_{n_tab}_reference_images']['imageText'].tolist(),
                            )
                        except Exception as e:
                            st.error(f"Erro ao carregar imagens: {e}")

                        # Show dataframe with references
                        if st.checkbox(f'Ver referências para notícia {n_tab}', value = True):
                            st.session_state[f'mundo_news_{n_tab}_reference_news_selected'] = st.data_editor(
                                st.session_state[f'mundo_news_{n_tab}_reference_news'], 
                                column_config={
                                    "create": st.column_config.CheckboxColumn(
                                        "Criar?",
                                    ),
                                    "url": st.column_config.LinkColumn(
                                        "Link", display_text="Link",
                                        disabled=True
                                    ),
                                    "title": st.column_config.TextColumn(
                                        "Título",
                                        max_chars=100,
                                        disabled=True
                                    ),
                                },
                                hide_index=True
                            )

                        if f'mundo_news_{n_tab}_reference_news_selected' in st.session_state:
                            if st.button(f'Gerar notícia {n_tab}'):
                                if f'mundo_news_{n_tab}_image_text' in st.session_state:
                                    selection = st.session_state[f'mundo_news_{n_tab}_reference_news_selected']
                                    # st.session_state[f'mundo_news_{n_tab}_final'] = WriterNews('Mundo', 
                                    #     selection[selection['source'] == True]['text'].tolist(),
                                    #     selection[selection['source'] == True]['title'].tolist(),
                                    #     st.session_state[f'mundo_news_{i}_image_url'],
                                    #     st.session_state[f'mundo_news_{i}_image_text'])
                                    
                            
                            
                        if f'mundo_news_{n_tab}_final' in st.session_state:
                            st.write(f"**Título:** {st.session_state[f'mundo_news_{n_tab}_final'].title}")
                            st.write(f"**Resumo:** {st.session_state[f'mundo_news_{n_tab}_final'].summary}")
                            st.write(f"**Imagem:** {st.session_state[f'mundo_news_{n_tab}_final'].imageUrl}")
                            st.write(f"**Texto da imagem:** {st.session_state[f'mundo_news_{n_tab}_final'].imageText}")
                            st.write(f"**Texto:** {st.session_state[f'mundo_news_{n_tab}_final'].text}")



if __name__ == '__main__':
    mundo()


