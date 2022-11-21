# Librerías para webscraping
# Librerías complmentarias
import json
import os
import time

import httplib2
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

#Variables Globales
#result = list()

#Dataframe de almacenamiento
# data = pd.DataFrame(columns=['primer_nombre', 'segundo_nombre', 'primer_apellido','segundo_apellido',
# 'edad','fecha_expedicion','tipo_de_documento','documento','departamento','ciudad',
# 'interpol','ofac','onu','proveedores_ficticios',
# 'concordato','desmovilizados','europol','rama_unificada',
# 'rama_judicial','simit','ruaf','secop_s',
# 'peps','rnmc','libreta_militar','contadores_sancionados',
# 'garantias_mobiliarias','secop','sisben'])

#Importar datos
filename = "Datos/Con Hallazgos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
#Numero de registros a buscar   
datos = archivo.iloc[0:4]

#Datos de consulta
Primer_Nombre =  []
Segundo_Nombre =  []
Primer_Apellido =  []
Sengundo_Apellido =  []
Nombres = []
Apellidos = []
Edad = []
Tipo_Documento = []
Fecha_Expedicion = []
Departamento = []
Ciudad = []
Documento = []
Nacionalidad = []
Fecha_Nacimiento=[]
interpol = []
ofac = []
sisben=[]
simit=[]
onu=[]
#Pruebas cristian
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver_path = 'C:\\Users\\CO-182\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'
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
directorio = "C:\\Users\\CO-182\\Desktop\\Reto 11-11-22\\Reto\\Documentos"

prefs = {
    "printing.print_preview_sticky_settings.appState": json.dumps(appState),
    'savefile.default_directory':directorio
}
options.add_experimental_option("prefs", prefs)
options.add_argument('--kiosk-printing')

driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)
time.sleep(1)
#Pruebas Cristian Fin

for i in datos.index:

    Primer_Nombre.append(archivo["primer_nombre"][i])
    Segundo_Nombre.append(archivo["segundo_nombre"][i])
    Primer_Apellido.append(archivo["primer_apellido"][i])
    Sengundo_Apellido.append(archivo["segundo_apellido"][i])
    if(str(Segundo_Nombre[i])=='nan'):
        Nombres.append(str(Primer_Nombre[i]))
    else:
        Nombres.append(str(Primer_Nombre[i])+" "+str(Segundo_Nombre[i]))
    Apellidos.append(str(Primer_Apellido[i])+" "+str(Sengundo_Apellido[i]))
    Edad.append(archivo["edad"][i])
    Tipo_Documento.append(archivo["tipo_de_documento"][i])
    Documento.append(archivo["documento"][i])
    Fecha_Expedicion.append(archivo["fecha_de_expedicion"][i])
    Ciudad.append(archivo["ciudad"][i])
    Departamento.append(archivo["departamento"][i])
    Nacionalidad.append(archivo["nacionalidad"][i])
    Fecha_Nacimiento.append(archivo["fecha_de_nacimiento"][i])
    Fecha_birth = Fecha_Nacimiento[i].split(sep='/')
    day = Fecha_birth[0]
    month = Fecha_birth[1]
    year = Fecha_birth[2]
    print(Apellidos)
    print(Nombres)

    #INTERPOL   
    # Iniciarla en la pantalla 
    # driver.set_window_position(200, 0)
    # driver.maximize_window()
    # time.sleep(1)

    #Inicio de la navegación
    driver.get('https://www.interpol.int/es/Como-trabajamos/Notificaciones/Ver-las-notificaciones-rojas')

    time.sleep(1)
    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#name')))\
        .send_keys(str(Apellidos[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#forename')))\
        .send_keys(str(Nombres[i]))
    time.sleep(1)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'select#nationality.generalForm__selectArea')))\
        .send_keys(str(Nacionalidad))
    time.sleep(1)
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#ageMin')))\
        .send_keys('0')
    time.sleep(1)
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#ageMax')))\
        .send_keys('100')
    time.sleep(1)
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="privacy-cookie-banner__privacy-close"]/i')))\
        .click()
    time.sleep(1)
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.btn.btn--black')))\
        .click()
    time.sleep(1)
    resultado_1 = driver.find_element(By.CSS_SELECTOR,'p#noSearchResults.redNoticesList__quantity')
    var_INTERPOL = resultado_1.text
    if(var_INTERPOL.__contains__('No hay resultados')):
        var_INTERPOL=var_INTERPOL.split('para')[0].upper()
        screenshot_name = "Documentos/"+"INTERPOL_"+str(Documento[i])+".png"
        driver.save_screenshot(screenshot_name)
    else:
        WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.redNoticeItem__labelLink')))\
        .click()
        time.sleep(1)
        # CargoInterpol= driver.find_element(By.CSS_SELECTOR,'p#charge').text.upper()
        # var_INTERPOL='PRESENTA HALLAZGOS EN LA INTERPOL POR '+ CargoInterpol
        var_INTERPOL='PRESENTA HALLAZGOS EN LA INTERPOL'
        # Guardar consulta como PDF 
        driver.execute_script('window.print();')
        time.sleep(1)
        os.replace("Documentos\\Ver las notificaciones rojas.pdf", "Documentos\\INTERPOL_"+str(Documento[i])+".pdf")
    interpol.append(str(var_INTERPOL))
    
    #OFAC
    # Cambio de página web
    driver.get('https://sanctionssearch.ofac.treas.gov/')

    time.sleep(1)

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
    var_OFAC = driver.find_element(By.XPATH,'//*[@id="scrollResults"]').text
    if(var_OFAC.__contains__('has not returned')):
        var_OFAC='NO HAY RESULTADOS'
    else:
        var_OFAC='PRESENTA HALLAZGOS EN LA LISTA CLINTON'
        #Ir al detalle del hallazgo
        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="gvSearchResults"]/tbody/tr/td[1]/a')))\
            .click()
        time.sleep(1)

    # Guardar y renombrar consulta como PDF 
    driver.execute_script('window.print();') 
    time.sleep(1)
    os.replace("Documentos\\Sanctions List Search.pdf", "Documentos\\OFAC_"+str(Documento[i])+".pdf")  
    ofac.append(str(var_OFAC)) 
    
    #Sisben
    # Cambio de página web

    driver.get('https://portal.sisben.gov.co/Paginas/consulta-tu-grupo.html')
    try:
        time.sleep(2)
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
        time.sleep(10)

        Result_pagina = driver.find_element(By.XPATH,'/html/body')
        Resultado_Pagina = Result_pagina.get_attribute('innerHTML')

        if 'swal2-title' in Resultado_Pagina:
            sisben.append('NO REGISTRADO')
        else:
            sisben.append('REGISTRADO')
        driver.execute_script('window.print();')    
        time.sleep(2)
        os.replace("Documentos\\Consulta tu Grupo Sisbén.pdf", "Documentos\\Sisben_"+str(Documento[i])+".pdf")
    except:
        sisben.append('FUENTE NO DISPONIBLE')
   #SIMIT
   #Inicio de la navegación
    driver.get('https://fcm.org.co/simit/#/home-public')
    try:
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 200)") 
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, -200)") 
        # driver.get('https://fcm.org.co/simit/#/home-public')
        driver.execute_script("location.reload()")
        time.sleep(20)
        for x in range(100):
            try:
                # ModalValidacion = driver.find_element(By.CSS_SELECTOR,'div#whcModal')
                ModalValidacion = driver.find_element(By.XPATH,'//*[@id="txtBusqueda"]')
                resultModal = ModalValidacion.text
                respuesta='1'
                if resultModal != "":
                    time.sleep(1)
                else:
                    break
            except:
                respuesta='0'
                driver.execute_script("location.reload()")  
                time.sleep(5)    
        if(respuesta=='1'):
            try:
                WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtBusqueda"]')))\
                .send_keys(str(Documento[i]))
                time.sleep(1)
                WebDriverWait(driver, 2)\
                    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button#consultar')))\
                    .click()
                time.sleep(3)
                try:
                    tabla = driver.find_element(By.XPATH,'//*[@id="multaTable"]')
                    resultado = 'CON MULTAS'
                except:
                    resultado = 'SIN MULTAS'
                #Evidencia de la consulta
                driver.execute_script('window.print();')    
                time.sleep(2)
                os.replace("Documentos\\SIMIT _ Estado de la Cuenta.pdf", "Documentos\\SIMIT_"+str(Documento[i])+".pdf")
            except:
                resultado='PENDIENTE CONSULTAR'
        else:
            resultado='PENDIENTE CONSULTAR'
        simit.append(resultado)
    except:
        simit.append('FUENTE NO DISPONIBLE')
    #ONU
    #Inicio de la navegación
    driver.get('https://scsanctions.un.org/search/')
    try:
        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#include')))\
            .send_keys(Nombres[i])

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
            result = 'TIENE RESULTADOS'
        except:
            result = "NO TIENE RESULTADOS"
        onu.append(result)
        #Evidencia de la consulta
        name_='ONU_'+str(Documento[i])+".pdf"
        driver.execute_script('document.title="ONU_'+str(Documento[i])+'"');    
        driver.execute_script('window.print();')    
        time.sleep(2)
        # os.replace("Documentos\\12ho4-en-all.pdf", "Documentos\\ONU_"+str(Documento[i])+".pdf")
    except:
        onu.append('FUENTE NO DISPONIBLE')

driver.quit()
#Dataframe de almacenamiento
data = pd.DataFrame({'primer_nombre':Primer_Nombre, 'segundo_nombre':Segundo_Nombre, 'primer_apellido':Primer_Apellido,'segundo_apellido':Sengundo_Apellido,
'edad':Edad,'fecha_expedicion':Fecha_Expedicion,'tipo_de_documento':Tipo_Documento,'documento':Documento,'departamento':Departamento,'ciudad':Ciudad,
'interpol':interpol,'ofac':ofac,'sisben':sisben,'simit':simit,'onu':onu})
#,'proveedores_ficticios',
# 'concordato','desmovilizados','europol','rama_unificada',
# 'rama_judicial','ruaf','secop_s',
# 'peps','rnmc','libreta_militar','contadores_sancionados',
# 'garantias_mobiliarias','secop'
data.to_csv('Archivos/Antecedentes.csv', index=True)



# EUROPOL


# OFAC
# ONU
# Proveedores ficticios
# Concordato (Supersociedades)
# Postulados (Desmovilizados)
# Europol
# Rama unificada
# SIMIT
# RUAF
# SECOP S
# PEPS
# Consulta de proceosos judiciales
# Rnmc (Medidas Correctivas)
# Libreta militar
# Contadores Sancionados
# Garantias mobiliarias
# SECOP
# Sisbén
