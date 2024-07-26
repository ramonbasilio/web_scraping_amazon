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
drive.get(url='https://www.amazon.com.br/s?me=A9CE3IN6HXXI1&marketplaceID=A2Q3Y263D00KWC') 

total_itens_por_pagina = drive.find_element(By.XPATH, '//*[@id="search"]/span[2]/div/h1/div/div[1]/div/div/span').text
tamanho_iteracao = tamanho_iteracao(total_itens_por_pagina)

for x in range(tamanho_iteracao):
    x = x+2
    drive.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{x}]/div/div/span/div/div/div/div[1]/div/div[2]/div/span/a/div'.format(x=x)).click()

    list_xpath = [
        '//*[@id="productTitle"]',
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
    print('Indice: {x}'.format(x=x))
    for x in resultado:
        print(x)
    drive.back()

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