from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import time
import pandas as pd
from datetime import datetime

print('')
print(' ------- Chupacabra 1.0 - By Ramon Basilio  ------- ')
print('')
url_concorrente_1 = input('Insira o link/url do vendedor Amazon: ')
print('')
print('Iniciando...')
print('Abrirá uma pagina do Chrome. Não se preocupe. Está tudo sob controle. Confie em mim!')


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
#url_concorrente_1 = 'https://www.amazon.com.br/sp?ie=UTF8&seller=A3GR3NYIKQSTKJ&isAmazonFulfilled=0&asin=B08X6BBZS7&ref_=olp_merch_name_2' 
nome_loja = ''



for i in range(5):
    try:
        drive.get(url=url_concorrente_1) 
        time.sleep(2)
        nome_loja = drive.find_element(By.XPATH, '//*[@id="seller-name"]').text
        time.sleep(1)
        drive.find_element(By.XPATH,'//*[@id="seller-info-storefront-link"]/span/a').click()
        total_itens_por_pagina = drive.find_element(By.XPATH, '//*[@id="search"]/span[2]/div/h1/div/div[1]/div/div/span').text
        time.sleep(1)
        break
    except:
        print(f'tentativa: {i+1}... calma pequeno gafanhoto...')

tamanho_iteracao = tamanho_iteracao(total_itens_por_pagina)
ultima_pagina = ultima_pagina(total_itens_por_pagina)

list_xpath = [
    '//*[@id="productTitle"]', #nome do produto
    '//*[@id="productDetails_techSpec_section_1"]/tbody/tr[1]/td', # fabricante
    '//*[@id="productDetails_techSpec_section_1"]/tbody/tr[6]/td',
    '//*[@id="corePrice_feature_div"]/div/div/span[1]/span[2]/span[2]', # PREÇO DEZENA
    '//*[@id="corePrice_feature_div"]/div/div/span[1]/span[2]/span[3]', #PREÇO UNIDADE
    '/html/body/div[2]/div/div[5]/div[3]/div[4]/div[3]/div/span[3]/a/span', #avaliações
    '/html/body/div[2]/div/div[5]/div[3]/div[1]/div[5]/div[2]/div/div[2]/a/span/span[1]' #ofertas
]

colunas = ['NomeProduto','Fabricante','Marca','Preço_Dez', 'Preço_Unid','Avaliações','Ofertas', 'URL']

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
                    #print(f"Tentativa de leitura: {i + 1}")
                    time.sleep(1)

            time.sleep(2)
            #listaConfirmada = check_xpath_exists(driver=drive, listXpath=list_xpath)
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
            #resultadoAtualizado = atulizaPreco(resultado)
            resultado.append(drive.current_url)
            #print(f"dados corrigido: {resultadoAtualizado}")

            # Verificar se os dados estão completos e válidos
            if len(resultado) != len(colunas):
                #print("Erro: número de colunas não corresponde.")
                continue


            # Verifique se cada valor na linha está correto
            # for i, value in enumerate(resultado):
            #     if not value:
            #         print(f"Aviso: Coluna {colunas[i]} está vazia ou incorreta.")

            df_temp = pd.DataFrame([resultado], columns=colunas)
            time.sleep(0.5)

            # Verificar conteúdo do df_temp antes de concatenação
            #print(f"df_temp:\n{df_temp}")

            df = pd.concat([df, df_temp], ignore_index=True)

            time.sleep(0.5)
            #print(f"DATAFRAME:\n{df}")
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
            #print(f"dados inicial: {resultado}")

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

print('Agora está tudo certo! Vamos começar...') 
print(f'Nome do vendedor: {nome_loja}')
for i in tqdm(range(ultima_pagina),               desc="Loading…", 
               ascii=False, ncols=75):
    for tentativa in range(5):
        try:
            funcListProducts2()
            drive.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[18]/div/div/span/a[3]').click()
            time.sleep(5)
            break
        except:
            #print(f"Tentativa: {tentativa + 1}")
            time.sleep(1)
    time.sleep(0.01)

print('Terminou. Abre a arquivo excel na pasta do programa. Boa sorte!')



# for i in range(ultima_pagina):
#     for tentativa in range(5):
#         try:
#             funcListProducts2()
#             drive.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[18]/div/div/span/a[3]').click()
#             time.sleep(5)
#             break
#         except:
#             print(f"Tentativa: {tentativa + 1}")
#             time.sleep(1)
    

df['preco'] = df['Preço_Dez'].astype(str)+','+ df['Preço_Unid'].astype(str)
#df['preco'] = df['preco'].astype(float)
df.drop(['Preço_Dez', 'Preço_Unid'], axis=1, inplace=True)
colunas = df.columns.tolist()
colunas.insert(2, colunas.pop(colunas.index('preco')))
df = df[colunas]


df.to_excel(f"{nome_arquivo}-{nome_loja}.xlsx", index=False)