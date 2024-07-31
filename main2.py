from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time

def tamanho_iteracao(texto):
    partes = texto.split('-')
    numero1 = int(partes[0].strip())
    numero2 = int(partes[1].split()[0].strip())
    return (1 + numero2 - numero1)

def check_xpath_exists(driver, listXpath):
    updated_list = list_xpath.copy()
    for index, xpath in enumerate(updated_list):
        try:
            driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            updated_list[index] = ''
    return updated_list

servico = Service(ChromeDriverManager().install())

drive = webdriver.Chrome(service=servico)

url_concorrente = 'https://www.amazon.com.br/'

drive.get(url=url_concorrente)
time.sleep(1) 
drive.get(url='https://www.amazon.com.br/s?i=merchant-items&me=A9CE3IN6HXXI1&marketplaceID=A2Q3Y263D00KWC&qid=1722306203&ref=sr_pg_1')

controle = True
i = 0

while controle:
    total_itens_por_pagina = drive.find_element(By.XPATH, '//*[@id="search"]/span[2]/div/h1/div/div[1]/div/div/span').text #PEGA O TEXTO 1-16 de 232 resultados
    tamanho_iteracao = tamanho_iteracao(total_itens_por_pagina) # RETORNA O A QUANTIDADE DE ITENS EXIBIDOS NA TELA, 16
    for i in range(i+2, tamanho_iteracao):
        drive.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{i}]/div/div/span/div/div/div/div[1]/div/div[2]/div/span/a/div'.format(i=i)).click()

                                    #'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/span/div/div/div/div[1]/div/div[2]/div/span/a/div'
                                    #/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/span/div/div/div/div[1]/div/div[2]/div/span/a/div
                                    #/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/span/div/div/div/div[1]/div/div[2]/div/span/a/div

        list_xpath = [
            '//*[@id="productTitle"]', '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/span/div/div/div/div[1]/div/div[2]/div/span/a/div/img'
            '//*[@id="bylineInfo"]',
            '//*[@id="corePrice_feature_div"]/div/div/span[1]/span[2]/span[2]', # PREÇO DEZENA
            '//*[@id="corePrice_feature_div"]/div/div/span[1]/span[2]/span[3]', #PREÇO UNIDADE
            '//*[@id="dynamic-aod-ingress-box"]/div/div[2]/a/span/span[1]',
            '//*[@id="acrCustomerReviewText"]'
        ]
        listaConfirmada = check_xpath_exists(driver=drive, listXpath=list_xpath)
        time.sleep(2)

        resultado = [];
        time.sleep(2)
        for xpath in listaConfirmada:
            if(xpath != ''):
                resultado.append(drive.find_element(By.XPATH,xpath).text)
            else:
                print('não existe...')
        time.sleep(2)
        print('----------------------')
        print('Indice: {i}'.format(i=i))
        for x in resultado:
            print(x)
        i = i+1
    #drive.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[18]/div/div/span/a[3]').click()

# nome_produto = drive.find_element('xpath',xpath).text
# marca_produto = drive.find_element('xpath',xpath)
# preco_produto_dezena = drive.find_element('xpath',xpath)
# preco_produto_unidade = drive.find_element('xpath',xpath)
# total_ofertas = drive.find_element('xpath', xpath)
# comentarios = drive.find_element('xpath', xpath)


# drive.back()

# time.sleep(2) 





# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a/span

# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a/span

# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[4]/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a/span

# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[5]/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a/span

# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[17]/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a/span