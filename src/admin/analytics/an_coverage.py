import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import folium
from branca.colormap import LinearColormap
from streamlit_folium import st_folium



def get_shapefile():
    shapefile_path = "src/admin/geo/BR_UF_2022.shp"

    if st.session_state['uf'] == "Brasil":
        st.session_state['granularidade_mapa'] == "Estado"

    if st.session_state['granularidade_mapa'] == "Estado":
        shapefile_path = "src/admin/geo/BR_UF_2022.shp"
        field = 'CD_UF'
    elif st.session_state['granularidade_mapa'] == "Mesorregião":
        shapefile_path = "src/admin/geo/BR_Mesorregioes_2022.shp"
        field = 'CD_MESO'
    elif st.session_state['granularidade_mapa'] == "Microrregião":
        shapefile_path = "src/admin/geo/BR_Microrregioes_2022.shp"
        field = 'CD_MICRO'
    elif st.session_state['granularidade_mapa'] == "Município":
        shapefile_path = "src/admin/geo/BR_Municipios_2022.shp"
        field = 'CD_MUN'
    
    gdf = gpd.read_file(shapefile_path)
    gdf['group'] = gdf[field].astype(int)
    
    if st.session_state['uf'] != "Brasil":
        gdf = gdf[gdf['SIGLA_UF'] == st.session_state['uf']]
    
    return gdf



def get_df():
    sheet_id = "1Ig5l5E-co1b98viut8YK3bPPiclrOX-OHEgad7l-7VQ"
    sheet_name = "IBGE"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    
    if st.session_state['granularidade_mapa'] == "País":
        field_cod = "pais_ibge_cod"
        field_name = "pais_ibge"
    elif st.session_state['granularidade_mapa'] == "Estado":
        field_cod = "uf_ibge_cod"
        field_name = "uf_ibge"
    elif st.session_state['granularidade_mapa'] == "Mesorregião":
        field_cod = "meso_ibge_cod"
        field_name = "meso_ibge"
    elif st.session_state['granularidade_mapa'] == "Microrregião":
        field_cod = "micro_ibge_cod"
        field_name = "micro_ibge"
    elif st.session_state['granularidade_mapa'] == "Município":
        field_cod = "mun_ibge_cod"
        field_name = "mun_ibge"
    
    if st.session_state['cobertura_por'] == "N° de município":
        metric = "counter"
    elif st.session_state['cobertura_por'] == "População":
        metric = "populacao"
    elif st.session_state['cobertura_por'] == "Área":
        metric = "area"
    
    print('df keys:')
    print(df.keys())
    grouped_df_total = df.groupby([field_cod, field_name])[metric].sum().reset_index()
    grouped_df_total.columns = ['group', 'group_name', 'metric']
    grouped_df_total['group'] = grouped_df_total['group'].astype(int)
    print(grouped_df_total.keys())
    # grouped_df_total['group_name'] = grouped_df_total[field_name]
    
    df_filtered = df[df['coverage'] == True]
    grouped_df_filtered = df_filtered.groupby([field_cod])[metric].sum().reset_index()
    grouped_df_filtered.columns = ['group', 'metric_filtered']
    
    result = pd.merge(left=grouped_df_filtered, right=grouped_df_total, on='group')
    result['coverage'] = result['metric_filtered'] / result['metric']
    print('Deu certo!')
    return result



def plot_map_detailed(gdf, df):
    gdf = gdf.merge(df, left_on='group', right_on='group', how='left')
    m = folium.Map(location=[-15.7801, -47.9292], zoom_start=4)
    colormap = LinearColormap(colors=['white', 'blue'], vmin=0, vmax=1)
    print(gdf.head())

    for _, row in gdf.iterrows():
        group = row['group_name']
        coverage = row['coverage'] if not pd.isna(row['coverage']) else 0  # Tratar valores NaN
        folium.GeoJson(
            row['geometry'],
            style_function=lambda x, cov=coverage: {
                'color': 'gray',
                'fillColor': colormap(cov),
                'weight': 0.5,
                'fillOpacity': 0.7
            }
        ).add_child(folium.Tooltip(f"Group: {group}<br>Coverage: {coverage:.2f}")).add_to(m)
    colormap.add_to(m)
    st_folium(m, width=700, height=500)



def plot_map_simplified(gdf, df):
    gdf = gdf.merge(df, left_on='group', right_on='group', how='left')

    fig, ax = plt.subplots(1, 1, figsize=(20, 20))
    gdf.boundary.plot(ax=ax, linewidth=1, color="gray")
    gdf.plot(column='coverage', cmap='Blues', linewidth=0.2, ax=ax, edgecolor='0.8', legend=True, vmin=0, vmax=1)
    
    ax.set_title(f'Cobertura por {st.session_state["granularidade_mapa"]} do {st.session_state["uf"]}', fontsize=28)
    ax.set_axis_off()
    st.pyplot(fig)



def an_coverage():
    ufs = ['Brasil', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']    
    if not 'granularidade_mapa' in st.session_state:
        st.session_state['granularidade_mapa'] = "Município"
    
    st.title("Cobertura")
    
    col1, col2 = st.columns([1, 2], gap='large')
    
    with col1:
        st.subheader("Parâmetros de análise", divider=True)
        st.radio("Tipo de mapa", ["Simplificado", "Detalhado"], index=0, key="tipo_mapa")
        st.selectbox("UF", ufs, index=0, key="uf")
        if st.session_state['uf'] != "Brasil":
            st.radio("Granularidade", ["Mesorregião", "Microrregião", "Município"], index=2, key="granularidade_mapa")
        st.radio("Cobertura por", ["N° de município", "População", "Área"], index=0, key="cobertura_por")
    
    with col2:
        gdf = get_shapefile()
        df_group = get_df()
        if st.session_state['tipo_mapa'] == "Detalhado":
            plot_map_detailed(gdf, df_group)
        else:
            plot_map_simplified(gdf, df_group)

if __name__ == '__main__':
    an_coverage()


        
        # m = folium.Map(location=[-15.7801, -47.9292], zoom_start=5)

        # # Adicionar todos os municípios ao mapa em cinza
        # # for _, row in gdf.iterrows():
        # #     folium.GeoJson(row['geometry'], style_function=lambda x: {'color': 'gray'}).add_to(m)
        
        # colormap = LinearColormap(colors=['red', 'blue'], vmin=0.0, vmax=1.0)
        
        # for _, row in gdf.iterrows():
        #     print('Início de novo grupo:')
        #     group = row['group']  # Pegar o 'group' de cada município
        #     print(group)
            
        #     try:
        #         coverage = df_group.loc[df_group['group'] == group]['coverage'].values[0]  # Pegar o valor da 'coverage'
        #     except:
        #         coverage=0

        #     folium.GeoJson(row['geometry'], style_function=lambda x, cov=coverage : {
        #         'color': colormap(cov),       # Cor da borda
        #         'fillColor': colormap(cov),   # Cor de preenchimento
        #         'weight': 0.3,           # Espessura da borda (1 é bem fino, você pode ajustar conforme necessário)
        #         'fillOpacity': 0.5     # Opacidade do preenchimento                
        #     }).add_to(m)

        # st_folium(m, width=700, height=500)

