import streamlit as st
import plotly.express as px 
import pandas as pd
import os

st.set_page_config(
    page_title = "Dashboard Celulares Amazon",
    page_icon = " 📊 " ,
    layout="wide" )

path = os.path.dirname(__file__)
path_mp = path+'/marca_pais.xlsx'
path_df = path+'/df_final.xlsx'

def get_data():
    df_pais_marca = pd.read_excel(path_mp)
    df = pd.read_excel(path_df)
    return df_pais_marca, df

df_pais_marca, df = get_data()


" # Dashboard Celulares Amazon "
st.markdown('Ctrl + Scroll do mouse para ajustar a página ao tamanho de sua tela')
st.sidebar.markdown(' # Dashboard dos dados dos celulares mais vendidos no site da Amazon brasil, o ranking vai do 1º celular mais vendido para o menos vendido, \
os dados foram coletados dia 20/01/2023.  \n')
st.sidebar.markdown(' ## ***Se você quiser rodar o script para coletar os dados e gerar um dashboard igual ao que você está vendo na página*** com os \
dados de hoje ***de forma automatizada*** você pode seguir as ***instruções da pagina do projeto no github:*** https://shre.ink/1WtH  \n ## Se por algum motivo quiser entrar em ***contato*** comigo ou tiver alguma sugestão ***pode me enviar um e-mail:*** gabbe2.718@gmail.com ')


#treemap pais->marca
fig_treemap = px.treemap(
    df_pais_marca, path= ['marca','paises'], values='valores',width=4800, height=800,
    title='Treemap marcas mais vendidas e seus paises de origem' )

#line preco
fig_preco = px.line(
    df, x= 'rank', y = 'preco', title='Rank x Preço', markers=True,
    labels={'rank':"Posição no Ranking", 'preco':'Preço'}
    )

# boxplot preco x marca
fig_boxpreco = px.box(
    df, x = 'marca',  y='preco',title = 'Boxplot dos Preços em relação as marcas', width=400, height=400
)

# rank x estrelas 
fig_estrelas = px.line(
    df, x='rank', y='stars', title ='Rank x Ranking estrelas', markers=True ,
    labels={'rank':"Posição no Ranking", 'stars':"Ranking 5 estrelas"}
)

# rank x numero de avaliações
fig_avaliacoes = px.line(
    df, x= 'rank', y= 'n_avalicoes' , title = 'Rank x Número de avaliações', markers=True,
    width=800, height=400,
    labels={'rank':"Posição no Ranking", 'n_avalicoes':"Número de Avaliações"}
)

# no bar plot ram e rom seria legal ter um tabela ao lado mostrando a dist. geral de cada categoria
# bar plot rom 
fig_rom = px.bar(
    df, x='rank', y='rom', title = 'Rom de acordo com o Rank',
    labels={'rank':"Posição no Ranking", 'rom':"Rom"}
)

fig_rom.update_layout(font_color = 'Black')

# bar plot ram
fig_ram = px.bar(
    df, x='rank', y='ram', title = 'Ram de acordo com o Rank',
    labels={'rank':"Posição no Ranking", 'ram':"Ram"}
)
# tabela de ram e rom depois, pra transformar ram e rom em string e pegar a frequencia
df['rom'] = df['rom'].map(str)
rom_zero =  df[df['rom']=='0'].count()
df['ram'] = df['ram'].map(str)

table_rom = df.groupby('rom')['rom'].count()
table_rom = table_rom.transform(lambda x: 100 * x/(149-rom_zero['rom']))


#st.table(table_rom[1:])

#tab ram
df['ram'] = df['ram'].map(str)

ram_zero =  df[df['ram']=='0'].count()

table_ram = df.groupby('ram')['ram'].count()
table_ram = table_ram.transform(lambda x: 100 * x/(149-ram_zero['ram']))


#st.table(table_ram[1:])
# se faze uma coluna em baixo da outra ele coloca embaixo do plot
col1,col2,col3,col4,col5 = st.columns(5, gap="large")
#col1 - treemap grande
# container treemap preço aval.
with st.container():
    col1,col2, col3 = st.columns(3, gap="large")

    with col1:
        st.plotly_chart(fig_treemap,use_container_width=True)
    with col2:
        st.plotly_chart(fig_preco,use_container_width=True)
        st.plotly_chart(fig_avaliacoes,use_container_width=True)
    #col3, col4 = st.columns(2, gap='large')
    with col3:
        st.plotly_chart(fig_boxpreco,use_container_width=True)
        st.plotly_chart(fig_estrelas,use_container_width=True)
    #with col4:
    #    st.plotly_chart(fig_avaliacoes,use_container_width=True)

with st.container():
    col1, col2 = st.columns(2, gap = 'large')

    with col1:
        st.plotly_chart(fig_ram,use_container_width=True)
        st.table(table_ram[1:])
        st.markdown('1ª coluna indica a Ram  2ª coluna porcentagem de celulares com aquela quantidade de ram em relação ao total de celulares')

    with col2:
        st.plotly_chart(fig_rom,use_container_width=True)
        st.table(table_rom[1:])
        st.markdown(' 1ª coluna indica o armazenamento \
             2ª coluna porcentagem de celulares com aquele armazenamento em relação ao total de celulares')

st.markdown('#### Colocamos os valores das variáveis em relação ao ranking para verificarmos se existe algum padrão em relação as variáveis e o ranking, \
que seria do celular mais vendido ao menos, no caso não detectamos nenhum padrão relevante, apenas de que o preço varia de acordo com a marca o que não era uma novidade')

st.title('Dados faltantes')
st.table(df.isnull().sum()[7:])
st.table(df[df == 0].count(axis=0)[5:8])
st.table(df[df == '0'].count(axis=0)[7:9])
st.markdown(" #### ***Observação em relação aos dados faltantes*** algumas descrições do site da Amazon não mencionam o nome da marca, apenas o modelo do celular e acabam 'burlando' o método que usado pelo script para coletar as marcas, o mesmo ocorre no ram e rom, e em alguns casos não temos os dados disponíveis para coletar pelo site, neste caso os dados ausentes são ignorados da visualização e no caso de ser numérico são preenchidos por zero  automaticamente para não atrapalhar a visualização.")


