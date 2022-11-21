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

dataINTERPOL = pd.DataFrame(columns=['Nombre', 'Apellido', 'Edad','Nacionalidad','Interpol'])

#Importar datos
filename = "Datos/Datos Gestion Documental Corregidos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
nombres = archivo["nombres_y_apellidos"].iloc[0:10]

#Datos de consulta
Apellido = []
Nombre =  []
Nacionalidad = "Colombia"
Edad = "22"

#Tratamiento de datos del dataframe
nombres= nombres.str.split(' ', expand=True)
nombres['nombres completos'] = nombres[0].str.cat(nombres[1],sep=' ')
nombres['apellidos completos'] = nombres[2].str.cat(nombres[3],sep=' ')
#Solicitud automatica
for i in nombres.index: 
    Nombre.append(nombres["nombres completos"][i])
    Apellido.append(nombres["apellidos completos"][i])

    # Opciones de navegación
    options =  webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    driver_path = 'C:\\Users\\CO-225\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'
    #driver_path = 'C:\\Users\\crahi\\appdata\\local\\programs\\python\\Python310\\Lib\\site-packages\\chromedriver.exe'
    driver = webdriver.Chrome(driver_path, chrome_options=options)
    # Iniciarla en la pantalla 2
    driver.set_window_position(200, 0)
    driver.maximize_window()
    time.sleep(1)

    #Inicializamos el navegador
    driver.get('https://www.interpol.int/es/Como-trabajamos/Notificaciones/Ver-las-notificaciones-rojas')


    time.sleep(1)
    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#name')))\
        .send_keys(Apellido[i])

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#forename')))\
        .send_keys(Nombre[i])

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'select#nationality.generalForm__selectArea')))\
        .send_keys(Nacionalidad)

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#ageMin')))\
        .send_keys('0')

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#ageMax')))\
        .send_keys('100')

    WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.privacy-cookie-banner__btn.btn')))\
    .click()

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.btn.btn--black')))\
        .click()
        
    time.sleep(1)
    resultado = driver.find_element(By.CSS_SELECTOR,'p#noSearchResults.redNoticesList__quantity')
    result = resultado.text
    # result.append(resultado)
    print(result)

    filanew = [Nombre[i],Apellido[i],Edad,Nacionalidad,result]
    dataINTERPOL.loc[i] =filanew
    # screenshot_name = "Archivos/"+"my_screenshot_name"+str(i)+".png"
    # driver.save_screenshot(screenshot_name)
    driver.quit()

dataINTERPOL.to_csv('Archivos/Antecedentes.csv', index=True)


