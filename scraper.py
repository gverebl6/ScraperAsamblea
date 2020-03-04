import requests
import time
from bs4 import BeautifulSoup 
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def getSoup(url):
    r = requests.get(url)
    if r.status_code == 200: 
        return BeautifulSoup(r.text, 'lxml')
    else:
        return None

def DinamicWait(driver, xpath, timeout=10):
    try: 
        res = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        time.sleep(2)
    except:
        print('La pagina tardo demasiado....')


def DriverDefinition():
    #Usar Selenium para extraer los nombres de archivos
    driver = webdriver.Chrome(executable_path='chromedriver')
    #Opciones del webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    return driver


def FileNameExtract(driver, url, pages_to_extract=1):
    file_names = []
    #GET a la pagina con la lista
    driver.get(url_tabla)
    
    
    #Extraer de todas las paginas
    for i in range(pages_to_extract):
        #Espera dinamica a que cargue
        DinamicWait(driver, '//div[@id="titulo"]', timeout=25)
        files = driver.find_elements_by_xpath('//div[@id="titulo"]')
        
        for file in files:
            file_names.append(file.get_attribute('innerHTML'))
        
        next_btn = driver.find_element_by_xpath('//div[@class="next"]')
        next_btn.click()
        
    
    return file_names
        

#La pagina de la asamble tiene un iframe conteniendo el link real de la tabla. 
url_tabla = getSoup('https://www.asamblea.gob.pa/actas-del-pleno').find('iframe').get('src')

#Declarar el driver
driver = DriverDefinition()

file_names = FileNameExtract(driver, url_tabla, pages_to_extract=2)

print(file_names, len(file_names))

driver.close()

# #TODO: Extraer los pdfs