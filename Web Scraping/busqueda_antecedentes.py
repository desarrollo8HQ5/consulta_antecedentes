# Librerías para webscraping
# Librerías complmentarias
import json
import os
import time
import glob
import win32com.client
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader

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
# filename = "Datos/Con Hallazgos.csv"
# fullpath = os.path.join(filename)
archivo = pd.read_csv("C:/Users/CO-182/Documents/GitHub/consulta_antecedentes/Datos/Con Hallazgos.csv")
#Numero de registros a buscar   
datos = archivo.iloc[0:1]

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
# PDFs
documentos=[]
# Consultas
interpol = []
ofac = []
sisben=[]
simit=[]
onu=[]
desmovilizados=[]
rama_unificada=[]
europol=[]
medidas_correctivas=[]
procuraduria=[]
personeria=[]
pep=[]
cpp=[]
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver_path = 'C:\\Users\\CO-182\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\chromedriver.exe'

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

directorio = "C:\\Users\\CO-182\\Documents\\GitHub\\consulta_antecedentes\\Consultas"

prefs = {
    "printing.print_preview_sticky_settings.appState": json.dumps(appState),
    'savefile.default_directory':directorio,
    "download.default_directory":directorio
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
    #Inicio de la navegación
    try:
        driver.get('https://www.interpol.int/es/Como-trabajamos/Notificaciones/Ver-las-notificaciones-rojas')

        time.sleep(1)
        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#name')))\
            .send_keys(str(Apellidos[i]))
        time.sleep(1)

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#forename')))\
            .send_keys(str(Nombres[i]))
        time.sleep(1)

        WebDriverWait(driver, 1)\
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
            var_INTERPOL='SIN RESULTADO'
        else:
            WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.redNoticeItem__labelLink')))\
            .click()
            time.sleep(1)
            var_INTERPOL='CON HALLAZGO'
            # Guardar consulta como PDF    
        driver.execute_script('window.print();')
        time.sleep(1)
        os.replace("Consultas\\Ver las notificaciones rojas.PDF", "Consultas\\INTERPOL_"+str(Documento[i])+".PDF")
        interpol.append(str(var_INTERPOL))
        documentos.append('INTERPOL_'+str(Documento[i])+'.PDF')
    except:
        driver.execute_script('window.print();')
        time.sleep(1)
        interpol.append('FUENTE NO DISPONIBLE')
    #OFAC
    # Inicio de la anvegación
    try:
        driver.get('https://sanctionssearch.ofac.treas.gov/')

        time.sleep(1)

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_MainContent_txtID"]')))\
            .send_keys(str(Documento[i]))

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_MainContent_ddlCountry"]')))\
            .send_keys("Colombia")

        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_MainContent_btnSearch"]')))\
            .click()

        time.sleep(1)
        var_OFAC = driver.find_element(By.XPATH,'//*[@id="scrollResults"]').text
        if(var_OFAC.__contains__('has not returned')):
            var_OFAC='SIN RESULTADOS'
        else:
            var_OFAC='CON HALLAZGO'
            #Ir al detalle del hallazgo
            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="gvSearchResults"]/tbody/tr/td[1]/a')))\
                .click()
            time.sleep(1)

        # Guardar y renombrar consulta como PDF
        driver.execute_script('window.print();') 
        time.sleep(1)
        os.replace("Consultas\\Sanctions List Search.PDF", "Consultas\\OFAC_"+str(Documento[i])+".PDF")  
        ofac.append(str(var_OFAC))
        documentos.append('OFAC_'+str(Documento[i])+'.PDF')
    except:
        driver.execute_script('window.print();') 
        time.sleep(1)
        ofac.append('FUENTE NO DISPONIBLE')
    
    #Sisben
    # Cambio de página web

    try:
        driver.get('https://portal.sisben.gov.co/Paginas/consulta-tu-grupo.html')
        time.sleep(1)
        #Select iFrame
        element = driver.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_ctl01__ControlWrapper_RichHtmlField"]/section/div/div[1]/div[12]/div/div/iframe')

        #Switch to iFrame
        driver.switch_to.frame(element)

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.ID,'TipoID')))\
            .send_keys(str(Tipo_Documento[i]))
        time.sleep(1)

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.ID,'documento')))\
            .send_keys(str(Documento[i]))
        time.sleep(1)

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.ID,'botonenvio')))\
            .click()
        time.sleep(10)

        Result_pagina = driver.find_element(By.XPATH,'/html/body')
        Resultado_Pagina = Result_pagina.get_attribute('innerHTML')

        if 'swal2-title' in Resultado_Pagina:
            sisben.append('SIN RESULTADO')
        else:
            sisben.append('CON HALLAZGO')
        time.sleep(1)
        driver.execute_script('window.print();')    
        time.sleep(1)
        os.replace("Consultas\\Consulta tu Grupo Sisbén.PDF", "Consultas\\SISBEN_"+str(Documento[i])+".PDF")
        documentos.append('SISBEN_'+str(Documento[i])+'.PDF')
    except:
        sisben.append('FUENTE NO DISPONIBLE')
   #SIMIT
   #Inicio de la navegación
    try:
        driver.get('https://fcm.org.co/simit/#/home-public')
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 200)") 
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, -200)") 
        time.sleep(1)
        driver.execute_script("location.reload()")
        time.sleep(10)
        for x in range(100):
            try:
                ModalValidacion = driver.find_element(By.XPATH,'//*[@id="txtBusqueda"]')
                resultModal = ModalValidacion.text
                respuesta='1'
                if resultModal != "":
                    time.sleep(3)
                else:
                    break
            except:
                respuesta='0'
                driver.execute_script("location.reload()")  
                time.sleep(5)    
        if(respuesta=='1'):
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
                resultado = 'CON HALLAZGO'
            except:
                resultado = 'SIN RESULTADO'
        else:
            resultado='FUENTE NO DISPONIBLE'
        #Evidencia de la consulta
        driver.execute_script('window.print();')    
        time.sleep(1)
        os.replace("Consultas\\SIMIT _ Estado de la Cuenta.PDF", "Consultas\\SIMIT_"+str(Documento[i])+".PDF")
        simit.append(resultado)
        documentos.append('SIMIT_'+str(Documento[i])+'.PDF')
    except:
        simit.append('FUENTE NO DISPONIBLE')
    #ONU
    #Inicio de la navegación
    try:
        driver.get('https://scsanctions.un.org/search/')
        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#include')))\
            .send_keys(Nombres[i])

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.XPATH,'/html/body/center/form/table/tbody/tr[1]/td[7]/input')))\
            .click()

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="adv"]/u')))\
            .click()
        ##dia
        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'select#daydropdown')))\
            .send_keys(day)
        ##mes
        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'select#monthdropdown')))\
            .send_keys(month)
        ##año
        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'select#yeardropdown')))\
            .send_keys(year)

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'select#nation')))\
            .send_keys(Nacionalidad)

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.XPATH,'/html/body/center/form/table/tbody/tr[26]/td[3]/input')))\
            .click()
        try:
            resultado = driver.find_element(By.CSS_SELECTOR,'tr.rowtext')
            result = 'CON HALLAZGO'
        except:
            result = "SIN RESULTADO"
        onu.append(result)
    except:
        onu.append('FUENTE NO DISPONIBLE')
    #Evidencia de la consulta
    driver.execute_script('document.title="ONU"')    
    driver.execute_script('window.print();')
    os.replace("Consultas\\ONU.PDF", "Consultas\\ONU_"+str(Documento[i])+".PDF")
    documentos.append('ONU_'+str(Documento[i])+'.PDF')
    #Desmovilzados
    # Inicializamos el navegador
    try:
        driver.get('https://www.fiscalia.gov.co/colombia/justicia-transicional-2/consulta-postulados/')
        driver.execute_script("window.scrollBy(0,600)")
        time.sleep(1)
        #Select iFrame
        element = driver.find_element(By.CLASS_NAME,'iframe-class')

        #Switch to iFrame
        driver.switch_to.frame(element)

        #Query document for the ID that you're looking for
        queryElement = driver.find_element(By.CLASS_NAME,'MuiInputBase-input')
        WebDriverWait(driver, 1)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input.MuiInputBase-input')))\
            .send_keys(Nombres[i]+" "+Apellidos [i])
        WebDriverWait(driver, 1)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input.MuiInputBase-input')))\
            .send_keys(Keys.ENTER)
        time.sleep(3)
        Respuesta = driver.find_element(By.CSS_SELECTOR,'div.MuiGrid-root.MuiGrid-container')
        result = Respuesta.text
        if(result.__contains__(str(Documento[i]))):
            desmovilizados.append('CON HALLAZGO')
        else:
            desmovilizados.append('SIN RESULTADO')
        driver.execute_script('document.title="Consulta postulados _ Fiscalía General de la Nación"')   
        driver.execute_script('window.print();')
        time.sleep(1)
        os.replace("Consultas\\Consulta postulados _ Fiscalía General de la Nación.PDF", "Consultas\\DESMOVILIZADOS_"+str(Documento[i])+".PDF")
    except:
        desmovilizados.append('FUENTE NO DISPONIBLE')  
        driver.execute_script('window.print();')
        time.sleep(1)
        try:
            os.replace("Consultas\\www.fiscalia.gov.co.PDF", "Consultas\\DESMOVILIZADOS_"+str(Documento[i])+".PDF")
        except:
            os.replace("Consultas\\Consulta postulados _ Fiscalía General de la Nación.PDF", "Consultas\\DESMOVILIZADOS_"+str(Documento[i])+".PDF")
        documentos.append('DESMOVILIZADOS_'+str(Documento[i])+'.PDF')
    
    #Rama unificada
    #Inicio de la navegación 
    try:
        driver.get('https://consultaprocesos.ramajudicial.gov.co/Procesos/NombreRazonSocial')
        time.sleep(1)
        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="mainContent"]/div/div/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[2]/div/div')))\
            .click()
        time.sleep(1)

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.ID,'input-72')))\
            .send_keys("Natural")
        time.sleep(1)

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.ID,'input-78')))\
            .send_keys(str(Nombres[i])+' '+str(Apellidos[i]))
        time.sleep(1)

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="mainContent"]/div/div/div/div[1]/div/div[2]/div/div[5]/button[1]/span')))\
            .click()
        time.sleep(3)    
        try:
            pop_up = driver.find_element(By.CSS_SELECTOR,'p.pl-1').text
            if(pop_up.__contains__('Hay más de mil registros') or  pop_up.__contains__('La consulta no generó resultados')):
                driver.execute_script('window.print();')
                time.sleep(1)
                os.replace("Consultas\\Consulta de Procesos por Nombre o Razón Social- Consejo Superior de la Judicatura.PDF", "Consultas\\RAMA_UNIFICADA_"+str(Documento[i])+".PDF")            
                rama_unificada.append('SIN RESULTADO')
        except:
            pop_up='unico resultado'
        if(pop_up.__contains__('Se han encontrado varios registros') or pop_up.__contains__('unico resultado') ):
            if(pop_up.__contains__('Se han encontrado varios registros')):
                WebDriverWait(driver, 1)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[3]/div/div/div[2]/div/button')))\
                    .click()
            WebDriverWait(driver,1)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/button/span')))\
                .click()
            time.sleep(1)
            files_path = os.path.join(directorio, '*')
            files = sorted(
                glob.iglob(files_path), key=os.path.getctime, reverse=True) 
            wdFormatPDF = 17
            outputFile = os.path.join(directorio,"RAMA_UNIFICADA_"+str(Documento[i])+".PDF")
            word = win32com.client.Dispatch('Word.Application')
            doc = word.Documents.Open(files[0])
            doc.SaveAs(outputFile, FileFormat=wdFormatPDF)
            doc.Close()
            word.Quit()
            time.sleep(1)
            os.remove(files[0])
            rama_unificada.append('CON HALLAZGO')
    except:
        rama_unificada.append('FUENTE NO DISPONIBLE')
        driver.execute_script('window.print();')
        time.sleep(1)
        os.replace("Consultas\\Consulta de Procesos por Nombre o Razón Social- Consejo Superior de la Judicatura.PDF", "Consultas\\RAMA_UNIFICADA_"+str(Documento[i])+".PDF")
    documentos.append('RAMA_UNIFICADA_'+str(Documento[i])+'.PDF')

    #Europol
    #Inicio de la navegación 
    try:
        driver.get('https://eumostwanted.eu/es')
        time.sleep(1)
        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#edit-search-block-form--2')))\
            .send_keys(Primer_Apellido[i]+", "+Primer_Nombre[i])
# Primer_Apellido[i]+", "+
        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button#edit-submit.secondary button radius postfix expand form-submit'.replace(' ', '.'))))\
            .click()
            
        time.sleep(1)
        result = driver.find_element(By.ID,'#searchResults').text
        filas = driver.find_elements(By.CSS_SELECTOR,'li.search-result')
        if(result.__contains__('SU BÚSQUEDA NO PRODUJO RESULTADOS')):
            file_path = os.path.join(directorio, 'EUROPOL_.png')
            driver.execute_script("window.scrollTo(0, 500)") 
            driver.save_screenshot(file_path)
            image_1 = Image.open(file_path)
            im_1 = image_1.convert('RGB')
            im_1.save(r'C:\\Users\\CO-182\\Documents\\GitHub\\consulta_antecedentes\\Consultas\\EUROPOL_'+str(Documento[i])+r'.PDF')
            os.remove(file_path)
            europol.append('SIN RESULTADO')
        else:            
            for r in range(1,len(filas)+1): 
                resultado = driver.find_element(By.XPATH,'//*[@id="#searchResults"]/ol/li['+str(r)+']/h3/a').text.split(sep='...')[0].upper()
                if(resultado.__contains__(Primer_Apellido[i]+", "+Primer_Nombre[i])):
                    driver.execute_script("window.scrollTo(0, 500)") 
                    time.sleep(1)
                    WebDriverWait(driver, 5)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="#searchResults"]/ol/li['+str(r)+']/h3/a')))\
                        .click()
                    time.sleep(1)
                    driver.execute_script('window.print();')
                    time.sleep(1)
                    os.replace("Consultas\\Europe's most wanted _.PDF", "Consultas\\EUROPOL_"+str(Documento[i])+".PDF")
                    break
            europol.append('CON HALLAZGO')
    except:
        europol.append('FUENTE NO DISPONIBLE')
        file_path = os.path.join(directorio, 'EUROPOL_.png')
        driver.execute_script("window.scrollTo(0, 500)") 
        driver.save_screenshot(file_path)
        image_1 = Image.open(file_path)
        im_1 = image_1.convert('RGB')
        im_1.save(r'C:\\Users\\CO-182\\Documents\\GitHub\\consulta_antecedentes\\Consultas\\EUROPOL_'+str(Documento[i])+r'.PDF')
        os.remove(file_path)
    documentos.append('EUROPOL_'+str(Documento[i])+'.PDF')

    #Medidas correctivas
    #Inicio de la navegación 
    try:
        driver.get('https://srvcnpc.policia.gov.co/PSC/frm_cnp_consulta.aspx')
        time.sleep(1)
        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.ID,'ctl00_ContentPlaceHolder3_ddlTipoDoc')))\
            .send_keys(str(Tipo_Documento[i]))
        time.sleep(1)

        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.ID,'ctl00_ContentPlaceHolder3_txtExpediente')))\
            .send_keys(str(Documento[i]))
        time.sleep(1)

        if  str(Tipo_Documento[i]) in ('CEDULA DE CIUDADANIA'):
            WebDriverWait(driver, 1)\
                .until(EC.element_to_be_clickable((By.ID,'txtFechaexp')))\
                .send_keys(str(Fecha_Expedicion[i]))
            time.sleep(1)
            boton_busqueda = '//*[@id="ctl00_ContentPlaceHolder3_btnConsultar2"]'
        else:
            boton_busqueda =  '//*[@id="ctl00_ContentPlaceHolder3_btnConsultar"]'


        WebDriverWait(driver, 1)\
            .until(EC.element_to_be_clickable((By.XPATH,boton_busqueda)))\
            .click()
        time.sleep(1)

        result = driver.find_element(By.XPATH,'//*[@id="flotante"]').text

        if(result.__contains__('NO TIENE MEDIDAS CORRECTIVAS PENDIENTES POR CUMPLIR')):
            driver.execute_script('document.title="MEDIDAS_CORRECTIVAS_"')
            WebDriverWait(driver,1)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder3_btnImprimir2"]')))\
                .click()
            medidas_correctivas.append('SIN RESULTADO')
        else:  
            WebDriverWait(driver,1)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder3_gv_expedientes"]/tbody/tr[2]/td[1]/a')))\
                .click()
            time.sleep(1)
            driver.execute_script('document.title="MEDIDAS_CORRECTIVAS_"')
            driver.execute_script('window.print();')
            medidas_correctivas.append('CON HALLAZGO') 

    except:
        driver.execute_script('document.title="MEDIDAS_CORRECTIVAS_"')
        medidas_correctivas.append('FUENTE NO DISPONIBLE')
        driver.execute_script('window.print();')

    time.sleep(1)
    try:
        os.replace("Consultas\\MEDIDAS_CORRECTIVAS_.PDF", "Consultas\\MEDIDAS_CORRECTIVAS_"+str(Documento[i])+".PDF")
        documentos.append('MEDIDAS_CORRECTIVAS_'+str(Documento[i])+'.PDF')
    except:
        continue
    #Antecedentes procuraduría
    try:
        # Inicio de la navegación 
        driver.get('https://www.procuraduria.gov.co/Pages/Consulta-de-Antecedentes.aspx')
        time.sleep(0.5)
        # Cambiar al iframe
        element = driver.find_element(By.CLASS_NAME,'embed-responsive-item')
        driver.switch_to.frame(element)
        validador=0
        for x in range(10):
            #Obtener la pregunta de seguridad y validar respuestas que se tengan
            time.sleep(3)        
            pregunta=driver.find_element(By.XPATH,'//*[@id="lblPregunta"]').text
            if(pregunta.__contains__('Cuanto es 9 - 2')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('7')
                validador=1
                break
            elif(pregunta.__contains__('dos primeras letras del primer nombre')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys(str(Primer_Nombre[i])[:2])
                validador=1
                break
            elif(pregunta.__contains__('dos ultimos digitos del documento')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys(str(Documento[i])[len(str(Documento[i]))-2:len(str(Documento[i]))])
                validador=1
                break
            elif(pregunta.__contains__('cantidad de letras del primer nombre')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys(len(str(Primer_Nombre[i])))
                validador=1
                break
            elif(pregunta.__contains__('tres primeros digitos del documento a consultar')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys(str(Documento[i])[:3])
                validador=1
                break
            elif(pregunta.__contains__('Capital del Atlantico')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('barranquilla')
                validador=1
                break
            elif(pregunta.__contains__('Capital de Antioquia')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('medellin')
                validador=1
                break
            elif(pregunta.__contains__('6 + 2')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('8')
                validador=1
                break
            elif(pregunta.__contains__('3 - 2')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('1')
                validador=1
                break
            elif(pregunta.__contains__('2 X 3')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('6')
                validador=1
                break
            elif(pregunta.__contains__('Capital de Colombia')):
                WebDriverWait(driver,2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txtRespuestaPregunta"]')))\
                    .send_keys('bogota')
                validador=1
                break
            else:
                driver.execute_script("location.reload()")
        if(validador==1):
            WebDriverWait(driver, 1)\
                .until(EC.element_to_be_clickable((By.ID,'ddlTipoID')))\
                .send_keys(str(Tipo_Documento[i]))
            time.sleep(1)
            WebDriverWait(driver, 1)\
                .until(EC.element_to_be_clickable((By.ID,'txtNumID')))\
                .send_keys(str(Documento[i]))
            time.sleep(1)  
            WebDriverWait(driver, 1)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="btnConsultar"]')))\
                .click()
            time.sleep(10)   
            for x in range(20):
                try:
                    resultado=driver.find_element(By.XPATH,'//*[@id="divSec"]/h2[2]').text
                    if(resultado.__contains__('El ciudadano no presenta antecedentes')):
                        procuraduria.append('SIN RESULTADOS')
                        break
                    else:
                        procuraduria.append('CON HALLAZGO') 
                        break
                except:
                    time.sleep(2)           
        else:
            procuraduria.append('FUENTE NO DISPONIBLE')
    except:
            procuraduria.append('FUENTE NO DISPONIBLE')

    driver.execute_script('window.print();')  
    time.sleep(1)  
    try:
        os.replace("Consultas\\Consulta de Antecedentes.PDF", "Consultas\\PROCURADURIA_"+str(Documento[i])+".PDF") 
    except:
        try:
            os.replace("Consultas\\www.procuraduria.gov.co.PDF", "Consultas\\PROCURADURIA_"+str(Documento[i])+".PDF")
        except:
            continue
    documentos.append('PROCURADURIA_'+str(Documento[i])+'.PDF')


    #Antecedentes personeria
    try:
        # Inicio de la navegación  
        driver.get('https://www.personeriabogota.gov.co/al-servicio-de-la-ciudad/expedicion-de-antecedentes')
        driver.execute_script("window.scrollTo(0,700)")
        time.sleep(2)
        element = driver.find_element(By.ID,'ir-formulario')
        driver.switch_to.frame(element)
        WebDriverWait(driver,1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/p/div[1]/button')))\
            .click()
        time.sleep(1)
        WebDriverWait(driver,1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="collapseAntecedete"]/div/form/div[1]/div[1]/select')))\
            .send_keys(str(Tipo_Documento[i]))
        time.sleep(1)
        WebDriverWait(driver,1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="numDoc"]')))\
            .send_keys(str(Documento[i]))    
        time.sleep(2)
        if(str(Tipo_Documento[i]).__contains__('CEDULA DE CIUDADANIA')):
            for x in range(20):
                pregunta = driver.find_element(By.XPATH,'//*[@id="collapseAntecedete"]/div/form/div[2]/div[2]/div/label').text
                if(pregunta.__contains__('7 * 1')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('7')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 2')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('14')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 3')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('21')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 4')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('28')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 5')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('35')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 6')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('42')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 7')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('49')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 8')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('56')
                    time.sleep(1)
                    break
                elif(pregunta.__contains__('7 * 9')):
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pregunta"]')))\
                        .send_keys('63')
                    time.sleep(1)
                    break
                else:
                    driver.switch_to.default_content()
                    driver.execute_script("location.reload()")
                    time.sleep(2)
                    element = driver.find_element(By.ID,'ir-formulario')
                    driver.switch_to.frame(element)
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/p/div[1]/button')))\
                        .click()
                    time.sleep(1)
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="collapseAntecedete"]/div/form/div[1]/div[1]/select')))\
                        .send_keys(str(Tipo_Documento[i]))
                    time.sleep(1)
                    WebDriverWait(driver,1)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="numDoc"]')))\
                        .send_keys(str(Documento[i]))    
                    time.sleep(2)
        WebDriverWait(driver,1)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="collapseAntecedete"]/div/form/button')))\
            .click()
        time.sleep(1)
        for x in range(20):
            try:
                WebDriverWait(driver,1)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div[2]/form/div[2]/div/a')))\
                .click()
                break
            except:
                time.sleep(2)
        time.sleep(1)
        personeria.append('CONSULTADO')
        try:
            os.replace("Consultas\\antecedente_disciplinario.PDF","Consultas\\PERSONERIA_"+str(Documento[i])+".PDF")
            documentos.append('PERSONERIA_'+str(Documento[i])+'.PDF')
        except:
            continue
    except:    
        personeria.append('FUENTE NO DISPONIBLE')
    
    #PEPS
    try:
        #     # Inicio de la navegación  
        driver.get('https://www.funcionpublica.gov.co/fdci/consultaCiudadana/consultaPEP')
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)

        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.ID,'numeroDocumento')))\
            .send_keys(str(Documento[i]))
        time.sleep(1)

        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.ID,'primerNombre')))\
            .send_keys(str(Primer_Apellido[i]))
        time.sleep(1)

        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.ID,'segundoNombre')))\
            .send_keys(str(Segundo_Nombre[i]))
        time.sleep(1)

        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.ID,'primerApellido')))\
            .send_keys(str(Primer_Apellido[i]))
        time.sleep(1)

        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.ID,'segundoApellido')))\
            .send_keys(str(Sengundo_Apellido[i]))
        time.sleep(1)

        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.ID,'find')))\
            .click()
        time.sleep(1)
        result = driver.find_element(By.XPATH,'//*[@id="list-consultaCiudadana"]/div[3]').text
        if(result.__contains__('No se encuentran declaraciones publicadas')):
            resultado = 'SIN RESULTADOS'
        else:
            resultado = 'CON HALLAZGOS'
    except:
        resultado = 'fuente no disponible'
    # Capturando evidencia de consulta
    driver.execute_script('window.print();')  
    time.sleep(1) 
    try:
        os.replace("Consultas\\Consulta Ciudadana - Personas Expuestas Políticamente (PEP) - Aplicativo por la Integridad Pública.PDF", "Consultas\\PEP_"+str(Documento[i])+".PDF") 
        documentos.append('PEP_'+str(Documento[i])+'.PDF')
    except:
        continue
    pep.append(resultado)

    #CONSULTA PUBLICA DE PROFESIONALES - CPP
    try:
        if(str(Tipo_Documento[i]).__contains__('CEDULA DE CIUDADANIA') or str(Tipo_Documento[i]).__contains__('CEDULA DE EXTRANJERIA') ):
            #     # Inicio de la navegación  
            driver.get('https://sgr.jcc.gov.co:8181/apex/f?p=138:1:0:::::')
            if(str(Tipo_Documento[i]).__contains__('CEDULA DE CIUDADANIA')):
                t_doc='Cédula<'
            else:
                t_doc='CE'

            WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((By.ID,'P1_VALOR')))\
                .send_keys(str(Documento[i]))
            time.sleep(1)

            WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="P1_CONSULTAR"]')))\
                .click()
            time.sleep(1)
            result = driver.find_element(By.XPATH,'//*[@id="P1_MSG_ESTADO_CONTAINER"]/div').text
            if(result.__contains__('No se encontraron datos')):
                resultado='SIN RESULTADOS'
            else:
                resultado='CON HALLAZGOS'
        else:
            resultado='N/A'
    except:
        resultado = 'fuente no disponible'
    # Capturando evidencia de consulta
    time.sleep(2) 
    driver.execute_script('window.print();')  
    time.sleep(1) 
    try:
        os.replace("Consultas\\Consulta pública de profesionales.PDF", "Consultas\\CPP_"+str(Documento[i])+".PDF") 
        documentos.append('CPP_'+str(Documento[i])+'.PDF')
    except:
        continue
    cpp.append(resultado)

    # pdfs = [os.path.join(directorio,'INTERPOL_'+str(Documento[i])+'.PDF'),os.path.join(directorio,'OFAC_'+str(Documento[i])+'.PDF'),os.path.join(directorio,'SISBEN_'+str(Documento[i])+'.PDF'),os.path.join(directorio,'SIMIT_'+str(Documento[i])+'.PDF'),os.path.join(directorio,'ONU_'+str(Documento[i])+'.PDF'),os.path.join(directorio,'DESMOVILIZADOS_'+str(Documento[i])+'.PDF'),os.path.join(directorio,'RAMA_UNIFICADA_'+str(Documento[i])+'.PDF'),os.path.join(directorio,'EUROPOL_'+str(Documento[i])+'.PDF'),os.path.join(directorio,'MEDIDAS_CORRECTIVAS_'+str(Documento[i])+'.PDF'),os.path.join(directorio,'PROCURADURIA_'+str(Documento[i])+'.PDF'),os.path.join(directorio,'PERSONERIA_'+str(Documento[i])+'.PDF')]
    
    # Generar un PDF
    merger = PdfFileMerger()
    for PDF in documentos:
        try:
            merger.append(os.path.join(directorio,PDF))
        except:
            continue
    # time.sleep(5)
    # os.remove(PDF)
    # doc=['PROCURADURIA_','RAMA_UNIFICADA_','SIMIT_','SISBEN_','INTERPOL_','DESMOVILIZADOS_','CPP_','INTERPOL_','PERSONERIA_','PEP_','EUROPOL_','OFA_','ONU_','MEDIDAS_CORRECTIVAS_','OFAC_']
    # for pdf in doc:
    #     try:
    #         os.close(os.path.join(directorio,pdf,str(Documento[i]),'.PDF'))
    #         time.sleep(1)
    #         os.remove('Consultas\\'+pdf+str(Documento[i])+'.PDF')
    #         print('Eliminado')
    #     except:
    #         print('no se pudo eliminar')
    #         continue
    # merger.write(os.path.join(directorio,'CONSULTA_'+str(Documento[i])+'.PDF'))


driver.quit()
print(len(interpol))
try:
    #Dataframe de almacenamiento
    data = pd.DataFrame({'PRIMER_NOMBRE':Primer_Nombre, 'SEGUNDO_NOMBRE':Segundo_Nombre, 'PRIMER_APELLIDO':Primer_Apellido,'SEGUNDO_APELLIDO':Sengundo_Apellido,
    'EDAD':Edad,'FECHA_EXPEDICION':Fecha_Expedicion,'TIPO_DE_DEOCUMENTO':Tipo_Documento,'DOCUMENTO':Documento,'DEPARTAMENTO':Departamento,'CIUDAD':Ciudad,
    'INTERPOL':interpol,'OFAC':ofac,'SISBEN':sisben,'SIMIT':simit,'ONU':onu,'DESMOVILIZADOS':desmovilizados,'RAMA_UNIFICADA':rama_unificada,'EUROPOL':europol,'MEDIDAS CORRECTIVAS':medidas_correctivas,'PROCURADURIA':procuraduria,'PERSONERIA':personeria,'PEP':pep,'CPP':cpp})
    # 'libreta_militar','garantias_mobiliarias'
    data.to_csv('Reporte/Antecedentes.csv', index=True)
    print('TERMINADO CORRECTAMENTE')
except:
    print('NO SE PUDO GENERAR EL ARCHIVO')
    print('INTERPOL',len(interpol))
    print('OFAC',len(ofac))
    print('SISBEN',len(sisben))
    print('SIMIT',len(simit))
    print('ONU',len(onu))
    print('DESMOVILIZADOS',len(desmovilizados))
    print('RAMA UNIFICADA',len(rama_unificada))
    print('EUROPOL',len(europol))
    print('MEDIDAS CORRECTIVAS',len(medidas_correctivas))
    print('PROCURADURIA',len(procuraduria))
    print('EPRSONERIA',len(personeria))
    print('PEP',len(pep))
    print('CPP',len(cpp))


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
