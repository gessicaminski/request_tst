import requests 
from bs4 import BeautifulSoup
import time 
import pandas as pd

lista = pd.read_excel(r'C:\Users\gessi\Downloads\empresas_ailos (1).xlsx')

nome_fantasia= lista[lista['NomeFantasia'].notna()]
nome_fantasia['NomeFantasia']=nome_fantasia['NomeFantasia'].str.lower()
nome_fantasia['NomeFantasia']= nome_fantasia['NomeFantasia'].str.strip()
primeiras_100_linhas = nome_fantasia.head(100) #peguei nome fantasia e os 100 primeiros 
list_name= primeiras_100_linhas['NomeFantasia'].str.strip()
#list_name

df= pd.DataFrame(columns=['razao_social_pesquisa','nome_empregador','data_autuado','num_processo', 'link_processo' ])
df2=pd.DataFrame()

#lista_empresa=['sicredi', 'ilhaazul']
lista_empresa=list_name.tolist()
for empregador  in lista_empresa :
    empregador=empregador.replace(" ", "")
    print(empregador)
    url=f'https://consultaprocessual.tst.jus.br/consultaProcessual/empregadorForm.do?consultaPJE=1&nomeEmpregador={empregador}'
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")
    df.loc['razao_social_pesquisa']= empregador
    list_n = list (range(0,len(soup.find_all('table'))))

    if len(list_n ) == 0:
        print("A lista está vazia.")
        df['nome_empregador']= 'erro ou sem dado'
        df['data_autuado']= 'erroou sem dado'
    else:    
        list_n.remove(0)
        list_n.remove(1)
        list_n.remove(2)
        list_n.remove(3)
    for n  in list_n :
        t=soup.find_all('table')[n]
        '''if soup.get_text() == 'ErrorInternal Server Error':
        df['nome_empregador']= 'ErrorInternal Server Error' 
        elif:'''
        try:
            # Código que pode gerar um erro
            nm_empregador = t.find_all("font", {"color":"black"})[2].get_text()  # Tentando dividir por zero
        except Exception as e:
            # Outros tipos de erros
            print(f"Erro inesperado: {e}")
            df['nome_empregador']= f"Erro inesperado: {e}"

        else:
            nm_empregador = t.find_all("font", {"color":"black"})[2].get_text()
            nm_empregador=nm_empregador.replace('Empregador: ', '')
            df['nome_empregador']= nm_empregador
            data_autuado = t.find_all("font", {"color":"black"})[1].get_text()
            data_autuado = data_autuado.replace('Autuado em:', '')
            df['data_autuado']= data_autuado
            n_processo = t.find_all("a", {"class": "linkProcesso"})[0].get_text()
            df['num_processo']=n_processo
            link=t.find_all("a", {"class": "linkProcesso"})[0]
            link_processo =  link['href']
            df['link_processo']=link_processo
    df2=pd.concat([df, df2])

df3=df2.reset_index()
df3=df3.drop(columns=['index'])