## Busqueda de antecedentes por juzgado especifico

# Librerías
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select 

import time
import pandas as pd
import os

#Variables Globales
#result = list()
dataJuzgadosTyba = pd.DataFrame(columns=['Nombre', 'Apellido', 'Tipo_Documento','Documento','Libreta_Militar'])

#Importar datos
filename = "Datos/Datos Gestion Documental Corregidos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
datos = archivo.iloc[0:10]

#Datos de consulta
Primer_Nombre =  []
Segundo_Nombre =  []
Primer_Apellido =  []
Sengundo_Apellido =  []
Ciudad = []
    

for i in datos.index:
            
    Primer_Nombre.append(archivo["primer_nombre"][i])
    Segundo_Nombre.append(archivo["segundo_nombre"][i])
    Primer_Apellido.append(archivo["primer_apellido"][i])
    Sengundo_Apellido.append(archivo["segundo_apellido"][i])
    Ciudad.append(archivo["ciudad_de_residencia"][i])

    # Opciones de navegación
    options =  webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    #driver_path = 'C:\\Users\\CO-225\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'
    driver_path = 'C:\\Users\\crahi\\appdata\\local\\programs\\python\\Python310\\Lib\\site-packages\\chromedriver.exe'

    chromeOptions = webdriver.ChromeOptions()

    #directorio = "D:\\Documentos\\HQ5\\ciencia de datos\\Reto\\Documentos\\Libreta"
    directorio = "C:\\Users\\CO-225\\Documents\\ciencia de datos\\Reto\\Documentos"
    prefs = {"profile.default_content_settings.popups": 0,    
            "download.default_directory":directorio, ##Set the path accordingly
            "download.prompt_for_download": False, #change the downpath accordingly
            "download.directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)


    driver = webdriver.Chrome(driver_path, chrome_options=options)
    driver.set_window_position(200, 0)
    driver.maximize_window()
    time.sleep(1)

    #Inicializamos el navegador
    driver.get('https://procesos.ramajudicial.gov.co/procesoscs/ConsultaJusticias21.aspx?EntryId=KhFNqaxOiCvDXco6pZpZH53UrL8%3d')
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ddlCiudad"]')))\
        .send_keys(str(Ciudad[i]))
    time.sleep(10)

    Entidad =driver.find_element(By.ID,'ddlEntidadEspecialidad')
    opcion = Entidad.text.split('\n')
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ddlEntidadEspecialidad')))\
        .send_keys(str(opcion[1]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ddlEntidadEspecialidad')))\
        .send_keys('\ue007')
    time.sleep(1)

    Consulta =driver.find_element(By.ID,'rblConsulta')
    opcion_Consulta = Consulta.text.split('\n')
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'rblConsulta')))\
        .send_keys(str(opcion_Consulta[1]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'rblConsulta')))\
        .send_keys('\ue007')
    time.sleep(1)

    #Consulda demandado

    Tipo_Sujeto =driver.find_element(By.ID,'ddlTipoSujeto')
    opcion_Tipo_Sujeto = Tipo_Sujeto.text.split('\n')
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ddlTipoSujeto')))\
        .send_keys(str(opcion_Tipo_Sujeto[2]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ddlTipoSujeto')))\
        .send_keys('\ue007')
    time.sleep(1)

    Tipo_Persona =driver.find_element(By.ID,'ddlTipoPersona')
    opcion_Tipo_Persona = Tipo_Persona.text.split('\n')
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ddlTipoPersona')))\
        .send_keys(str(opcion_Tipo_Persona[1]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ddlTipoPersona')))\
        .send_keys('\ue007')
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'txtNatural')))\
        .send_keys(str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i])+" "+str(Primer_Apellido[i])+" "+str(Sengundo_Apellido[i]))
    time.sleep(1)


    slider = driver.find_element(By.CSS_SELECTOR,'input#btnConsultaNom')
    driver.execute_script("arguments[0].disabled = false", slider)
    time.sleep(2)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'btnConsultaNom')))\
        .click()
    time.sleep(3)

    #validar resultados cuando tiene y no tiene

    result_1 = driver.find_element(By.ID,'modalError')
    Resultados_1 = result_1.text

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="modalError"]/div/table/tbody/tr/td/input')))\
        .click()
    time.sleep(3)


    #Consulda demandado

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'btnNuevaConsultaNom')))\
        .click()
    time.sleep(3)


    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ddlTipoSujeto')))\
        .send_keys(str(opcion_Tipo_Sujeto[1]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ddlTipoSujeto')))\
        .send_keys('\ue007')
    time.sleep(1)

    slider = driver.find_element(By.CSS_SELECTOR,'input#btnConsultaNom')
    driver.execute_script("arguments[0].disabled = false", slider)
    time.sleep(2)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'btnConsultaNom')))\
        .click()
    time.sleep(3)

    #validar resultados cuando tiene y no tiene

    result_2 = driver.find_element(By.ID,'modalError')
    Resultados_2 = result_2.text

    print("primer resultado")
    print(Resultados_1)
    print("segundo resultado")
    print(Resultados_2)

    filanew = [Primer_Nombre[i]+" "+Segundo_Nombre[i],Primer_Apellido[i]+" "+Sengundo_Apellido[i],Ciudad[i],Resultados_1,Resultados_2]
    dataJuzgadosTyba.loc[i] =filanew
    # screenshot_name = "Archivos/"+"my_screenshot_name"+str(i)+".png"
    # driver.save_screenshot(screenshot_name)

    driver.quit