# Librerías para webscraping
# Librerías complmentarias
import json
import os
import time

import httplib2
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

#Importar datos
filename = "Datos/Con Hallazgos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
#Numero de registros a buscar   
datos = archivo.iloc[0:1]

#Datos de consulta
Primer_Nombre =  []
Segundo_Nombre =  []
Primer_Apellido =  []
Sengundo_Apellido =  []
Nombres = []
Apellidos = []
Edad = []
Tipo_Documento = []
Fecha_Expedicion = []
Departamento = []
Ciudad = []
Documento = []
Nacionalidad = []
interpol = []
ofac = []
sisben=[]
#Pruebas cristian
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver_path = 'C:\\Users\\CO-182\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\chromedriver.exe'
# Opciones de navegación
options = Options()
appState = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local"
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2
}
options.headless = False
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

#directorio = "D:\\Documentos\\HQ5\\ciencia de datos\\Reto\\Documentos\\Sisben"
directorio = "C:\\Users\\CO-182\\Desktop\\Reto 11-11-22\\Reto\\Documentos"

prefs = {
    "printing.print_preview_sticky_settings.appState": json.dumps(appState),
    'savefile.default_directory':directorio
}
options.add_experimental_option("prefs", prefs)
options.add_argument('--kiosk-printing')

driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)
time.sleep(1)
#Pruebas Cristian Fin

for i in datos.index:
    Primer_Nombre.append(archivo["primer_nombre"][i])
    Segundo_Nombre.append(archivo["segundo_nombre"][i])
    Primer_Apellido.append(archivo["primer_apellido"][i])
    Sengundo_Apellido.append(archivo["segundo_apellido"][i])
    if(str(Segundo_Nombre[i])=='nan'):
        Nombres.append(str(Primer_Nombre[i]))
    else:
        Nombres.append(str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]))
    Apellidos.append(str(Primer_Apellido[i])+" "+str(Sengundo_Apellido[i]))
    Edad.append(archivo["edad"][i])
    Tipo_Documento.append(archivo["tipo_de_documento"][i])
    Documento.append(archivo["documento"][i])
    Fecha_Expedicion.append(archivo["fecha_de_expedicion"][i])
    Ciudad.append(archivo["ciudad"][i])
    Departamento.append(archivo["departamento"][i])
    Nacionalidad.append(archivo["nacionalidad"][i])
    
    print(Apellidos)
    print(Nombres)
    #Inicio de la navegación
    driver.get('https://fcm.org.co/simit/#/home-public')
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 200)") 
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, -200)") 
    # driver.get('https://fcm.org.co/simit/#/home-public')
    driver.execute_script("location.reload()")
    time.sleep(20)
    for x in range(100):
        try:
            # ModalValidacion = driver.find_element(By.CSS_SELECTOR,'div#whcModal')
            ModalValidacion = driver.find_element(By.XPATH,'//*[@id="txtBusqueda"]')
            resultModal = ModalValidacion.text
            respuesta='1'
            if resultModal != "":
                time.sleep(1)
            else:
                break
        except:
            respuesta='0'
            driver.execute_script("location.reload()")  
            time.sleep(5)    
    if(respuesta=='1'):
        try:
            WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtBusqueda"]')))\
            .send_keys(str(Documento[i]))
            time.sleep(1)
            WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button#consultar')))\
                .click()
            time.sleep(3)
            try:
                tabla = driver.find_element(By.XPATH,'//*[@id="multaTable"]')
                resultado = 'CON MULTAS'
            except:
                resultado = 'SIN MULTAS'
            #Evidencia de la consulta
            driver.execute_script('window.print();')    
            time.sleep(2)
            os.replace("Documentos\\SIMIT _ Estado de la Cuenta.pdf", "Documentos\\SIMIT_"+str(Documento[i])+".pdf")
        except:
            resultado='PENDIENTE CONSULTAR'
    else:
        resultado='PENDIENTE CONSULTAR'
    print(resultado)
# driver.quit()