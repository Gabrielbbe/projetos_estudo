import pandas as pd
import re


def extrair_gb(info): #extrai conjuntos de caracteres numéricos seguidos por letras, ou por espaço depois letras.
    gb = re.findall(r'\b[0-9]+\s*[A-Za-z]+\b',info)
    return gb

def remove_gb(info): # pra retornar as linhas limpas para o dataframe, assim tiramos o gb e tiramos ruido na hora de tirar outras informações.
    return re.sub(r'[0-9]+\s*GB', '', info) # remove o GB da string que vamos coletar, então podemos tirar ele da string e ter menos ruído 
#quando formos coletar as outra informações.

# função para verificar qual é maior e qual é a menor e retornar(ram,armazenamento)
# versão final
def ram_armz(lista):
    numeros = []
    for num in lista:
        numeros.append(re.findall('[0-9]+\s*GB$',num)) #string terminada em GB
        #    numeros = [int(i[0]) for i in numeros] #i[0] pq é uma sub-lista que o re retorna.
    return numeros

df = pd.read_excel("info_amazon.xlsx")

# transforma as linhas com quebra \n em colunas na ordem
df[['rank','info','n_avalicoes','preco']] = df['info'].apply(
    lambda x: pd.Series(str(x).split('\n') ) )

df = df.fillna(0) # preenche espaços vazios com zero


# limpando o stars.
# os primeiros dois caracteres são os números.
# limpa n avaliacoes
# limpa preco e transforma ele pra tipo numérico
print('limpando os dados')
for i in range(len(df['stars'])):
    
    df.loc[i,'stars'] = df.loc[i,'stars'][0:3]
    df.loc[i,'stars'] = df.loc[i,'stars'].replace(',','.')
    df.loc[i,'n_avalicoes'] = str(df.loc[i,'n_avalicoes'])
    if '$' in df.loc[i,'n_avalicoes']:
         df.loc[i,'preco'] = df.loc[i,'n_avalicoes'] # as vezes não tem o n_avaliacao e ele adiciona o preço no lugar
         df.loc[i,'n_avalicoes'] = 0 
    df.loc[i,'n_avalicoes'] = re.sub(r'[a-zA-Z]+',' ', str(df.loc[i,'n_avalicoes'])) # remove os caracteres
    df.loc[i,'n_avalicoes'] = str(df.loc[i,'n_avalicoes']).replace('.','') # remove pontos no num. de avaliacoes
    df.loc[i,'n_avalicoes'] = str(df.loc[i,'n_avalicoes']).replace(',','')
    df.loc[i,'n_avalicoes'] = int(df.loc[i,'n_avalicoes']) # transforma avaliacoes em int.
    df.loc[i,'preco'] = str(df['preco'][i])
    df.loc[i,'preco'] = df['preco'][i].replace(',','.')
    df.loc[i,'preco'] = re.sub(r'.+?(?=[R ])','', df['preco'][i]) # substitui tudo atrás de R$ por nada pra pegar só o preço
    
    df.loc[i,'rank'] = i+1
    
    if df['preco'][i].count('.') == 2 :
    
        df['preco'][i] = re.sub(r'[R$]', '',df['preco'][i]) 
        df['preco'][i] = re.sub(r'[A-Za-z]+', '',df['preco'][i]) 
        #print(i, df['preco'][i])
        df['preco'][i] = float(re.sub(r'\.{1}', '',df['preco'][i], count = 1) ) # remove a primeira aparição de um ponto
        #print(i, df['preco'][i])
    
    else: # se ele não tem dois pontos ele só pode ter um então só limpamos a string, pq um celular não vai custar milhoes
    
        df['preco'][i] = df['preco'][i][-10:] # pega os últimos 10 elementos da string pra evitar erro
        df['preco'][i]= re.sub(r'[R$]', '', df['preco'][i]) # limpa a string pra evitar erros
        df['preco'][i]= df['preco'][i].replace(',','.') # troca , por ponto pra normalizar

print('extraindo GB')
# Coletando os GB nas strings de info, titulo dos icones das paginas
GB = pd.DataFrame(columns=['ram','rom']) # vai ter duas colunas, ram e rom
ind = 0
for i in df['info']:
    #print(ind)
    linha = ram_armz(extrair_gb(str(df['info'][ind]).upper())) # lista com sub-listas.
    numeros = []

    for j in linha:
        if j == []:
            numeros = numeros
        else:
            numeros.append(re.findall('[0-9]+', j[0] ))

    numeros = [int(num[0]) for num in numeros]
    numeros = sorted(numeros)
    #print(numeros)

    if len(numeros)==0: # caso onde não temos a informação então temos uma lista vazia
        GB.loc[ind,'ram']=0 # então substituímos nas duas colunas por zero pra não atrapalhar nossa análise posteriormente 
        GB.loc[ind,'rom']=0 #

    if len(numeros) == 1:
        if numeros[0] > 6: # vamos considerar que + de 6GB seria de rom
            GB.loc[ind,'rom'] = numeros[0]
            GB.loc[ind,'ram'] = 0
        else:
            GB.loc[ind,'ram'] = numeros[0]
            GB.loc[ind,'rom'] = 0

    if len(numeros) == 2 :
        GB.loc[ind,'ram']=numeros[0] #menor numero seria a ram.
        GB.loc[ind,'rom']=numeros[1] #segundo maior numero seria a rom.

    if len(numeros) > 2:
        GB.loc[ind,'ram'] = numeros[0] # primeiro numero seria considerado a ram
        GB.loc[ind,'rom'] = numeros[(len(numeros)-1)] #ultimo numero seria considerado rom

    ind = ind + 1
    
df = pd.concat([df,GB.reindex(df.index)], axis=1)

#########################################################################
# script coletar marcas, 
marcas_df = pd.read_excel("marcas_celulares.xlsx")
marcas_df.drop(['Region','Country','Notes'], axis=1)


# pega a linha e verifica se a marca tá na linha retorna a marca, linha sem a marca, e o pais
# tentei tirar a marca da linha para pegar os modelos depois e ver os modelos + vendidos por marca mas acabou não dando certo.

def marca_dois(linha):
    # passar a linha como linha.upper() para normalizar.
    #linha = linha.upper()
    for index, brand in enumerate(marcas_df['Brand']):
        brand = str(brand)
        if brand.upper() in linha:
            
            return [brand.upper(), linha.replace(brand.upper(), " "), marcas_df.loc[index,'pais'] ]
        else:
            continue
        
    return None, linha, None

# gera uma tabela com as marcas e os pais da marca de cada linha.
coluna_marca2 = pd.DataFrame(columns=['marca','pais'])
ind = 0
for i in df['info']:
    m_linha = marca_dois( str(df['info'][ind]).upper() )
    #print(m_linha)
    coluna_marca2.loc[ind,'marca']= m_linha[0]
    #df.loc[ind,'info']=m_linha[1] # remove a marca da string para deixar ela mais limpa.
    coluna_marca2.loc[ind,'pais']= m_linha[2]
    
    ind = ind+1

#coluna_marca2

df = pd.concat([df,coluna_marca2],axis=1)

tab = df.groupby(['marca','pais']).size()
marcas = tab.index.to_list()
marcas = tab.index.to_list()
paises = []
brands = []
ind = 0
for i in (marcas):
    p, b = marcas[ind]
    paises.append(p)
    brands.append(b)
    ind = ind + 1

valores = [i for i in tab]

tab_df = {'marca': brands, 'paises':paises , 'valores': valores}
tab_df = pd.DataFrame(tab_df)

df.to_excel('df_final.xlsx')
tab_df.to_excel('marca_pais.xlsx')
