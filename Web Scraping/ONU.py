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
dataONU = pd.DataFrame(columns=['Nombre', 'Apellido','ONU'])

#Importar datos
filename = "Datos/Datos Gestion Documental Corregidos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
nombres = archivo["nombres_y_apellidos"].iloc[0:3]

#Datos de consulta
Apellido = []
Nombre =  []
Fecha_de_nacimiento = '10/01/1998'
Fecha_birth = []
Nacionalidad = "colombia"

#Tratamiento de datos del dataframe
nombres= nombres.str.split(' ', expand=True)
nombres['nombres completos'] = nombres[0].str.cat(nombres[1],sep=' ')
nombres['apellidos completos'] = nombres[2].str.cat(nombres[3],sep=' ')

Fecha_birth = Fecha_de_nacimiento.split(sep='/')
day = Fecha_birth[0]
month = Fecha_birth[1]
year = Fecha_birth[2]


#incluir el for aqui
for i in nombres:
    #Solicitud automatica
    Nombre.append(nombres["nombres completos"][i])
    Apellido.append(nombres["apellidos completos"][i])

    # Opciones de navegación
    options =  webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    driver_path = 'C:\\Users\\CO-182\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'

    driver = webdriver.Chrome(driver_path, chrome_options=options)
    # Iniciarla en la pantalla 2
    driver.set_window_position(200, 0)
    driver.maximize_window()
    time.sleep(1)

    #Inicializamos el navegador
    driver.get('https://scsanctions.un.org/search/')

    Nombre_Completo = Nombre[i]+" "+Apellido[i]
    
    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#include')))\
        .send_keys(Nombre)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'/html/body/center/form/table/tbody/tr[1]/td[7]/input')))\
        .click()

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="adv"]/u')))\
        .click()
    ##dia
    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'select#daydropdown')))\
        .send_keys(day)
    ##mes
    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'select#monthdropdown')))\
        .send_keys(month)
    ##año
    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'select#yeardropdown')))\
        .send_keys(year)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'select#nation')))\
        .send_keys(Nacionalidad)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'/html/body/center/form/table/tbody/tr[26]/td[3]/input')))\
        .click()
    try:
        resultado = driver.find_element(By.CSS_SELECTOR,'tr.rowtext')
        result = resultado.text
        print(result)
    except:
        result = "NO HAY RESULTADOS"
        print(result)

    filanew = [Nombre[i],Apellido[i],result]
    dataONU.loc[i] =filanew

    driver.quit()

dataONU.to_csv('Archivos/Antecedentes.csv', index=True)