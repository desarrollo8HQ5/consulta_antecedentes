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
dataLibretaMilitar = pd.DataFrame(columns=['Nombre', 'Apellido', 'Tipo_Documento','Documento','Libreta_Militar'])

#Importar datos
filename = "Datos/Datos Gestion Documental Corregidos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
nombres = archivo["nombres_y_apellidos"].iloc[0:5]

#Datos de consulta
Apellido = []
Nombre =  []
Valdiar_Tipo = []
Tipo_Documento = []
Documento = []
    
#Tratamiento de datos del dataframe
nombres= nombres.str.split(' ', expand=True)
nombres['nombres completos'] = nombres[0].str.cat(nombres[1],sep=' ')
nombres['apellidos completos'] = nombres[2].str.cat(nombres[3],sep=' ')

for i in nombres.index:
        
    Nombre.append(nombres["nombres completos"][i])
    Apellido.append(nombres["apellidos completos"][i])
    Valdiar_Tipo.append(archivo["tipo_de_documento"][i])
    Documento.append(archivo["documento"][i])

    if 'CEDULA DE CIUDADANIA' == str(Valdiar_Tipo[i]):
        Tipo_Documento.append("Cédula de Ciudadanía") 
    else:
        Tipo_Documento.append("NUIP") 

    # Opciones de navegación
    options =  webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    driver_path = 'C:\\Users\\CO-225\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'
    #driver_path = 'C:\\Users\\crahi\\appdata\\local\\programs\\python\\Python310\\Lib\\site-packages\\chromedriver.exe'

    chromeOptions = webdriver.ChromeOptions()

    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")cleart
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])

    directorio = "C:\\Users\\CO-225\\Documents\\ciencia de datos\\Reto\\Documentos\\Libreta"
    #directorio = "D:\\Documentos\\HQ5\\ciencia de datos\\Reto\\Documentos\\Libreta"
    prefs = {"profile.default_content_settings.popups": 0,    
            "download.default_directory":directorio, ##Set the path accordingly
            "download.prompt_for_download": False, #change the downpath accordingly
            "download.directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(driver_path, chrome_options=options)
    # Iniciarla en la pantalla 2
    driver.set_window_position(200, 0)
    driver.maximize_window()
    time.sleep(1)

    #Inicializamos el navegador
    driver.get('https://www.libretamilitar.mil.co/')
    time.sleep(2)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ctl00_lblMenuConsults')))\
        .click()
    time.sleep(1)


    mouse_mov = driver.find_element(By.ID,'ctl00_lblMenuConsults')
    mouse_mov2 = driver.find_element(By.ID,'ctl00_lblMenuMilitarySituation')
    movimiento = ActionChains(driver)
    movimiento.move_to_element(mouse_mov).move_to_element(mouse_mov2).click().perform()

    driver.switch_to.window(driver.current_window_handle)
    print(driver.title)

    selec = driver.find_element(By.ID,"ctl00_MainContent_drpDocumentType")
    selec.get_attribute("value")
    print(selec.text)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ctl00_MainContent_drpDocumentType')))\
        .send_keys(str(Tipo_Documento[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ctl00_MainContent_txtNumberDocument')))\
        .send_keys(str(Documento[i]))
    time.sleep(1)
        
    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID,'ctl00_MainContent_btnConsult')))\
        .click()
    time.sleep(1)

    Resultado = driver.find_element(By.XPATH,'//*[@id="divErrorMessages"]')
    Result = str(Resultado.text)


    if Result != "":

        filanew = [Nombre[i],Apellido[i],Tipo_Documento[i],Documento[i],Result]
        dataLibretaMilitar.loc[i] =filanew

        driver.quit()

    else:

        Informacion = driver.find_element(By.XPATH,'//*[@id="aspnetForm"]/div[9]/div[6]/div[2]')
        presentar = Informacion.text
        
        Estado = []

        Estado_1 = driver.find_element(By.XPATH,'//*[@id="divHead"]')
        presentar_1 = str(Estado_1.get_attribute("style"))
        presentar_1_1 = str(Estado_1.get_attribute("id"))
        Estado.append(presentar_1+"-"+presentar_1_1)

        Estado_2 = driver.find_element(By.XPATH,'//*[@id="divCited"]')
        presentar_2 = str(Estado_2.get_attribute("style"))
        presentar_2_1 = str(Estado_2.get_attribute("id"))
        Estado.append(presentar_2+"-"+presentar_2_1)

        Estado_3 = driver.find_element(By.XPATH,'//*[@id="divSuitable"]')
        presentar_3 = str(Estado_3.get_attribute("style"))
        presentar_3_1 = str(Estado_3.get_attribute("id"))
        Estado.append(presentar_3+"-"+presentar_3_1)

        Estado_4 = driver.find_element(By.XPATH,'//*[@id="divLiquidation"]')
        presentar_4 = str(Estado_4.get_attribute("style"))
        presentar_4_1 = str(Estado_4.get_attribute("id"))
        Estado.append(presentar_4+"-"+presentar_4_1)

        Estado_5 = driver.find_element(By.XPATH,'//*[@id="divDefined"]')
        presentar_5 = str(Estado_5.get_attribute("style"))
        presentar_5_1 = str(Estado_5.get_attribute("id"))
        Estado.append(presentar_5+"-"+presentar_5_1)
        
        #Validar en cual de los estados se encuentra
        for y in range(len(Estado)):
            if 'none' in str(Estado[y]) :
                print("Found")
            else:
                #Definir el estado
                if 'divHead' in str(Estado[y]): 
                    Estado_Consulta = 'Inscripción'
                    div = "1"
                elif 'divCited' in str(Estado[y]):
                    Estado_Consulta = 'Inscripción'
                    div = "2"
                elif 'divSuitable' in str(Estado[y]):
                    Estado_Consulta = 'Citado'
                    div = "3"
                elif 'divLiquidation' in str(Estado[y]):
                    Estado_Consulta = 'En Liquidación'
                    div = "4"
                elif 'divDefined' in str(Estado[y]):
                    Estado_Consulta = 'Reservista'
                    div = "5"
        #Ver informacion
        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="Div'+div+'"]/div/div[3]/div/div[1]/img')))\
            .click()
        time.sleep(1)
        # Descargar certificado
        if Estado_Consulta == 'Reservista':
            Barra_info = driver.find_element(By.XPATH,'//*[@id="Div'+div+'"]/div/div[3]/div/p')
            WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_MainContent_lblTextDefined"]/a')))\
                .click()
            time.sleep(1)
            WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#ctl00_MainContent_imgBtnSeeCertificate')))\
                .click()
            time.sleep(1)

            dir = 'Documentos/Libreta/'
            old_file = os.path.join(dir, 'CertificadoLibretaMilitar.pdf')
            new_file = os.path.join(dir, 'CertificadoLibretaMilitar'+str(Documento[i])+'.pdf')
            os.rename(old_file, new_file)
            print("\n")

            cadena = (presentar).split()
            Estado = " ".join(cadena[6:])
            Resultado = Estado +"\n"+ str(Barra_info.text)
            print(Resultado)

            filanew = [Nombre[i],Apellido[i],Tipo_Documento[i],Documento[i],Resultado]
            dataLibretaMilitar.loc[i] =filanew

            driver.quit()
            
        else:
            Barra_info = driver.find_element(By.XPATH,'//*[@id="Div'+div+'"]/div/div[3]/div/p')
            print("\n")

            cadena = (presentar).split()
            Estado = " ".join(cadena[6:])
            Resultado = Estado +"\n"+ str(Barra_info.text)
            print(Resultado)

            filanew = [Nombre[i],Apellido[i],Tipo_Documento[i],Documento[i],Resultado]
            dataLibretaMilitar.loc[i] =filanew

            driver.quit()
        
    dataLibretaMilitar.to_csv('Archivos/Antecedentes.csv', index=True)




