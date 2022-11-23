# Consulta por juzgados general

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
import numpy as np
#Variables Globales
#result = list()
dataJuzgadosTyba = pd.DataFrame(columns=['Nombre', 'Apellido', 'Documento','Ciudad','Juzgados'])

#Importar datos
filename = "Datos/Datos Gestion Documental Corregidos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
#Numero de registros a buscar
datos = archivo.iloc[0:5]

#Datos de consulta
Primer_Nombre =  []
Segundo_Nombre =  []
Primer_Apellido =  []
Sengundo_Apellido =  []
Ciudad = []
Documento = []

for i in datos.index:
            
    Primer_Nombre.append(archivo["primer_nombre"][i])
    Segundo_Nombre.append(archivo["segundo_nombre"][i])
    Primer_Apellido.append(archivo["primer_apellido"][i])
    Sengundo_Apellido.append(archivo["segundo_apellido"][i])
    Ciudad.append(archivo["ciudad"][i])
    Documento.append(archivo["documento"][i])

    # Opciones de navegación
    options =  webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    #driver_path = 'C:\\Users\\CO-225\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'
    driver_path = 'C:\\Users\\crahi\\appdata\\local\\programs\\python\\Python310\\Lib\\site-packages\\chromedriver.exe'

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

    #directorio = "D:\\Documentos\\HQ5\\ciencia de datos\\Reto\\Documentos\\Juzgados"
    directorio = "C:\\Users\\CO-225\\Documents\\ciencia de datos\\Reto\\Documentos\\Juzgados"

    prefs = {
        "printing.print_preview_sticky_settings.appState": json.dumps(appState),
        'savefile.default_directory':directorio
    }

    options.add_experimental_option("prefs", prefs)
    options.add_argument('--kiosk-printing')

    driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)
    time.sleep(1)


    #Inicializamos el navegador
    driver.implicitly_wait(5)
    driver.get('https://procesos.ramajudicial.gov.co/procesoscs/ConsultaJusticias21.aspx?EntryId=KhFNqaxOiCvDXco6pZpZH53UrL8%3d')

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ddlJuzgados')))\
        .send_keys(str(Ciudad[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'btnIrJuzgados')))\
        .click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0]) 
    driver.close()
    driver.switch_to.window(driver.window_handles[0]) 
    driver.get(driver.current_url) 
    print(driver.title)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/p[2]/select')))\
        .send_keys('Documento de identificación del sujeto')
    time.sleep(1)
    # send_keys('apellidos del sujeto')
    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/p[2]/select')))\
        .send_keys('\ue007')
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'//html/body/form/p[3]/input[1]')))\
        .send_keys(str(Documento[i]))
    time.sleep(1)
    # .send_keys('por_nombre')
    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/p[3]/input[2]')))\
        .click()
    time.sleep(1)

    result = driver.find_elements(By.XPATH,"/html/body/div/font/font/center/p[1]/font[1]/font[1]/table/tbody/tr")
    Resultado_Previo = len(result)
    
    if Resultado_Previo == 2:
        Resultado = "NO HAY RESULTADO DE ANTECEDENTES JUDICIALES PARA ESTA PERSONA"
        print(Resultado)
        filanew = [str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]),str(Primer_Apellido[i])+" "+str(Sengundo_Apellido[i]),str(Documento[i]),str(Ciudad[i]),Resultado]
        dataJuzgadosTyba.loc[i] =filanew
        # screenshot_name = "Archivos/"+"my_screenshot_name"+str(i)+".pclearng"
        # driver.save_screenshot(screenshot_name)
        driver.quit()
    else:
        rows = len(driver.find_elements(By.XPATH,"/html/body/div/font/font/center/p[1]/font[1]/font[1]/table/tbody/tr")) 
        col = len(driver.find_elements(By.XPATH,"/html/body/div/font/font/center/p[1]/font[1]/font[1]/table/tbody/tr[1]/th"))
        #Imprimir antecedentes encontrados
        for n in range(3, rows+1):
            for b in range(1, col+1):
                if b == 1:
                    WebDriverWait(driver, 2)\
                        .until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/font/font/center/p[1]/font[1]/font[1]/table/tbody/tr["+str(n)+"]/td["+str(b)+"]")))\
                        .click()
                    #driver.switch_to.window(driver.window_handles) 
                    driver.get(driver.current_url) 
                    print(driver.current_url)
                    driver.execute_script('window.print();')
                    time.sleep(5)
                    os.rename("Documentos\\Juzgados\\Datos del Proceso.pdf", "Documentos\\Juzgados\\Juzgados_"+str(Documento[i])+"_"+str(n)+".pdf")
                    time.sleep(5)
                    driver.back()

                dato = driver.find_element(By.XPATH,"/html/body/div/font/font/center/p[1]/font[1]/font[1]/table/tbody/tr["+str(n)+"]/td["+str(b)+"]").text
                print(dato)
            print()
        Resultado ='Se encontraron '+str(rows-2)+' resultados'
        print ("filas=%s columnas=%s" % (rows, col))
        #Resultado = "Se encontraron resultados"
        
        filanew = [str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]),str(Primer_Apellido[i])+" "+str(Sengundo_Apellido[i]),str(Documento[i]),str(Ciudad[i]),Resultado]
        dataJuzgadosTyba.loc[i] =filanew
        # screenshot_name = "Archivos/"+"my_screenshot_name"+str(i)+".pclearng"
        # driver.save_screenshot(screenshot_name)
        driver.quit()

dataJuzgadosTyba.to_csv('Archivos/Antecedentes.csv', index=True)


