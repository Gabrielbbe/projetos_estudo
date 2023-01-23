 
# Scrips que rodam o projeto automaticamente na máquina local </h1>

## Requisitos: 
- Ter o python3 instalado em seu computador  
- Tenha o Navegador Firefox instalado na sua máquina.  
- Instalar os requirements, via terminal pelo comando: <code>pip3 install -r requirements.txt </code>  

 Baixe este repositório na sua máquina, abra a pasta onde baixou o repositório via terminal e siga os passos.
## Primeiro passo: 
- Rode o script "script_webscraping_amazon.py" via terminal pelo comando <code> python3 script_webscraping_amazon.py </code>
esse passo é o mais demorado(1 - 2 minutos), ele vai terminar quando criar um arquivo excel com o nome 'info_amazon.xlsx'
 
## Então seguimos para o segundo passo:
- Rode o script "script_estrutura.py" com o comando <code> python3 script_estrutura.py </code> ele estrutura os dados coletados e extrai alguma informações que queremos dos dados coletados.
 
## Terceito e último passo:
- Rode o script "streamlit_part.py" com o comando <code> streamlit run streamlit_part.py </code>, após rodar esse comando ele deve automaticamente abrir o seu navegador padrão e mostrar o dashboard.
