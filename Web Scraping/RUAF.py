# Librerías
from argparse import Action
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import pandas as pd
import os

#Variables Globales
#result = list()
dataRUAF = pd.DataFrame(columns=['Nombre', 'Apellido', 'Documento','Fecha_Expedicion','RUAF'])

#Importar datos
filename = "Datos/Datos Gestion Documental Corregidos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
nombres = archivo["nombres_y_apellidos"].iloc[0:5]
expediciones = archivo["fecha_de_expedicion"].iloc[0:5]

#Datos de consulta
Apellido = []
Nombre =  []
Day_Expedicion = []
Month_Expedicion = []
Year_Expedicion = []
Documento = []
    
#Tratamiento de datos del dataframe
nombres= nombres.str.split(' ', expand=True)
nombres['nombres completos'] = nombres[0].str.cat(nombres[1],sep=' ')
nombres['apellidos completos'] = nombres[2].str.cat(nombres[3],sep=' ')

Expedicion= expediciones.str.split('/', expand=True)
expediciones = Expedicion.rename(columns={0:'day_expedicion', 1:'month_expedicion', 2:'year_expedicion'})

try:

    for i in nombres.index:
            
        Nombre.append(nombres["nombres completos"][i])
        Apellido.append(nombres["apellidos completos"][i])
        Day_Expedicion.append(expediciones["day_expedicion"][i])
        Month_Expedicion.append(expediciones["month_expedicion"][i])
        Year_Expedicion.append(expediciones["year_expedicion"][i])
        Documento.append(archivo["documento"][i])


        # Opciones de navegación
        options =  webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        driver_path = 'C:\\Users\\CO-182\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\chromedriver.exe'
        #driver_path = 'C:\\Users\\crahi\\appdata\\local\\programs\\python\\Python310\\Lib\\site-packages\\chromedriver.exe'
        directorio = "C:\\Users\\CO-182\\Desktop\\Reto 11-11-22\\Reto\\Documentos"
        #directorio = "D:\\Documentos\\HQ5\\ciencia de datos\\Reto\\Documentos\\Libreta"
        prefs = {"profile.default_content_settings.popups": 0,    
        "download.default_directory":directorio, ##Set the path accordingly
        "download.prompt_for_download": False, #change the downpath accordingly
        "download.directory_upgrade": True}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(driver_path, chrome_options=options)

        # Iniciarla en la pantalla
        driver.set_window_position(200, 0)
        driver.maximize_window()
        time.sleep(1)

        #Inicializamos el navegador
        driver.get('https://www.sispro.gov.co/central-prestadores-de-servicios/Pages/RUAF-Registro-Unico-de-Afiliados.aspx')
        time.sleep(2)

        #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        driver.execute_script("window.scrollBy(0,800)")
        time.sleep(2)

        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="area-contenido"]/div/div[2]/div[2]/div/div[1]/div/div[2]/a/span')))\
            .click()

        while True:
            if str(driver.title) == 'Inicio - Consulta RUAF':
                break
            else:
                WebDriverWait(driver, 2)\
                    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="area-contenido"]/div/div[2]/div[2]/div/div[1]/div/div[2]/a/span')))\
                    .click()
                time.sleep(1)

        time.sleep(1)
        
        driver.switch_to.window(driver.current_window_handle)
        print(driver.title)

        
        time.sleep(3)

        mouse_mov = driver.find_element(By.XPATH,'//*[@id="menuSuperior"]/li[2]')
        mouse_mov2 = driver.find_element(By.XPATH,'//*[@id="menuSuperior"]/li[2]/ul')
        movimiento = ActionChains(driver)
        movimiento.move_to_element(mouse_mov).move_to_element(mouse_mov2).click().perform()

        time.sleep(2)

        driver.switch_to.window(driver.current_window_handle)
        print(driver.current_url)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        time.sleep(1)
        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#MainContent_RadioButtonList1_0')))\
            .click()
        time.sleep(1)

        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.NAME,'ctl00$MainContent$btnEnviar')))\
            .click()
        time.sleep(1)

        driver.switch_to.window(driver.current_window_handle)
        print(driver.current_url)
        time.sleep(1)

        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.ID,'MainContent_txbNumeroIdentificacion')))\
            .send_keys(str(Documento[i]))
        time.sleep(1)

        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.ID,'MainContent_datepicker')))\
            .send_keys(str(Day_Expedicion[i] + "/"+ Month_Expedicion[i] + "/"+ Year_Expedicion[i]))
        time.sleep(2)

        WebDriverWait(driver, 2)\
            .until(EC.element_to_be_clickable((By.ID,'MainContent_btnConsultar')))\
            .click()
        time.sleep(5)

        try:
            WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((By.ID,'ctl00_MainContent_rvConsulta_ctl09_ctl04_ctl00_ButtonImg')))\
                .click()
            time.sleep(1)

            WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_MainContent_rvConsulta_ctl09_ctl04_ctl00_Menu"]/div[1]/a')))\
                .click()
            time.sleep(5)
            os.rename("Documentos\\Ruaf\\Afiliaciones.pdf", "Documentos\\Ruaf\\Afiliaciones"+str(Documento[i])+"_"+str(i)+".pdf")
            time.sleep(5)
        except:
            continue


        Afiliaciones = driver.find_element(By.XPATH,'//*[@id="ctl00_MainContent_rvConsulta_fixedTable"]')
        print(Afiliaciones.text)

        if str(Afiliaciones.text) == "":
            driver.quit()
            break
        #Afiliacion_Pensiones = driver.find_element(By.XPATH,'//*[@id="Pbde850e7c5e44242949c3f51d321e05e_1_oReportCell"]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[17]/td[3]/table/tbody/tr[3]/td[1]')
        # Afiliacion_Riesgos_Lab = driver.find_element(By.XPATH,'//*[@id="Pbde850e7c5e44242949c3f51d321e05e_1_160iT2R0x0_aria"]/div')
        # Afiliacion_Compnesacion_Fam = driver.find_element(By.XPATH,'//*[@id="Pbde850e7c5e44242949c3f51d321e05e_1_160iT2R0x0_aria"]/div')
        # Afiliacion_Cesantias = driver.find_element(By.XPATH,'<div style="display: -ms-flexbox;display: -webkit-flex;display: flex;-ms-flex-align:start;-webkit-align-items:flex-start;align-items:flex-start;" class="A9bcd515b527d49578a6e1387c27130ea452_NR"><div style="width:252.56mm;min-width: 252.56mm;">No se han reportado afiliaciones para esta persona</div></div>')

        # Result = Afiliaciones.get_attribute("innerHTML")

        Datos_RUAF = str(Afiliaciones.text)
        cadena = (Datos_RUAF).split()
        cadena_Item_0 = cadena.index('BASICA')

        cadena_Item_1 = cadena.index('SALUD')
        Informacion_Basica = cadena[cadena_Item_0-1:cadena_Item_1-2]
        Informacion_Basica = " ".join(Informacion_Basica)

        cadena_Item_2 = cadena.index('PENSIONES')
        Afiliacion_Salud = cadena[cadena_Item_1-2:cadena_Item_2 -2]
        Afiliacion_Salud = " ".join(Afiliacion_Salud)

        cadena_Item_3 = cadena.index('LABORALES')
        Afiliacion_Pensiones = cadena[cadena_Item_2-2:cadena_Item_3 -3]
        Afiliacion_Pensiones = " ".join(Afiliacion_Pensiones)

        cadena_Item_4 = cadena.index('FAMILIAR')
        Afiliacion_Riesgos_Lab = cadena[cadena_Item_3-3:cadena_Item_4 -3]
        Afiliacion_Riesgos_Lab = " ".join(Afiliacion_Riesgos_Lab)

        cadena_Item_5 = cadena.index('CESANTIAS')
        Afiliacion_Compensacion_Fam = cadena[cadena_Item_4-3:cadena_Item_5-2]
        Afiliacion_Compensacion_Fam = " ".join(Afiliacion_Compensacion_Fam)

        cadena_Item_6 = cadena.index('PENSIONADOS')
        Afiliacion_Cesantias = cadena[cadena_Item_5-2:cadena_Item_6-1]
        Afiliacion_Cesantias = " ".join(Afiliacion_Cesantias)

        cadena_Item_7 = cadena.index('SOCIAL')
        Pensionados = cadena[cadena_Item_6:cadena_Item_7-5]
        Pensionados = " ".join(Pensionados)

        cadena_Item_8 = cadena.index('Ministerio')
        Asistencia_Social = cadena[cadena_Item_7-5:cadena_Item_8]
        Asistencia_Social = " ".join(Asistencia_Social)

        Otra_Informacion = cadena[cadena_Item_8:]
        Otra_Informacion = " ".join(Otra_Informacion)

        # print(Informacion_Basica)
        # print("\n")
        # print(Afiliacion_Salud)
        # print("\n")
        # print(Afiliacion_Riesgos_Lab)
        # print("\n")
        # print(Afiliacion_Compensacion_Fam)
        # print("\n")
        # print(Afiliacion_Cesantias)
        # print("\n")
        # print(Pensionados)
        # print("\n")
        # print(Asistencia_Social)

        result = Informacion_Basica+" "+Afiliacion_Salud+" "+Afiliacion_Riesgos_Lab+" "+Afiliacion_Compensacion_Fam+" "+Afiliacion_Cesantias+" "+Pensionados+" "+Asistencia_Social
        print(result)
        filanew = [Nombre[i],Apellido[i],Documento[i],Day_Expedicion[i] + "/"+ Month_Expedicion[i] + "/"+ Year_Expedicion[i],result]
        dataRUAF.loc[i] =filanew

        driver.quit()

    dataRUAF.to_csv('Archivos/Antecedentes.csv', index=True)
except:
    #Mostrar el dato en el que quedo la consulta

    #Guardar la consulta realizada
    dataRUAF.to_csv('Archivos/Antecedentes.csv', index=True)

