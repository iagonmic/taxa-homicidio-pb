import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def main():
    st.set_page_config(page_title='Análise Anual', page_icon='📅', layout='wide')
    
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    st.title('Análise anual das taxas de homicídio na Paraíba')
    
    col1, col2 = st.columns(2)
    
    file = pd.read_csv('csv_visualizacao/pb_taxa_homicidios.csv', sep=',', encoding='utf-8')
    df = pd.DataFrame(file)
    
    filebr = pd.read_csv('csv_visualizacao/brasil_taxa_homicidio.csv', sep=';', encoding='utf-8')
    df_br = pd.DataFrame(filebr)
    
    with col1:
        min_year = min(df['ANO'])
        max_year = max(df['ANO'])
        anos = st.slider(
            "Selecione o intervalo de anos",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        
        df_anos = df[(df['ANO'] >= anos[0]) & (df['ANO'] <= anos[1])]
        
        col11, col12, col13 = st.columns(3)
        with col11:
            min_hom = df_anos['TAXA'].min()
            st.metric(label="Taxa minima", value=min_hom)
        
        with col12:
            max_hom = df_anos['TAXA'].max()
            st.metric(label="Taxa máxima", value=max_hom)
        
        with col13:
            media_hom = df_anos['TAXA'].mean()
            st.metric(label="Média das taxas", value=f"{media_hom:.3f}")
        
        fig = px.line(df_anos, x="ANO", y="TAXA", title="Taxa de Homicídio ao longo dos anos")
        fig.update_xaxes(type='category')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        lista_anos = df['ANO'].unique()
        option = st.selectbox('Selecione um ano',
                              lista_anos,
                              label_visibility=st.session_state.visibility, 
                              disabled=st.session_state.disabled, )

        col21, col22 = st.columns(2)
        with col21:
            taxabr = df_br.query(f'período == {option}')
            taxabr = taxabr['valor'].iloc[0]
            st.metric(label=f'Taxa homicídio Brasil no ano {option}', value=taxabr)
        with col22:
            taxapb = df.query(f'ANO == {option}')
            taxapb = taxapb['TAXA'].iloc[0]
            st.metric(label=f'Taxa homicídio Paríba no ano {option}', value=taxapb)
        
        escala_min = 0
        escala_max = taxabr*2
        
        cor_delta = "green" if taxapb <= taxabr else "red"
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta", 
            value=taxapb,  
            delta={'reference': taxabr, 'position': "top", 'increasing': {'color': cor_delta}},  
            gauge={
                'axis': {'range': [escala_min, escala_max]}, 
                'bar': {'color': "black"},  
                'steps': [
                    {'range': [escala_min, 0.5 * taxabr], 'color': "green"},  # Faixa abaixo do neutro
                    {'range': [0.5 * taxabr, taxabr], 'color': "yellow"},  # Faixa neutra
                    {'range': [taxabr, escala_max], 'color': "red"}  # Faixa acima do neutro
                ],
            },
            title={'text': "Comparação com Valor Neutro"}  
        ))
        
        st.plotly_chart(fig)
if __name__ == '__main__':
    main()
