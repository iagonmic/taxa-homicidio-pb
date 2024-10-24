import streamlit as st
import pandas as pd
from random import randint
import plotly.express as px

def main():
    st.set_page_config(page_title='Análise Geral', page_icon='📊', layout='wide')

    if 'keys_order' not in st.session_state:
        st.session_state['keys_order'] = []

    paths = {
        'Idade': 'csv_visualizacao/idade.csv',
        'Escolaridade': 'csv_visualizacao/escolaridade.csv',
        'Ocupação': 'csv_visualizacao/ocupacao.csv',
        'Raça': 'csv_visualizacao/raca.csv',
        'Sexo': 'csv_visualizacao/sexo.csv'
    }

    with st.sidebar:
        multiselect = st.multiselect(
            label='Label',
            label_visibility='hidden',
            options=paths.keys(),
            placeholder='Escolha uma opção'
        )

        if multiselect:
            for element in multiselect:
                key = str(element)

                if key not in st.session_state['keys_order']:
                    st.session_state['keys_order'].append(key)

                st.selectbox(label=f'Tipo de gráfico: {element}', options=['Barra', 'Pizza'], key=key, index=0)

        # remover gráfico ao ser deselecionado na sidebar
        for key in paths:
            if key in st.session_state and key not in multiselect:
                del st.session_state[key]

    keys = {}

    if st.session_state['keys_order']:
        keys = create_graph_keys_dict()

    pop_graph(paths=paths, keys=keys)

    with st.expander('Informações de uso', expanded=True):
        st.write(
            '''
            Para visualizar os gráficos, primeiro selecione o fator social que você quer visualizar na barra lateral à esquerda 👈,
            depois selecione o tipo de gráfico que você quer visualizar.
            
            Após isso, role a tela para baixo para ir visualizando os gráficos.

            Fonte dos gráficos: Elaboração própria.
            '''
        )

    
def pop_graph(paths:dict, keys:dict):
    for social_factor, graph_type in keys.items():
        path = paths[social_factor]

        df = pd.read_csv(path).drop('Unnamed: 0', axis=1)

        st.header(social_factor)

        if graph_type == 'Barra':
            fig = px.bar(data_frame=df, x=df.columns[0], y=df.columns[1], color=df.columns[0], labels={'index': social_factor})

            fig.update_layout(
                xaxis=dict(
                    showticklabels=False
                )
            )

            fig.update_traces(
                hovertemplate="%{label}<br>" + 
                        "Frequência: %{value}<br>" +  
                        "<extra></extra>",

                hoverlabel=dict(
                    font_size=16,
                    bgcolor="black",  
                    bordercolor="white",  
                    font_color="white"
                ),
            )
            
            st.plotly_chart(fig, key=str(social_factor) + '_graph')
        
        if graph_type == 'Pizza':
            fig = px.pie(data_frame=df, names=df.columns[0], labels={'index': social_factor}, values=df.columns[1])

            fig.update_traces(
                hovertemplate="%{label}<br>" + 
                        "Frequência: %{value}<br>" +  
                        "<extra></extra>",

                hoverlabel=dict(
                    font_size=16,
                    bgcolor="black",  
                    bordercolor="white",  
                    font_color="white"
                ),
            )
            

            st.plotly_chart(fig, key=str(social_factor) + '_graph')


def create_graph_keys_dict():
    temp_list = st.session_state['keys_order']

    graph_keys = {}

    while temp_list:
        key = temp_list[0]
        temp_list.remove(key)
        value = st.session_state.get(key)

        graph_keys.update({key:value})

    return graph_keys


if __name__ == '__main__':
    main()
