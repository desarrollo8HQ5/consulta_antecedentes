
# Librerías
from http.client import CONTINUE
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
dataMedidasCorrectivas = pd.DataFrame(columns=['Nombre','Apellido','Tipo_Documento','Documento','Fecha_Expedicion','PEPS'])

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
    Fecha_Expedicion.append(archivo["fecha_de_expedicion"][i])

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
    driver.get('https://srvcnpc.policia.gov.co/PSC/frm_cnp_consulta.aspx')
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ctl00_ContentPlaceHolder3_ddlTipoDoc')))\
        .send_keys(str(Tipo_Documento[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ctl00_ContentPlaceHolder3_txtExpediente')))\
        .send_keys(str(Documento[i]))
    time.sleep(1)

    if  str(Tipo_Documento[i]) in ('CEDULA DE CIUDADANIA'):
        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.ID,'txtFechaexp')))\
            .send_keys(str(Fecha_Expedicion[i]))
        time.sleep(1)
        boton_busqueda = '//*[@id="ctl00_ContentPlaceHolder3_btnConsultar2"]'
    else:
        boton_busqueda =  '//*[@id="ctl00_ContentPlaceHolder3_btnConsultar"]'
   

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,boton_busqueda)))\
        .click()
    time.sleep(1)

    Result = driver.find_element(By.XPATH,'//*[@id="flotante"]')
    Resultado = Result.text
    print(Resultado)

    if 'NO TIENE MEDIDAS CORRECTIVAS PENDIENTES POR CUMPLIR' in Resultado:
        Respuesta = 'NO TIENE MEDIDAS CORRECTIVAS PENDIENTES POR CUMPLIR'
        print(Respuesta)
        time.sleep(1)
        driver.execute_script('window.print();')
        time.sleep(2)
        time.sleep(2)
        os.rename("Documentos\\RNMC\\Consulta.pdf", "Documentos\\RNMC\\Medidas_Correctivas_"+str(Documento[i])+"_"+str(i)+".pdf")
        time.sleep(2)
        filanew = [str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]),str(Primer_Apellido[i])+" "+str(Segundo_Apellido[i]),str(Tipo_Documento[i]),str(Documento[i]),str(Fecha_Expedicion[i]),str(Respuesta)]
        dataMedidasCorrectivas.loc[i] =filanew
        driver.quit()
    else:
        if 'La Policía Nacional de Colombia informa' in Resultado:
            WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder3_gv_expedientes"]/tbody/tr[2]/td[1]/a')))\
                .click()
            time.sleep(2)

            Respuesta = driver.find_element(By.ID,'ctl00_ContentPlaceHolder3_pn_comportamiento')
            #Detalle Comportamiento Contrario a la Convivencia
            Comportamiento = driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder3_pn_comportamiento"]/div[1]')
            Respuesta_Comportamiento = Comportamiento.text
            #Medidas correctivas
            Medidas = driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder3_pn_comportamiento"]/div[2]')
            Respuesta_Medidas = Medidas.text

            time.sleep(1)
            driver.execute_script('window.print();')
            time.sleep(2)

            time.sleep(2)
            os.rename("Documentos\\RNMC\\Consulta.pdf", "Documentos\\RNMC\\Medidas_Correctivas_"+str(Documento[i])+"_"+str(i)+".pdf")
            time.sleep(2)
            
            filanew = [str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]),str(Primer_Apellido[i])+" "+str(Segundo_Apellido[i]),str(Tipo_Documento[i]),str(Documento[i]),str(Fecha_Expedicion[i]),str(Respuesta_Comportamiento)+"\n"+str(Respuesta_Medidas)]
            dataMedidasCorrectivas.loc[i] =filanew
            driver.quit()

    dataMedidasCorrectivas.to_csv('Archivos/Antecedentes.csv', index=True)
