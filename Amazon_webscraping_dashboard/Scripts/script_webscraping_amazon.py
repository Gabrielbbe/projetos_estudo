# requirements/imports.
from selenium import webdriver  # webdriver é uma api pra web
from selenium.webdriver.firefox.options import Options
import time 
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para coletar as informações dos celulares

def coletar_dados_celulares(url = str()):

    option = Options() # Opções para manipular o webdriver.
    option.headless = True  # Pra não abrir o navegador e mostrar ele coletando as coisas.
    driver = webdriver.Firefox(options=option) # Se colocar assim ele já não abre o navegador e mostra as operações
    
    driver.get(url)

    # Comando para descer até o final da página para carregar todos os elementos.
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)

    # encontra todos os elementos com o id=gridItemRoot que é o id geral dos celulares
    cellphones = driver.find_elements('id','gridItemRoot')

    ind = 0 #indicador do xpath, eles tem essa numeração no meio pra identificar cada elemento.
    df = pd.DataFrame(columns=['info','stars']) #dataframe onde vamos guardar as informações
    page = requests.get(url) 
    soup = BeautifulSoup(page.content,'html.parser') #abrindo a pagina utilizando o Beautifulsoup também
    # abrimos a página utilizando o Beautifulsoup porque utilizando apenas o Selenium
    # não foi possivel coletar todas as informações sem erros
    # st = star title(o titulo informa o valor do rank de estrelas de avaliação do celular)
    
    for cell,st in zip(cellphones, soup.find_all('a',class_='a-link-normal',title=True)):    
        # tem um padrão para nomear o id de cada celular, com um index q usei aqui
        rank_xpath = ('//*[@id="p13n-asin-index-'+'%d'+'"]') % ind
        rank = cell.find_element('xpath',rank_xpath).text
        
        df.loc[ind,'info'] = rank
        df.loc[ind,'stars'] = st['title']
        
            
        ind = ind + 1 
        
        
        #print(rank,st['title'])

    return df

# queremos as 3 primeiras páginas, e previamente já verificamos que elas possuem o mesmo link com o número 
# diferente no final

df = []
# link, muda apenas o numero no final.
link = 'https://www.amazon.com.br/gp/bestsellers/electronics/16243890011/ref=zg_bs_pg_1?ie=UTF8&pg='
for i in range(1,4):
    a = coletar_dados_celulares((link+'%d')% i )
    df.append(a)
df=pd.concat(df)
df

df.to_excel('info_amazon.xlsx', header=True)
