# Librerías
from distutils.spawn import find_executable
from gettext import find
from unittest import result
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
dataSisben = pd.DataFrame(columns=['Nombre','Apellido','Tipo_Documento','Documento','Sisben'])

#Importar datos
filename = "Datos/Con Hallazgos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
datos = archivo.iloc[0:2]

#Datos de consulta
Primer_Nombre =  []
Segundo_Nombre =  []
Primer_Apellido =  []
Segundo_Apellido =  []
Tipo_Documento = []
Documento = []


# while True:

    # try:
for i in datos.index:

    Primer_Nombre.append(archivo["primer_nombre"][i])
    Segundo_Nombre.append(archivo["segundo_nombre"][i])
    Primer_Apellido.append(archivo["primer_apellido"][i])
    Segundo_Apellido.append(archivo["segundo_apellido"][i])
    Tipo_Documento.append(archivo["tipo_de_documento"][i])
    Documento.append(archivo["documento"][i])


    # Opciones de navegación
    options =  webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    driver_path = 'C:\\Users\\CO-225\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'
    #driver_path = 'C:\\Users\\crahi\\appdata\\local\\programs\\python\\Python310\\Lib\\site-packages\\chromedriver.exe'

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
    directorio = "C:\\Users\\CO-182\\Desktop\\Reto 11-11-22\\Reto\\Documentos\\Sisben"

    prefs = {
        "printing.print_preview_sticky_settings.appState": json.dumps(appState),
        'savefile.default_directory':directorio
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--kiosk-printing')

    driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)
    time.sleep(1)

    #Inicializamos el navegador
    driver.get('https://portal.sisben.gov.co/Paginas/consulta-tu-grupo.html')
    time.sleep(1)

    driver.execute_script("window.scrollBy(0,1000)")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0,1000)")
    time.sleep(1)

    #Select iFrame
    element = driver.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_ctl01__ControlWrapper_RichHtmlField"]/section/div/div[1]/div[12]/div/div/iframe')

    #Switch to iFrame
    driver.switch_to.frame(element)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'TipoID')))\
        .send_keys(str(Tipo_Documento[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'documento')))\
        .send_keys(str(Documento[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'botonenvio')))\
        .click()
    time.sleep(5)

    Result_pagina = driver.find_element(By.XPATH,'/html/body')
    Resultado_Pagina = Result_pagina.get_attribute('innerHTML')

    if 'swal2-title' in Resultado_Pagina:
        Result= driver.find_element(By.XPATH,'/html/body/div[2]/div')
        print(Result.text)


        time.sleep(1)
        driver.execute_script('window.print();')
        time.sleep(2)

        time.sleep(2)
        os.replace("Documentos\\Sisben\\Consulta tu Grupo Sisbén.pdf", "Documentos\\Sisben\\Sisben_"+str(Documento[i])+".pdf")
        time.sleep(2)

        filanew = [str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]),str(Primer_Apellido[i])+" "+str(Segundo_Apellido[i]),str(Tipo_Documento[i]),str(Documento[i]),str(Result)]
        dataSisben.loc[i] =filanew
        driver.quit()
    else:
        # Result = driver.find_element(By.XPATH,'/html/body/div[1]/main/div')
        # ## print(Result.text)

        # Grupo = driver.find_element(By.XPATH,'/html/body/div[1]/main/div/div[1]/div[2]/div/div[2]')
        # Grupo_Result = str(Grupo.text )
        # print(Grupo_Result)
        # time.sleep(1)
        driver.execute_script('window.print();')
        time.sleep(2)
        os.replace("Documentos\\Sisben\\Consulta tu Grupo Sisbén.pdf", "Documentos\\Sisben\\Sisben_"+str(Documento[i])+".pdf")
        time.sleep(2)

        # filanew = [str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]),str(Primer_Apellido[i])+" "+str(Segundo_Apellido[i]),str(Tipo_Documento[i]),str(Documento[i]),str(Grupo_Result)]
        # dataSisben.loc[i] =filanew
        

dataSisben.to_csv('Archivos/Antecedentes.csv', index=True)
    # break

    #1004274387
    #1030691395

    # except:
    #     print('volver a cargar la pagina')
    #     driver.quit()
    #     break
