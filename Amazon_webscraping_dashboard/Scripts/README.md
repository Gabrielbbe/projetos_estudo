 <h1> Scrips que rodam o projeto automaticamente na máquina local </h1>

<h2> Requisitos: </h2>
- &nbsp;  Ter o python3 instalado em seu computador  
- &nbsp;  Tenha o Navegador Firefox instalado na sua máquina.  
- &nbsp;  Instalar os requirements, via terminal pelo comando: <code>pip3 install -r requirements.txt </code>  \n

&nbsp; Baixe este repositório na sua máquina, e siga os passos.
&nbsp; Primeiro passo: 
&nbsp; Rode o script "script_webscraping_amazon.py" via terminal pelo comando <code> python3 script_webscraping_amazon.py </code>
esse passo é o mais demorado, ele vai terminal quando criar um arquivo excel com o nome 'info_amazon.xlsx'
 
&nbsp; Então seguimos para o segundo passo:
&nbsp; Rode o script "script_estrutura.py" com o comando <code> python3 script_estrutura.py </code> ele extrutura os dados coletados e extrais alguma informações que queremos dos dados coletados.
 
&nbsp; Terceito e último passo:
&nbsp; Rode o script "streamlit_part.py" com o comando <code> python3 streamlit_part.py </code>, após rodar esse comando ele deve automaticamente abrir o seu navegador padrão e mostrar o dashboard.
