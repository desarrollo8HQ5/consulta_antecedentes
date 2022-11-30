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
# 'concordato','desmovilizados','personeria','personeria',
# 'rama_judicial','simit','ruaf','secop_s',
# 'peps','rnmc','libreta_militar','contadores_sancionados',
# 'garantias_mobiliarias','secop','sisben'])

#Importar datos
# filename = "Datos/Con Hallazgos.csv"
# fullpath = os.path.join(filename)
archivo = pd.read_csv("C:/Users/CO-182/Documents/GitHub/consulta_antecedentes/Datos/Con Hallazgos.csv")
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
Fecha_Nacimiento=[]
interpol = []
ofac = []
sisben=[]
simit=[]
onu=[]
desmovilizados=[]
personeria=[]
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


    #Antecedentes personeria
    try:
        # Inicio de la navegación  
        driver.get('https://www.personeriabogota.gov.co/al-servicio-de-la-ciudad/expedicion-de-antecedentes')
        driver.execute_script("window.scrollTo(0,700)")
        time.sleep(2)
        element = driver.find_element(By.ID,'ir-formulario')
        driver.switch_to.frame(element)
        WebDriverWait(driver,1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/p/div[1]/button')))\
            .click()
        time.sleep(1)
        WebDriverWait(driver,1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="collapseAntecedete"]/div/form/div[1]/div[1]/select')))\
            .send_keys(str(Tipo_Documento[i]))
        time.sleep(1)
        WebDriverWait(driver,1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="numDoc"]')))\
            .send_keys(str(Documento[i]))    
        time.sleep(2)
        if(str(Tipo_Documento[i]).__contains__('CEDULA DE CIUDADANIA')):
            for x in range(20):
                pregunta = driver.find_element(By.XPATH,'//*[@id="collapseAntecedete"]/div/form/div[2]/div[2]/div/label').text
                if(pregunta.__contains__('7 * 1')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('7')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 2')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('14')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 3')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('21')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 4')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('28')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 5')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('35')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 6')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('42')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 7')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('49')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 8')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('56')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 9')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('63')
                    time.sleep(1)
                    break
                else:
                    driver.switch_to.default_content()
                    driver.execute_script("location.reload()")
                    time.sleep(2)
                    element = driver.find_element(By.ID,'ir-formulario')
                    driver.switch_to.frame(element)
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/p/div[1]/button')))\
                        .click()
                    time.sleep(1)
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="collapseAntecedete"]/div/form/div[1]/div[1]/select')))\
                        .send_keys(str(Tipo_Documento[i]))
                    time.sleep(1)
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="numDoc"]')))\
                        .send_keys(str(Documento[i]))    
                    time.sleep(2)
        WebDriverWait(driver,1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="collapseAntecedete"]/div/form/button')))\
            .click()
        time.sleep(1)
        for x in range(20):
            try:
                WebDriverWait(driver,1)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div[2]/form/div[2]/div/a')))\
                .click()
                break
            except:
                time.sleep(2)
        time.sleep(1)
        personeria.append('CONSULTADO')
        try:
            os.replace("Consultas\\antecedente_disciplinario.pdf","Consultas\\PERSONERIA_"+str(Documento[i])+".pdf")
        except:
            continue
    except:    
        personeria.append('FUENTE NO DISPONIBLE')

    
    print(personeria)
driver.quit()
data = pd.DataFrame({'DOCUMENTO':Documento,'PERSONERIA':personeria})
data.to_csv('Reporte/Antecedentes.csv', index=True)