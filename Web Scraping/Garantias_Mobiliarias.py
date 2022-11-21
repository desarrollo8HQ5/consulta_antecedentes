
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
dataMobiliarias = pd.DataFrame(columns=['Nombre','Apellido','Tipo_Documento','Documento','Garantias_Mobiliarias'])

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
Tipo_Documento = []
Documento = []
Fecha_Expedicion = []

for i in datos.index:

    Primer_Nombre.append(archivo["primer_nombre"][i])
    Segundo_Nombre.append(archivo["segundo_nombre"][i])
    Primer_Apellido.append(archivo["primer_apellido"][i])
    Segundo_Apellido.append(archivo["primer_apellido"][i])
    Tipo_Documento.append(archivo["tipo_de_documento"][i])
    Documento.append(archivo["documento"][i])

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
    driver_path = 'C:\\Users\\CO-225\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'
    #driver_path = 'C:\\Users\\crahi\\appdata\\local\\programs\\python\\Python310\\Lib\\site-packages\\chromedriver.exe'

    directorio = "C:\\Users\\CO-225\\Documents\\ciencia de datos\\Reto\\Documentos\\RNMC"
    #directorio = "D:\\Documentos\\HQ5\\ciencia de datos\\Reto\\Documentos\\RNMC"

    prefs = {
    "printing.print_preview_sticky_settings.appState": json.dumps(appState),
    'savefile.default_directory':directorio
    }

    options.add_experimental_option("prefs", prefs)
    options.add_argument('--kiosk-printing')

    driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)
    time.sleep(1)

    #Inicializamos el navegador
    driver.get('https://www.garantiasmobiliarias.com.co/')
    time.sleep(1)

    WebDriverWait(driver, 2)\
    .until(EC.element_to_be_clickable((By.ID,'ContentPlaceHolderSeguridad_ContentPlaceHolderContenido_txtNumeroIdentificacion')))\
    .send_keys(str(Documento[0]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
    .until(EC.element_to_be_clickable((By.ID,'ContentPlaceHolderSeguridad_ContentPlaceHolderContenido_btnConsultarIdentificacion')))\
    .click()
    time.sleep(1)


    result = driver.find_element(By.ID,'ContentPlaceHolderSeguridad_ContentPlaceHolderContenido_upBusqueda')
    Resultado = result.text
    print(result.text)
    filanew = [str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]),str(Primer_Apellido[i])+" "+str(Segundo_Apellido[i]),str(Tipo_Documento[i]),str(Documento[i]),str(Resultado)]
    dataMobiliarias.loc[i] =filanew
    driver.quit()

dataMobiliarias.to_csv('Archivos/Antecedentes.csv', index=True)

