import streamlit as st
import pandas as pd
import plotly.express as px
import json

def main():
    st.set_page_config(page_title='Análise Municipal', page_icon='🏠', layout='wide')

    paraiba = get_transformed_json()

    df = df_transformed(path='csv_visualizacao/mun_taxa_homicidios.csv')

    with st.sidebar:
        option = st.selectbox('Escolha o modo de visualização', options=['Colunas', 'Intervalo'], index=1)
    
    if option == 'Colunas':
        
        col1, col2 = st.columns(2, gap='large')

        with col1:
            select_option1 = st.selectbox('Selecione o ano a ser analisado para o primeiro mapa:', options=range(2010,2023), key='selectbox1')

            df1 = df[df['Ano'] == select_option1]

            fig = plot_cloropleth(
                df1,
                geojson=paraiba,
                locations='Código do Município',
                color='Taxa de Homicídio (100 mil hab.)',
                featureidkey='properties.id',
                hover_data=[column for column in df.columns if column not in ['Nome do Município', 'Ano']],
                hover_name='Nome do Município',
                height=500
            )

            st.plotly_chart(fig, key='map1')

        with col2:
            select_option2 = st.selectbox('Selecione o ano a ser analisado para o primeiro mapa:', options=range(2010,2023), key='selectbox2')

            df2 = df[df['Ano'] == select_option2]

            fig = plot_cloropleth(
                df2,
                geojson=paraiba,
                locations='Código do Município',
                color='Taxa de Homicídio (100 mil hab.)',
                featureidkey='properties.id',
                hover_data=[column for column in df.columns if column not in ['Nome do Município', 'Ano']],
                hover_name='Nome do Município',
                height=500
            )

            st.plotly_chart(fig, key='map2')

    elif option == 'Intervalo':
        st.slider('Selecione o ano a ser analisado para o primeiro mapa:', min_value=2010, max_value=2023, key='slider1')

        fig = plot_cloropleth(
            df,
            geojson=paraiba,
            locations='Código do Município',
            color='Taxa de Homicídio (100 mil hab.)',
            featureidkey='properties.id',
            hover_data=[column for column in df.columns if column not in ['Nome do Município', 'Ano']],
            hover_name='Nome do Município',
            height=800
        )

        st.plotly_chart(fig, key='map1')


def get_transformed_json(): # transformação do id dentro do json
    with open('data/paraiba.json', 'r') as file:
        state = json.load(file)
        
        for i in range(len(state['features'])):
            state['features'][i]['properties']['id'] = state['features'][i]['properties']['id'][:-1]

    return state

def plot_cloropleth(df, geojson, locations, color, featureidkey, hover_data, hover_name, height=None):
    fig = px.choropleth(
            df,
            geojson=geojson,
            locations=locations,
            color=color,
            featureidkey=featureidkey,
            color_continuous_scale='Oranges', # escala de cor
            hover_data=hover_data,
            hover_name=hover_name
        )

    fig.update_geos(
        fitbounds='locations', # dar zoom no gráfico
        visible=False, # excluir outras localizações não marcadas
        bgcolor='rgba(0,0,0,0)' # fundo transparente
    )

    fig.update_layout(
        height=height,
        coloraxis_colorbar=dict(
        title="Taxa de Homicídio",
        x=1,  # posição horizontal (0: extrema esquerda, 1: extrema direita)
        )
    )

    fig.update_traces(
        hovertemplate="<b>Município:</b> %{hovertext}<br>" + 
                  "<b>Taxa de Homicídio (100 mil hab.):</b> %{z}<br>" +  
                  "<extra></extra>",

        hoverlabel=dict(
            font_size=16,
            bgcolor="black",  
            bordercolor="white",  
            font_color="white"
        )
    )
    
    return fig

def df_transformed(path):

    df = (
        pd.read_csv(
            path,
            index_col='Unnamed: 0'
        )
        .reset_index()
        .drop('index', axis=1)
    )

    df = df.rename({
        'TAXA_HOMICIDIO': 'Taxa de Homicídio (100 mil hab.)',
        'COD_MUN': 'Código do Município',
        'NOM_MUN': 'Nome do Município',
        'ANO': 'Ano',
        'HOMICIDIOS': 'Quantidade de Homicídios',
        'POPULACAO': 'População do Ano Selecionado'
        }, axis=1)

    df['Taxa de Homicídio (100 mil hab.)'] = (
        df['Taxa de Homicídio (100 mil hab.)']
        #.apply(lambda x: normalize(x, df, 'Taxa de Homicídio (%)'))
    )

    anos = df['Ano'].unique()
    cod_mun = df['Código do Município'].unique()
    nom_mun = df['Nome do Município'].unique()

    df_nom_mun = pd.DataFrame(
        data=list(zip(nom_mun, cod_mun)),
        columns=['Nome do Município', 'Código do Município']
        )

    df = (df.merge(
        pd.DataFrame(
            index=pd.MultiIndex.from_product(
                [anos, cod_mun], names=['Ano', 'Código do Município']
            )
        ).reset_index(),
        on=['Ano', 'Código do Município'],
        how='outer'
        )
        .merge(df_nom_mun, 'outer', on='Código do Município')
        .drop('Nome do Município_x', axis=1)
        .fillna(0)
        .rename({'Nome do Município_y': 'Nome do Município'}, axis=1)
        )

    return df

def normalize(number, df, column:str):
    x = round(100 * (number-df[column].min())/(df[column].max()-df[column].min()), 2)

    return x

if __name__ == '__main__':
    main()