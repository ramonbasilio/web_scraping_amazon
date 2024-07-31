from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


import time
import pandas as pd
from datetime import datetime



def tamanho_iteracao(texto):
    partes = texto.split('-')
    numero1 = int(partes[0].strip())
    numero2 = int(partes[1].split()[0].strip())
    return (1 + numero2 - numero1)

def ultima_pagina(texto):
    partes = texto.split('-')
    numero2 = int(partes[1].split()[0].strip())
    return numero2-1

def check_xpath_exists(driver, listXpath):
    updated_list = listXpath.copy()
    for index, xpath in enumerate(updated_list):
        try:
            driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            updated_list[index] = ''
    return updated_list

def atulizaPreco(lista):
    numero1 = lista[1]
    numero2 = lista[2]
    resultado = '{num1},{num2}'.format(num1= numero1, num2= numero2)
    lista.pop(1)
    lista.pop(1)
    lista.append(resultado)
    # print('Resultado da funcao: {lista}'.format(lista=lista))
    return lista

servico = Service(ChromeDriverManager().install())

drive = webdriver.Chrome(service=servico)

url_inicial = 'https://www.amazon.com.br/'
url_concorrente_1 = 'https://www.amazon.com.br/s?me=A2I3NDH4PQ94GD&marketplaceID=A2Q3Y263D00KWC' #Karina Iamada Multimarcas

drive.get(url=url_inicial)
time.sleep(1) 
drive.get(url=url_concorrente_1) 
time.sleep(1)
total_itens_por_pagina = drive.find_element(By.XPATH, '//*[@id="search"]/span[2]/div/h1/div/div[1]/div/div/span').text
time.sleep(1)
tamanho_iteracao = tamanho_iteracao(total_itens_por_pagina)
ultima_pagina = ultima_pagina(total_itens_por_pagina)

list_xpath = [
    '//*[@id="productTitle"]', #nome do produto
    '//*[@id="corePrice_feature_div"]/div/div/span[1]/span[2]/span[2]', # PREÇO DEZENA
    '//*[@id="corePrice_feature_div"]/div/div/span[1]/span[2]/span[3]', #PREÇO UNIDADE
    '/html/body/div[2]/div/div[5]/div[3]/div[4]/div[3]/div/span[3]/a/span', #avaliações
    '/html/body/div[2]/div/div[5]/div[3]/div[1]/div[5]/div[2]/div/div[2]/a/span/span[1]',
]

colunas = ['NomeProduto', 'Avaliações','Ofertas','Preço', 'URL']

df = pd.DataFrame(columns=colunas)

data_hora_atual = datetime.now()
nome_arquivo = data_hora_atual.strftime("%Y-%m-%d_%H-%M-%S")

def funcListProducts2():
    global df
    for x in range(tamanho_iteracao):
        x = x + 2
        try:
            for i in range(3):
                try:
                    drive.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{x}]/div/div/span/div/div/div/div[1]/div/div[2]/div/span/a/div'.format(x=x)).click()  # IMAGEM FOTO
                    break
                except:
                    print(f"Tentativa de leitura: {i + 1}")
                    time.sleep(1)

            time.sleep(2)
            #listaConfirmada = check_xpath_exists(driver=drive, listXpath=list_xpath)
            time.sleep(1)
            resultado = []

            for i, xpath in enumerate(list_xpath):
                try:
                    dado = drive.find_element(By.XPATH, xpath).text
                except NoSuchElementException:
                    dado = ''  # ou um valor padrão
                resultado.insert(i, dado)


                # if xpath != '':
                #     try:
                #         dado = drive.find_element(By.XPATH, xpath).text
                #     except NoSuchElementException:
                #         dado = ''  # ou um valor padrão
                #     resultado.insert(i, dado)
                # else:
                #     resultado.insert(i, '')

            #print(f"dados inicial: {resultado}")
            time.sleep(1)
            resultadoAtualizado = atulizaPreco(resultado)
            resultadoAtualizado.append(drive.current_url)
            #print(f"dados corrigido: {resultadoAtualizado}")

            # Verificar se os dados estão completos e válidos
            if len(resultadoAtualizado) != len(colunas):
                print("Erro: número de colunas não corresponde.")
                continue


            # Verifique se cada valor na linha está correto
            for i, value in enumerate(resultadoAtualizado):
                if not value:
                    print(f"Aviso: Coluna {colunas[i]} está vazia ou incorreta.")

            df_temp = pd.DataFrame([resultadoAtualizado], columns=colunas)
            time.sleep(0.5)

            # Verificar conteúdo do df_temp antes de concatenação
            #print(f"df_temp:\n{df_temp}")

            df = pd.concat([df, df_temp], ignore_index=True)
            time.sleep(0.5)
            print(f"DATAFRAME:\n{df}")
            drive.back()
        except NoSuchElementException:
            print('houve um erro...')



def funcListProducts():
    global df
    for x in range(tamanho_iteracao):
        x = x+2
        try:
            #/html/body/div[1]/div[1]/span[2]/div/h1/div/div[1]/div/div/span
            #//*[@id="search"]/span[2]/div/h1/div/div[1]/div/div/span
            for i in range(3):
                try:
                    drive.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{x}]/div/div/span/div/div/div/div[1]/div/div[2]/div/span/a/div'.format(x=x)).click() #IMAGEM FOTO
                    break
                except:
                    print(f"Tentativa de leitura: {i + 1}")
                    time.sleep(1)
            
            time.sleep(2)
            listaConfirmada = check_xpath_exists(driver=drive, listXpath=list_xpath)
            time.sleep(1)
            resultado = [];
            for i, xpath in enumerate(listaConfirmada):
                if(xpath != ''):
                    dado = drive.find_element(By.XPATH,xpath).text
                    resultado.insert(i, dado)
                elif(xpath == ''):
                    resultado.insert(i, '')
            print(f"dados inicial: {resultado}")

            time.sleep(1)
            resultadoAtualizado = atulizaPreco(resultado)
            print(f"dados corrigido: {resultadoAtualizado}")
            resultadoAtualizado.append(drive.current_url)
            df_temp = pd.DataFrame([resultadoAtualizado], columns=colunas)
            time.sleep(0.5)
            df = pd.concat([df, df_temp], ignore_index=True)
            time.sleep(0.5)
            #print(df)
            drive.back()
        except NoSuchElementException:
            print('houve um erro...')
        

for i in range(ultima_pagina):
    for tentativa in range(5):
        try:
            funcListProducts2()
            drive.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[18]/div/div/span/a[3]').click()
            time.sleep(5)
            break
        except:
            print(f"Tentativa: {tentativa + 1}")
            time.sleep(1)
    



df.to_excel(f"{nome_arquivo}-KarinaIamadaMultimarcas.xlsx", index=False)