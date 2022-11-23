# Librerías para webscraping
# Librerías complmentarias
import json
import os
import time
import glob
import win32com.client

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

#Variables Globales
#result = list()

#Dataframe de almacenamiento
# data = pd.DataFrame(columns=['primer_nombre', 'segundo_nombre', 'primer_apellido','segundo_apellido',
# 'edad','fecha_expedicion','tipo_de_documento','documento','departamento','ciudad',
# 'interpol','ofac','onu','proveedores_ficticios',
# 'concordato','desmovilizados','europol','europol',
# 'rama_judicial','simit','ruaf','secop_s',
# 'peps','rnmc','libreta_militar','contadores_sancionados',
# 'garantias_mobiliarias','secop','sisben'])

#Importar datos
# filename = "Datos/Con Hallazgos.csv"
# fullpath = os.path.join(filename)
archivo = pd.read_csv("C:/Users/CO-182/Documents/GitHub/consulta_antecedentes/Datos/Con Hallazgos.csv")
#Numero de registros a buscar   
datos = archivo.iloc[0:4]
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
Fecha_Nacimiento=[]
interpol = []
ofac = []
sisben=[]
simit=[]
onu=[]
desmovilizados=[]
europol=[]
#Pruebas cristian
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver_path = 'C:\\Users\\CO-182\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'
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
directorio = "C:\\Users\\CO-182\\Documents\\GitHub\\consulta_antecedentes\\Documentos"

prefs = {
    "printing.print_preview_sticky_settings.appState": json.dumps(appState),
    'savefile.default_directory':directorio,
    "download.default_directory":directorio
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
    Fecha_Nacimiento.append(archivo["fecha_de_nacimiento"][i])
    Fecha_birth = Fecha_Nacimiento[i].split(sep='/')
    day = Fecha_birth[0]
    month = Fecha_birth[1]
    year = Fecha_birth[2]

    #Rama unificada
    #Inicio de la navegación 
    driver.get('https://eumostwanted.eu/es')
    try:
        time.sleep(1)
        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#edit-search-block-form--2')))\
            .send_keys(Primer_Apellido[i]+", "+Primer_Nombre[i])

        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button#edit-submit.secondary button radius postfix expand form-submit'.replace(' ', '.'))))\
            .click()
            
        time.sleep(1)
        result = driver.find_element(By.ID,'#searchResults').text
        print(result)
        europol.append('FUENTE DISPONIBLE')
    except:
        europol.append('FUENTE NO DISPONIBLE')
        # driver.execute_script('window.print();')
        # time.sleep(2)
        # os.replace("Documentos\\Consulta de Procesos por Nombre o Razón Social- Consejo Superior de la Judicatura.pdf", "Documentos\\RAMA_UNIFICADA_"+str(Documento[i])+".pdf")
driver.quit()
data = pd.DataFrame({'DOCUMENTO':Documento,'RAMA_UNIFICADA':europol})
data.to_csv('Archivos/Antecedentes.csv', index=True)