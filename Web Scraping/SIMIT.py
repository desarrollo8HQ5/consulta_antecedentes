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

dataSIMIT = pd.DataFrame(columns=['Nombre', 'Apellido', 'Placa','SIMIT'])

#Importar datos
filename = "Datos/Datos Gestion Documental Corregidos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
nombres = archivo["nombres_y_apellidos"].iloc[0:10]

#Datos de consulta
Apellido = []
Nombre =  []


#Tratamiento de datos del dataframe
nombres= nombres.str.split(' ', expand=True)
nombres['nombres completos'] = nombres[0].str.cat(nombres[1],sep=' ')
nombres['apellidos completos'] = nombres[2].str.cat(nombres[3],sep=' ')


#Solicitud automatica
for i in nombres.index: 
    Nombre.append(nombres["nombres completos"][i])
    Apellido.append(nombres["apellidos completos"][i])
    Placa = ['ASJ999','AUJ999','AXZ999','AZZ999','AXK000','AZA000','AZN000','ANK999','CNM999','CPL999','CRR000']

    # Opciones de navegación

    options =  webdriver.ChromeOptions()
    options.headless = False
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    driver_path = 'C:\\Users\\CO-182\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'
    #driver_path = 'C:\\Users\\crahi\\appdata\\local\\programs\\python\\Python310\\Lib\\site-packages\\chromedriver.exe'
    driver = webdriver.Chrome(driver_path, chrome_options=options)
    # Iniciarla en la pantalla 2
    driver.set_window_position(200, 0)
    driver.maximize_window()
    time.sleep(1)

    #Inicializamos el navegador
    driver.get('https://fcm.org.co/simit/#/home-public')
    time.sleep(1)
    for x in range(100):
        try:
            ModalValidacion = driver.find_element(By.CSS_SELECTOR,'div#whcModal')
            resultModal = ModalValidacion.text
            print(resultModal)
            if resultModal != "":
                time.sleep(1)
            else:
                time.sleep(1)
                break
        except:
            time.sleep(3)
            break

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtBusqueda"]')))\
        .send_keys(Placa[i])
        #TOK39E AVZ999
    time.sleep(1)
    print(i)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button#consultar')))\
        .click()
    time.sleep(3)

    try:
        tabla = driver.find_element(By.XPATH,'//*[@id="multaTable"]')
        tablaRes = tabla.text
        cadena = (tablaRes).split()
        print("Datos "+str(cadena))

        Tipo =  driver.find_element(By.XPATH,'//*[@id="multaTable"]/tbody/tr/td[1]').text
        Notificacion = driver.find_element(By.XPATH,'//*[@id="multaTable"]/tbody/tr/td[2]').text
        Placa = driver.find_element(By.XPATH,'//*[@id="multaTable"]/tbody/tr/td[3]').text
        Secretaria = driver.find_element(By.XPATH,'//*[@id="multaTable"]/tbody/tr/td[4]').text
        infranccion =  driver.find_element(By.XPATH,'//*[@id="multaTable"]/tbody/tr/td[5]').text
        Estado = driver.find_element(By.XPATH,'//*[@id="multaTable"]/tbody/tr/td[6]').text
        Valor = driver.find_element(By.XPATH,'//*[@id="multaTable"]/tbody/tr/td[7]').text

        result = Tipo+" "+Notificacion+" "+Placa+" "+Secretaria+" "+infranccion+" "+Estado+" "+Valor
        print(result)
        filanew = [Nombre[i],Apellido[i],Placa[i],result]
        dataSIMIT.loc[i] =filanew
        screenshot_name = "Documentos/"+"SIMIT_"+str(i)+".png"
        driver.save_screenshot(screenshot_name)
    except:
        resultado = driver.find_element(By.XPATH,'//*[@id="mainView"]/div/div[1]')
        result = resultado.text
        print(result)
        filanew = [Nombre[i],Apellido[i],Placa[i],result]
        dataSIMIT.loc[i] =filanew
        screenshot_name = "Documentos/"+"SIMIT_"+str(i)+".png"
        driver.save_screenshot(screenshot_name)
    driver.quit()

dataSIMIT.to_csv('Archivos/Antecedentes.csv', index=True)