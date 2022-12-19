# Librerías para webscraping
# Librerías complementarias
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
from anticaptchaofficial.recaptchav2proxyless import *

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
personeria=[]
medidas_correctivas=[]
antecedentes_judiciales=[]
delitos_sexuales=[]

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


    #Delitos sexuales
    # try:
    #     # Inicio de la navegación  
    driver.get('https://inhabilidades.policia.gov.co:8080/')
    WebDriverWait(driver,1)\
        .until(EC.element_to_be_clickable((By.ID,'tipo')))\
        .send_keys(str(Tipo_Documento[i]))
    WebDriverWait(driver,1)\
        .until(EC.element_to_be_clickable((By.ID,'nuip')))\
        .send_keys(str(Documento[i]))
    WebDriverWait(driver,1)\
        .until(EC.element_to_be_clickable((By.ID,'fechaExpNuip')))\
        .send_keys(str(Fecha_Expedicion))
    WebDriverWait(driver,1)\
        .until(EC.element_to_be_clickable((By.ID,'nombreEmpresa')))\
        .click()
    WebDriverWait(driver,1)\
        .until(EC.element_to_be_clickable((By.ID,'nombreEmpresa')))\
        .send_keys('HQ5 S.A.S.')
    WebDriverWait(driver,1)\
        .until(EC.element_to_be_clickable((By.ID,'nitEmpresa')))\
        .send_keys('901023218-0')
    WebDriverWait(driver,1)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="frmCons"]/div[7]/label')))\
        .click()
    # Solucionar CAPTCHA
    #Obtener llave y la url del reCaptcha
    site_key=driver.find_element(By.XPATH,'//*[@id="captcha"]')
    site_key = str(site_key.get_attribute('data-sitekey'))
    site_url=driver.find_element(By.XPATH,'//*[@id="captcha"]/div/div/iframe')
    site_url = str(site_url.get_attribute('src'))
    print ('site_key: ' + site_key)
    print ('site_url: ' + site_url)
    # Mostrar espacio de key_response
    key_response = driver.find_element(By.XPATH,'//*[@id="g-recaptcha-response"]')
    driver.execute_script('var element=document.getElementById("g-recaptcha-response");element.style.display="block";')
    
     # Llamado al api para solucionar el captcha

    # solver = recaptchaV2Proxyless()
    # solver.set_verbose(1)
    # solver.set_key("cfe8dbdca00a0661d2d6d60bc14ef04b")
    # solver.set_website_url(site_url)
    # solver.set_website_key(site_key)
    # solver.set_soft_id(0)

    # g_response = solver.solve_and_return_solution()
    # if g_response != 0:
    #     print ("g-response: "+g_response)
    #     driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""",g_response)
    # else:
    #     print ("task finished with error "+solver.error_code)

    time.sleep(20)
    WebDriverWait(driver,1)\
        .until(EC.element_to_be_clickable((By.ID,'btnConsultar')))\
        .click()
    time.sleep(5)
    #Obteniendo resultados
    for r in range(20):
        try:
            result=driver.find_element(By.XPATH,'//*[@id="res"]/div/div/div/div/p[3]').text
            break
        except:
            time.sleep(1)
    try:
        if(result.__contains__('NO REGISTRA INHABILIDAD')):
            respuesta = 'SIN RESULTADOS'
        else:
            respuesta = 'CON HALLAZGO'
        
        WebDriverWait(driver,1)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="btnPrint"]')))\
        .click()       
    except:
        respuesta = 'FUENTE NO DISPONIBLE'
        driver.execute_script('window.print();')

    time.sleep(5)
    try:
        os.replace("Consultas\\Consulta de Inhabilidades.PDF", "Consultas\\Delitos_sexuales_"+str(Documento[i])+".PDF")
    except:
        continue
    delitos_sexuales.append(respuesta)
    print(delitos_sexuales)
driver.quit()
# data = pd.DataFrame({'DOCUMENTO':Documento,'PERSONERIA':personeria})
# data.to_csv('Reporte/Antecedentes.csv', index=True) 