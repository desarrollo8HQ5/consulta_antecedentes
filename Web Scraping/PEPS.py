# Librerías
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
import json

import time
import pandas as pd
import os


#Variables Globales
#result = list()
dataPEP = pd.DataFrame(columns=['Nombre','Apellido','Documento','PEPS'])

#Importar datos
filename = "Datos/Datos Gestion Documental Corregidos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
datos = archivo.iloc[0:10]

#Datos de consulta
Primer_Nombre =  []
Segundo_Nombre =  []
Primer_Apellido =  []
Segundo_Apellido =  []
Ciudad = []
Documento = []

for i in datos.index:
    Primer_Nombre.append(archivo["primer_nombre"][i])
    Segundo_Nombre.append(archivo["segundo_nombre"][i])
    Primer_Apellido.append(archivo["primer_apellido"][i])
    Segundo_Apellido.append(archivo["segundo_apellido"][i])
    Ciudad.append(archivo["ciudad_de_residencia"][i])
    Documento.append(archivo["documento"][i])

    # Opciones de navegación
    options =  Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    driver_path = 'C:\\Users\\CO-225\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'
    #driver_path = 'C:\\Users\\crahi\\appdata\\local\\programs\\python\\Python310\\Lib\\site-packages\\chromedriver.exe'

    chromeOptions = webdriver.ChromeOptions()

    directorio = "C:\\Users\\CO-225\\Documents\\ciencia de datos\\Reto\\Documentos\\PEP"
    #directorio = "D:\\Documentos\\HQ5\\ciencia de datos\\Reto\\Documentos\\PEP"
    prefs = {"profile.default_content_settings.popups": 0,    
            "download.default_directory":directorio, ##Set the path accordingly
            "download.prompt_for_download": False, #change the downpath accordingly
            "download.directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(driver_path, chrome_options=options)
    #Inicializamos el navegador
    driver.get('https://www.funcionpublica.gov.co/fdci/consultaCiudadana/consultaPEP')
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'numeroDocumento')))\
        .send_keys(str(Documento[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'primerNombre')))\
        .send_keys(str(Primer_Nombre[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'segundoNombre')))\
        .send_keys(str(Segundo_Nombre[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'primerApellido')))\
        .send_keys(str(Primer_Apellido[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'segundoApellido')))\
        .send_keys(str(Segundo_Apellido[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'find')))\
        .click()
    time.sleep(1)

    Result = driver.find_element(By.XPATH,'//*[@id="list-consultaCiudadana"]/div[3]')
    Resultado_Consulta = Result.text


    if "No se encuentran declaraciones" in str(Resultado_Consulta) :
        Resultado = "No se encuentran declaraciones publicadas según los datos de consulta suministrados"
        print(Resultado_Consulta)
    else:
        rows =  len(driver.find_elements(By.XPATH,'//*[@id="list-consultaCiudadana"]/div[3]/table/tbody/tr'))
        col =  len(driver.find_elements(By.XPATH,'//*[@id="list-consultaCiudadana"]/div[3]/table/thead/tr[1]/th'))
        Resultado ='Se encontraron '+str(rows)+' resultados'
        print ("filas=%s columnas=%s" % (rows, col))
        #Descargar antecedentes encontrados
        for n in range(1, rows+1):
            for b in range(1, col+1):
                if b == 2:
                    descargar = driver.find_element(By.XPATH, '//*[@id="list-consultaCiudadana"]/div[3]/table/tbody/tr['+str(n)+']/td['+str(b)+']')
                    WebDriverWait(descargar, 2)\
                        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.btn.btn-outline-dark.mb-3.mt-3.btn-sm')))\
                        .click()
                    time.sleep(5)
                    os.rename("Documentos\\PEP\\REPORTE.zip", "Documentos\\PEP\\REPORTE_"+str(Documento[i])+"_"+str(n)+".zip")
                    time.sleep(5)
    filanew = [str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]),str(Primer_Apellido[i])+" "+str(Segundo_Apellido[i]),str(Documento[i]),Resultado]
    dataPEP.loc[i] =filanew
    # screenshot_name = "Archivos/"+"my_screenshot_name"+str(i)+".pclearng"
    # driver.save_screenshot(screenshot_name)
    driver.quit()

dataPEP.to_csv('Archivos/Antecedentes.csv', index=True)
