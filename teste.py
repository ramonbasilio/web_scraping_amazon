from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time

servico = Service(ChromeDriverManager().install())

drive = webdriver.Chrome(service=servico)

url_concorrente = 'https://www.amazon.com.br/'

url_pesquisa = 'https://www.amazon.com.br/Hinode-HYPE-FOR-HER/dp/B07NQHQ9C7/ref=sr_1_3?dib=eyJ2IjoiMSJ9.CsowlmUQy8zl8qE9Y8zNROMDoOlZNylCdYx3AhI68YTAbSslKoSc2kMnHZ31P96YC-Lt_oAQHA9IHm3qrtFWs38TxEZeX9G_hFxcJ0qwD3HPOZ3eEHBe_cnDbYCUXOrWiWTnI1ZMe5t3TdiD14jiamU_3ueghi0t_1bHWKfHEbx3fbhCp2vEn3z1Nc8E_O2H2yoIy8IzWWIPygy85mWpMGEUypW2Es3nDvhxr_Nhnnw.1xqCm43KRvXmCROIsRBOnIc-LG4ZgmYxTmewd1jlVAk&dib_tag=se&m=A2I3NDH4PQ94GD&marketplaceID=A2Q3Y263D00KWC&qid=1722398513&s=merchant-items&sr=1-3&ufe=app_do%3Aamzn1.fos.6d798eae-cadf-45de-946a-f477d47705b9'
elemento_xpath = '/html/body/div[2]/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/h1/span'
preco_1 =  '//*[@id="corePrice_feature_div"]/div/div/span[1]/span[2]/span[2]' # PREÇO DEZENA
preco_2 =  '//*[@id="corePrice_feature_div"]/div/div/span[1]/span[2]/span[3]'

drive.get(url=url_concorrente)
time.sleep(2) 
drive.get(url=url_pesquisa)
time.sleep(2)
elemento1 = ''
elemento2 = ''
for i in range(3):
    try:
        elemento1 = drive.find_element(By.XPATH, preco_1).text
        elemento2 = drive.find_element(By.XPATH, preco_2).text
        break
    except:
        print(f"tentativa {i+1}")

print(f"preço 1: {elemento1} preco 2: {elemento2}")

time.sleep(2)

# drive.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[18]/div/div/span/a[3]').click()
# time.sleep(2)
# drive.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[18]/div/div/span/a[3]').click()
# time.sleep(2)
# drive.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[18]/div/div/span/a[3]').click()
# time.sleep(2)
# drive.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[18]/div/div/span/a[3]').click()







