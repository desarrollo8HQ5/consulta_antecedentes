# Librerías
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

#Variables Globales
#result = list()
dataOFAC = pd.DataFrame(columns=['Nombres','Apellidos','Documento', 'Nacionalidad','OFAC'])

#Importar datos
filename = "Datos/Datos Gestion Documental Corregidos 2.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
nombres = archivo["nombres_y_apellidos"].iloc[0:3]
Documentos = archivo["documento"].iloc[0:3]

#Datos de consulta
PrimerNombre = []
SegundoNombre =  []
PrimerApellido =  []
SegundoApelldio =  []
Nacionalidad = "Colombia"
Documento = []

#Tratamiento de datos del dataframe
nombres= nombres.str.split(' ', expand=True)
nombres = nombres.rename(columns={0:'primer nombre', 1:'segundo nombre', 2:'primer apellido',3:'segundo apellido'})

 #incluir el for aqui
for i in nombres.index:
    #Solicitud automatica
    PrimerNombre.append(nombres["primer nombre"][i])
    SegundoNombre.append(nombres["segundo nombre"][i])
    PrimerApellido.append(nombres["primer apellido"][i])
    SegundoApelldio.append(nombres["segundo apellido"][i])

    Documento.append(archivo["documento"][i])

    
    # Opciones de navegación
    options =  webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    driver_path = 'C:\\Users\\CO-225\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'

    driver = webdriver.Chrome(driver_path, chrome_options=options)
    # Iniciarla en la pantalla 2
    driver.set_window_position(200, 0)
    driver.maximize_window()
    time.sleep(1)

    # Inicializamos el navegador
    driver.get('https://sanctionssearch.ofac.treas.gov/')

    time.sleep(1)

    # WebDriverWait(driver, 2)\
    #     .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_MainContent_txtLastName"]')))\
    #     .send_keys(PrimerNombre[i])


    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_MainContent_txtID"]')))\
        .send_keys(str(Documento[i]))

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_MainContent_ddlCountry"]')))\
        .send_keys("Colombia")

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_MainContent_btnSearch"]')))\
        .click()

    time.sleep(1)
    resultado = driver.find_element(By.XPATH,'//*[@id="scrollResults"]')
    result = resultado.text
    print(result)

    filanew = [PrimerNombre[i],PrimerApellido[i],Documento[i],Nacionalidad,result]
    dataOFAC.loc[i] =filanew
    # screenshot_name = "Archivos/"+"my_screenshot_name"+str(i)+".png"
    # driver.save_screenshot(screenshot_name)
    driver.quit()

    dataOFAC.to_csv('Archivos/Antecedentes.csv', index=True)
