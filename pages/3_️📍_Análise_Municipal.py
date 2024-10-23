import streamlit as st
import pandas as pd
import plotly.express as px
import json

def main():
    st.set_page_config(page_title='Análise Municipal', page_icon='🏠', layout='wide')

    with st.sidebar:
        option = st.selectbox('Modo de visualização', options=['Colunas', 'Intervalo'], index=0)

        head_amount = st.number_input('Quantidade de linhas na tabela:', min_value=0, max_value=30, value=5)

        fill_button = st.checkbox('Visualizar municípios com dados indisponíveis', value=True)

    paraiba = get_transformed_json()

    df = df_transformed(path='csv_visualizacao/mun_taxa_homicidios.csv', fill=fill_button)
    
    if option == 'Colunas':
        
        col1, col2 = st.columns(2, gap='large')

        with col1:
            select_option1 = st.selectbox('Selecione o ano a ser analisado para o primeiro mapa:', index=0, options=range(2010,2023), key='selectbox1')

            df1 = df[df['Ano'] == select_option1]

            df1_sorted = (df1
            .sort_values(by='Taxa de Homicídio (100 mil hab.)', ascending=False)
            .head(head_amount)
            .assign(Ranking = lambda x: x.reset_index().index + 1)
            .filter(['Ranking','Código do Município', 'Nome do Município', 'Taxa de Homicídio (100 mil hab.)'])
            )

            fig = plot_choropleth(
                df1,
                geojson=paraiba,
                locations='Código do Município',
                color='Taxa de Homicídio (100 mil hab.)',
                featureidkey='properties.id',
                hover_data=[column for column in df.columns if column not in ['Nome do Município', 'Ano']],
                hover_name='Nome do Município',
                ano = select_option1,
                height=500,
            )

            st.plotly_chart(fig, key='map1')
            
            st.dataframe(df1_sorted, hide_index=True, width=2000)

        with col2:
            select_option2 = st.selectbox('Selecione o ano a ser analisado para o segundo mapa:', index=12, options=range(2010,2023), key='selectbox2')

            df2 = df[df['Ano'] == select_option2]

            df2_sorted = (df2
            .sort_values(by='Taxa de Homicídio (100 mil hab.)', ascending=False)
            .head(head_amount)
            .assign(Ranking = lambda x: x.reset_index().index + 1)
            .filter(['Ranking','Código do Município', 'Nome do Município', 'Taxa de Homicídio (100 mil hab.)'])
            )

            fig = plot_choropleth(
                df2,
                geojson=paraiba,
                locations='Código do Município',
                color='Taxa de Homicídio (100 mil hab.)',
                featureidkey='properties.id',
                hover_data=[column for column in df.columns if column not in ['Nome do Município', 'Ano']],
                hover_name='Nome do Município',
                ano = select_option2,
                height=500,
            )
            
            st.plotly_chart(fig, key='map2')

            st.dataframe(df2_sorted, hide_index=True, width=2000)

    elif option == 'Intervalo':

        select_option_slider = st.slider('Selecione o intervalo a ser analisado no mapa:', min_value=2010, max_value=2022, value=(2010,2022), key='slider1')

        df_slider = (
            df[
                (df['Ano'] >= select_option_slider[0]) & (df['Ano'] <= select_option_slider[1])
            ].groupby('Código do Município')['Taxa de Homicídio (100 mil hab.)']
            .mean()
            .reset_index()
            .merge(df[['Código do Município','Nome do Município']], on='Código do Município', how='inner')
            .drop_duplicates()
            )

        df_slider_sorted = (df_slider
            .sort_values(by='Taxa de Homicídio (100 mil hab.)', ascending=False)
            .head(head_amount)
            .assign(Ranking = lambda x: x.reset_index().index + 1)
            .filter(['Ranking','Código do Município', 'Nome do Município', 'Taxa de Homicídio (100 mil hab.)'])
            )

        fig = plot_choropleth(
            df_slider,
            geojson=paraiba,
            locations='Código do Município',
            color='Taxa de Homicídio (100 mil hab.)',
            featureidkey='properties.id',
            hover_data=[column for column in df_slider.columns if column not in ['Nome do Município', 'Ano']],
            hover_name='Nome do Município',
            height=600,
            ano = select_option_slider
        )

        st.plotly_chart(fig, key='map1')

        st.dataframe(df_slider_sorted, hide_index=True, width=2000)


def get_transformed_json(): # transformação do id dentro do json
    with open('data/paraiba.json', 'r') as file:
        state = json.load(file)
        
        for i in range(len(state['features'])):
            state['features'][i]['properties']['id'] = state['features'][i]['properties']['id'][:-1]

    return state

def plot_choropleth(df, geojson, locations, color, featureidkey, hover_data, hover_name, ano, range_color=None, height=None):
    fig = px.choropleth(
            df,
            geojson=geojson,
            locations=locations,
            color=color,
            featureidkey=featureidkey,
            color_continuous_scale='Oranges', # escala de cor
            hover_data=hover_data,
            hover_name=hover_name,
            range_color=range_color,
            #title=f'Taxa de Homicídio na Paraíba em {ano}'
        )

    fig.update_geos(
        fitbounds='locations', # dar zoom no gráfico
        visible=False, # excluir outras localizações não marcadas
        bgcolor='rgba(0,0,0,0)' # fundo transparente
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
        ),
    )

    fig.update_layout(
        height=height,
        coloraxis_colorbar=dict(
            title="Taxa Hom.",
            x=1,  # posição horizontal (0: extrema esquerda, 1: extrema direita)
            dtick='25',
        ),
        hovermode='closest',
    )

    fig.add_annotation(
        showarrow=False,
        text='Os municípios que tem taxa igual a 0 não possuem dados disponíveis no período.',
        font=dict(size=12), 
        x=0.5,
        y=-0.1
    )

    return fig

def df_transformed(path, fill=True):

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
    cod_mun = list(df['Código do Município'].unique())
    nom_mun = list(df['Nome do Município'].unique())

     # adicionar carrapateira manualmente
    cod_mun.append('250410') 
    nom_mun.append('Carrapateira')

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
        .rename({'Nome do Município_y': 'Nome do Município'}, axis=1)
        )

    if fill:
        df = df.fillna(0)

    return df

def normalize(number, df, column:str):
    x = round(100 * (number-df[column].min())/(df[column].max()-df[column].min()), 2)

    return x

if __name__ == '__main__':
    main()