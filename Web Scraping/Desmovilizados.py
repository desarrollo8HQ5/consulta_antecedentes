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
dataDesmovilizados = pd.DataFrame(columns=['Nombres','Apellidos','Documento','Desmovilizados'])

#Importar datos
filename = "Datos/Datos Gestion Documental Corregidos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
nombres = archivo["nombres_y_apellidos"].iloc[0:3]
Documentos = archivo["documento"].iloc[0:3]

#Datos de consulta
PrimerNombre = []
SegundoNombre =  []
PrimerApellido =  []
SegundoApelldio =  []
Documento = []
#Tratamiento de datos del dataframe
nombres= nombres.str.split(' ', expand=True)
nombres = nombres.rename(columns={0:'primer nombre', 1:'segundo nombre', 2:'primer apellido',3:'segundo apellido'})

print(Documento)
#Solicitud automatica
for i in nombres.index:
    PrimerNombre.append(nombres["primer nombre"][i])
    SegundoNombre.append(nombres["segundo nombre"][i])
    PrimerApellido.append(nombres["primer apellido"][i])
    SegundoApelldio.append(nombres["segundo apellido"][i])
    Documento = Documentos[i]


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
    # Inicializamos el navegador
    driver.get('https://www.fiscalia.gov.co/colombia/justicia-transicional-2/consulta-postulados/')
    #link_iframe = 'https://webjyp.fiscalia.gov.co/postulates'
    #driver.get(link_iframe)
    driver.execute_script("window.scrollBy(0,600)")
    time.sleep(1)

    #Busqueda de iframes                                                                                                                                                                                                            

    # frames = driver.find_elements(By.TAG_NAME,'iframe')
    # print(len(frames))

    # for i in frames:
    #     print("Frame src: "+i.get_attribute('src'))
    #     print("Frame name: "+i.get_attribute('name'))
    # WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "/html/body/div[6]/div[2]/div[2]/div/div[2]/div/div/div/div/div/iframe")))


    #Select iFrame
    element = driver.find_element(By.CLASS_NAME,'iframe-class')

    #Switch to iFrame
    driver.switch_to.frame(element)

    #Query document for the ID that you're looking for
    queryElement = driver.find_element(By.CLASS_NAME,'MuiInputBase-input')
    #Send key to the ID
    queryElement.send_keys(PrimerNombre[i]+" "+PrimerApellido[i])
    time.sleep(3)
    queryElement.send_keys(u'\ue007')
    time.sleep(3)

    Respuesta = driver.find_element(By.CSS_SELECTOR,'div.MuiGrid-root.MuiGrid-container')
    result = Respuesta.text
    if result == "":
        result="NO HAY DATOS EN LA BUSQUEDA"
        print(result)
    else:
        buscarDocumento = Documento in result
        if buscarDocumento == True:
            print(result)
        else:
            result="NO HAY DATOS EN LA BUSQUEDA"
            print(result)

    driver.switch_to.default_content()

    filanew = [PrimerNombre[i]+" "+SegundoNombre[i],PrimerApellido[i]+" "+SegundoApelldio[i],Documento,result]
    dataDesmovilizados.loc[i] =filanew
    #screenshot_name = "Archivos/"+"my_screenshot_name"+str(i)+".png"
    #driver.save_screenshot(screenshot_name)
    driver.quit()

dataDesmovilizados.to_csv('Archivos/Antecedentes.csv', index=True)