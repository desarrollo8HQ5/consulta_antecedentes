# Librerías
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

import time
import pandas as pd
import os

#Variables Globales
#result = list()
dataJuzgadosUnificada= pd.DataFrame(columns=['Nombre', 'Apellido','Documento','Departamento','Ciudad','Juzgados_Unificado'])

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
Departamento = []
Documento = []

dataEncontrada = pd.DataFrame(columns=['consultado', 'numero_de_radicacion', 'fecha_de_radicacion_y_ultima_actuacion','despacho_y_departamento','sujetos_procesales'])

consultado = []
numero_de_radicacion = []
fecha_de_radicacion_y_ultima_actuacion = []
despacho_y_departamento = []
sujetos_procesales = []

for i in datos.index:
        
    Primer_Nombre.append(archivo["primer_nombre"][i])
    Segundo_Nombre.append(archivo["segundo_nombre"][i])
    Primer_Apellido.append(archivo["primer_apellido"][i])
    Segundo_Apellido.append(archivo["segundo_apellido"][i])
    Departamento.append(archivo["departamento"][i])
    Ciudad.append(archivo["ciudad"][i])
    Documento.append(archivo["documento"][i])

    #Opciones de navegación
    options =  webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    driver_path = 'C:\\Users\\CO-225\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'
    #driver_path = 'C:\\Users\\crahi\\appdata\\local\\programs\\python\\Python310\\Lib\\site-packages\\chromedriver.exe'

    chromeOptions = webdriver.ChromeOptions()

    directorio = "D:\\Documentos\\HQ5\\ciencia de datos\\Reto\\Documentos\\Juzgados_Unificada"
    #directorio = "C:\\Users\\CO-225\\Documents\\ciencia de datos\\Reto\\Documentos\\Juzgados_Unificada"
    prefs = {"profile.default_content_settings.popups": 0,    
            "download.default_directory":directorio, ##Set the path accordingly
            "download.prompt_for_download": False, #change the downpath accordingly
            "download.directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(driver_path, chrome_options=options)
    #Iniciarla en la pantalla 
    driver.set_window_position(200, 0)
    driver.maximize_window()
    time.sleep(1)


    driver = webdriver.Chrome(driver_path, chrome_options=options)
    driver.set_window_position(200, 0)
    driver.maximize_window()
    time.sleep(1)

    #Inicializamos el navegador
    driver.get('https://consultaprocesos.ramajudicial.gov.co/Procesos/NombreRazonSocial')
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="mainContent"]/div/div/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[2]/div/div')))\
        .click()
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'input-72')))\
        .send_keys("Natural")
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'input-78')))\
        .send_keys(str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i])+" "+str(Primer_Nombre[i])+" "+str(Segundo_Apellido[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'input-83')))\
        .send_keys(str(Departamento[i]))
    time.sleep(1)

    driver.execute_script("window.scrollBy(0,900)")
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'input-89')))\
        .send_keys(str(Ciudad[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="mainContent"]/div/div/div/div[1]/div/div[2]/div/div[5]/button[1]/span')))\
        .click()
    time.sleep(10)

    try:
        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[4]/div/div/div[2]/div/button/span')))\
            .click()
        time.sleep(1)
    except:
        continue

    result = driver.find_element(By.XPATH,'//*[@id="app"]/div[4]/div/div')
    Resultado_Consultado = str(Resultado_Consultado.text)
    if 'La consulta no generó resultados' in Resultado_Consultado:
        Resultado = 'La consulta no generó resultados, por favor revisar las opciones ingresadas e intentarlo nuevamente.'
        filanew = [str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]),str(Primer_Apellido[i])+" "+str(Segundo_Apellido[i]),str(Documento[i]),str(Departamento[i]),str(Ciudad[i]),Resultado]
        dataJuzgadosUnificada.loc[i] =filanew
        driver.quit()
    elif 'Se han encontrado varios registros' in Resultado_Consultado:
        rows =  len(driver.find_elements(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div/table/tbody/tr'))
        col =  len(driver.find_elements(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div/table/thead/tr[1]/th'))
        Resultado ='Se encontraron '+str(rows)+' resultados'
        print ("filas=%s columnas=%s" % (rows, col))

        #Imprimir antecedentes encontrados
        for n in range(1, rows+1):
            for b in range(1, col+1):
                if b == 1:
                    col_1 = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div/table/tbody/tr['+str(n)+']/td['+str(b)+']')
                    consultado.append(str(col_1.text))
                if b == 2:
                    col_2 = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div/table/tbody/tr['+str(n)+']/td['+str(b)+']')
                    numero_de_radicacion.append(str(col_2.text))
                if b == 3:
                    col_3 = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div/table/tbody/tr['+str(n)+']/td['+str(b)+']')
                    fecha_de_radicacion_y_ultima_actuacion.append(str(col_3.text))
                if b == 4:
                    col_4 = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div/table/tbody/tr['+str(n)+']/td['+str(b)+']')
                    despacho_y_departamento.append(str(col_4.text))
                if b == 5:
                    col_5 = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div/table/tbody/tr['+str(n)+']/td['+str(b)+']')
                    sujetos_procesales.append(str(col_5.text))

            filanew_dataEncontrada = [consultado[n-1],numero_de_radicacion[n-1],fecha_de_radicacion_y_ultima_actuacion[n-1],despacho_y_departamento[n-1],sujetos_procesales[n-1]]
            dataEncontrada.loc[n] =filanew_dataEncontrada
        dataEncontrada.to_csv('Documentos/Juzgados_Unificada/Consulta_Juzgados_Unificado_'+str(Documento[i])+'.csv', index=True)
        
        filanew = [str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]),str(Primer_Apellido[i])+" "+str(Segundo_Apellido[i]),str(Documento[i]),str(Departamento[i]),str(Ciudad[i]),Resultado]
        dataJuzgadosUnificada.loc[i] =filanew
        driver.quit()
dataJuzgadosUnificada.to_csv('Archivos/Antecedentes.csv', index=True)