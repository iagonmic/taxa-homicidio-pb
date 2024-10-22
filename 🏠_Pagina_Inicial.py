import streamlit as st

def main():
    st.set_page_config(page_title="Taxa de Homicídio na Paraíba", page_icon=":knife:")

    st.title(':knife: Taxa de Homicídio na Paraíba :flag-br:')

    st.markdown(
        '''

        ### Seja bem-vindo(a) ao nosso aplicativo analisador da taxa de homicídio na Paraíba!

        #### Contexto
        Nesse aplicativo você encontrará uma analise detalhada da taxa de homicídio no estado da Paraíba e seus municípios,
        investigando a relação entre a quantidade de homicídios e a população de baixa escolaridade em cada localização e por ano,
        bem como fatores sociais, a se dizer, idade, sexo, raça, escolaridade e ocupação.

        #### Instruções
        O aplicativo é dividido em 3 principais partes:
        1. **Análise Geral**: Análise geral da taxa de homicídio em relação aos fatores sociais no estado.
        2. **Análise Anual**: Comparação entre a taxa de homicídio na Paraíba e no Brasil, analisada ano a ano.
        3. **Análise Municipal**: Análise detalhada da taxa de homicídio em cada município da Paraíba.

        ##### 👈 Navegue pelas páginas do aplicativo ao lado 👈 
                    
        '''
    )


if __name__ == '__main__':
    main()
