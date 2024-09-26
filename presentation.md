# Análise descritiva temporal das taxas de homicídio no estado da Paraíba

# Introdução

- De acordo com o Anuário Brasileiro de Segurança Pública, de 2023, o Nordeste está em queda nas taxas de violência letal com uma **queda de 4.2%** em relação a 2022.

- Mesmo com essa queda, a região possui a maior taxa de Mortes Violentas Intencionais (MVI) do país.

- **Taxa de MVI do Brasil em 2023: 23,4** (a cada 100 mil habitantes)

- **Taxa de MVI no Nordeste em 2023: 36,9** (a cada 100 mil habitantes)

## Homicídio e Educação

- Com a revisão da literatura, encontrou-se evidências de que a educação é um fator de proteção contra o homicídio. (Gleditsch; Rivera; Zárate-tenorio, 2021)

- Entretanto, verificou-se que não há estudos que evidenciem essa correlação na região Nordeste, mais especificamente no estado da Paraíba.

## Objetivos

Objetiva-se por meio desse estudo, realizar uma análise descritiva dos dados sobre mortalidade na Paraíba, entre os anos de 2010 a 2022, a fim de encontrar evidências da correlação das taxas de homicídio com a baixa escolaridade, além de encontrar o perfil mais comum entre as vítimas de homicídio no estado.

# Metodologia

## Origem dos dados

- Foram utilizados os dados disponibilizados pelo Departamento de Informática do Sistema Único de Saúde (DATASUS), mais especificamente, microdados do Sistema de Informação sobre Mortalidade (SIM).

- Esses microdados centralizam as Declarações de Óbito (DO) de todo território nacional.

- Além disso, foram utilizadas estimativas populacionais do IBGE (Instituto Brasileiro de Geografia e Estatística) para calcular a taxa de homicídio.

## Período temporal e região

- Foram coletados os dados do período de 2010 a 2022, do estado da Paraíba, visto que existe uma carência de estudos voltados a evolução das taxas de homicídio correlacionados a educação, nessa região.

- Além disso, de acordo com os dados do Instituto de Pesquisa Econômica Aplicada (IPEA), houve uma queda nas taxas de homicídio na Paraíba, após o ano de 2010, justificando a escolha do período abordado.

## Extração e tratamento dos dados

### Dados do SIM

- Primeiramente, foi realizado o download dos dados através da plataforma do DATASUS, mais especificamente através do SIM, do período selecionado para análise (2010 a 2022).

- A formatação inicial é em .DBC (Database File Compressed), uma forma compactada do arquivo em .DBF (Database File), e tornou-se necessária a utilização da biblioteca `pyreaddbc`. Essa biblioteca roda apenas em sistemas de arquitetura Linux, o que gerou dificuldade no processo de extração.

- Após a conversão dos arquivos para .DBF, foi realizada a leitura dos dados através da biblioteca `dbfread` e convertemos em objetos da classe `DataFrame` da biblioteca `pandas`.

### Dados do IBGE

Foi realizada a leitura dos dados do IBGE, que vieram no formato inicial `.csv`, através da função `read_csv()` da biblioteca `pandas` e convertemos em objetos da classe `DataFrame`. Os dados foram tratados na hora da leitura.

### Tratamento dos dados

- Realizou-se a verificação da tipagem dos dados e a conversão dos mesmos para utilização na análise.

- Foi observado que aproximadamente 74% dos dados ou estavam vazios ou a escolaridade foi ignorada. A fim de alcançar o objetivo do estudo, foi realizada a remoção dos dados faltantes ou ignorados para a realização do trabalho, facilitando o processo de análise descritiva.

- Após a extração e tratamento dos dados do banco de dados do IBGE e do SIM, houve a junção desses dados em um único `DataFrame`, com a finalidade de definir-se as métricas para análise descritíva.

## Definição das métricas

- A princípio, através do dicionário de dados do SIM definimos as métricas 

## Análise descritiva geral

## Análise segmentada por identificação

Como as métricas foram definidas?

Como os dados foram analisados?