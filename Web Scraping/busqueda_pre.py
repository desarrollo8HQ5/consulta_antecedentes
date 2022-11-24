# Librerías para webscraping
# Librerías complmentarias
import json
import os
import time
import glob
import win32com.client
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader

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
# 'concordato','desmovilizados','antecedentes_procuraduria','antecedentes_procuraduria',
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
antecedentes_procuraduria=[]
medidas_correctivas=[]
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

#directorio = "D:\\Consultas\\HQ5\\ciencia de datos\\Reto\\Consultas\\Sisben"
directorio = "C:\\Users\\CO-182\\Documents\\GitHub\\consulta_antecedentes\\Consultas"

prefs = {
    "printing.print_preview_sticky_settings.appState": json.dumps(appState),
    'savefile.default_directory':directorio,
    'download.default_directory':directorio
}
options.add_experimental_option("prefs", prefs)
options.add_argument('--kiosk-printing')

driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)
time.sleep(0.5)
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


    #Antecedentes procuraduría
    try:
        # Inicio de la navegación 
        driver.get('https://www.procuraduria.gov.co/Pages/Consulta-de-Antecedentes.aspx')
        time.sleep(0.5)
        # Cambiar al iframe
        element = driver.find_element(By.CLASS_NAME,'embed-responsive-item')
        driver.switch_to.frame(element)
        validador=0
        for x in range(10):
            #Obtener la pregunta de seguridad y validar respuestas que se tengan
            time.sleep(3)        
            pregunta=driver.find_element(By.XPATH,'//*[@id="lblPregunta"]').text
            if(pregunta.__contains__('Cuanto es 9 - 2')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('7')
                validador=1
                break
            elif(pregunta.__contains__('dos primeras letras del primer nombre')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys(str(Primer_Nombre[i])[:2])
                validador=1
                break
            elif(pregunta.__contains__('dos ultimos digitos del documento')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys(str(Documento[i])[len(str(Documento[i]))-2:len(str(Documento[i]))])
                validador=1
                break
            elif(pregunta.__contains__('cantidad de letras del primer nombre')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys(len(str(Primer_Nombre[i])))
                validador=1
                break
            elif(pregunta.__contains__('tres primeros digitos del documento a consultar')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys(str(Documento[i])[:3])
                validador=1
                break
            elif(pregunta.__contains__('Capital del Atlantico')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('barranquilla')
                validador=1
                break
            elif(pregunta.__contains__('Capital de Antioquia')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('medellin')
                validador=1
                break
            elif(pregunta.__contains__('6 + 2')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('8')
                validador=1
                break
            elif(pregunta.__contains__('3 - 2')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('1')
                validador=1
                break
            elif(pregunta.__contains__('2 X 3')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('6')
                validador=1
                break
            elif(pregunta.__contains__('Capital de Colombia')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('bogota')
                validador=1
                break
            else:
                driver.execute_script("location.reload()")
        if(validador==1):
            WebDriverWait(driver, 1)\
                .until(EC.element_to_be_clickable((By.ID,'ddlTipoID')))\
                .send_keys(str(Tipo_Documento[i]))
            time.sleep(1)
            WebDriverWait(driver, 1)\
                .until(EC.element_to_be_clickable((By.ID,'txtNumID')))\
                .send_keys(str(Documento[i]))
            time.sleep(1)  
            WebDriverWait(driver, 1)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="btnConsultar"]')))\
                .click()
            time.sleep(10)   
            for x in range(10):
                try:
                    resultado=driver.find_element(By.XPATH,'//*[@id="divSec"]/h2[2]').text
                    if(resultado.__contains__('El ciudadano no presenta antecedentes')):
                        antecedentes_procuraduria.append('SIN RESULTADOS')
                        break
                    else:
                        antecedentes_procuraduria.append('CON HALLAZGO') 
                        break
                except:
                    time.sleep(2)           
        else:
            antecedentes_procuraduria.append('FUENTE NO DISPONIBLE')
    except:
            antecedentes_procuraduria.append('FUENTE NO DISPONIBLE')

    driver.execute_script('window.print();')  
    time.sleep(1)  
    try:
        os.replace("Consultas\\Consulta de Antecedentes.pdf", "Consultas\\ANTECEDENTES_PROCURADURIA_"+str(Documento[i])+".pdf") 
    except:
        continue
    
    print(antecedentes_procuraduria)
driver.quit()
# data = pd.DataFrame({'DOCUMENTO':Documento,'MEDIDAS CORRECTIVAS':medidas_correctivas})
# data.to_csv('Reporte/Antecedentes.csv', index=True)