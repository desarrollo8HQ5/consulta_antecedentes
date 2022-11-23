from bs4 import BeautifulSoup 
import requests
import httplib2
# import antigravity
# import webbrowser

website = "https://www.interpol.int/es"
##Enviar solicitud a la  pagina
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())

http = httplib2.Http()
response, content2 = http.request(website)

box = soup.find('div', class_="header__right")
seleccion1=box.find('nav',class_="navigation js-MenuMobile")
seleccion2=seleccion1.find('ul',class_="navigation__menu")
seleccion3=seleccion2.find('li',class_="navigation__menu__item")
seleccion4=seleccion3.find('ul',class_="navigation__submenu")


##obtener links de la pagina
links = []
for link in BeautifulSoup(content2).find_all('a', href=True):
    links.append(link['href'])

for link in links:
    if "/es/Como-trabajamos/Notificaciones/Ver-las-notificaciones-rojas" in link:
        linkSearch=link

websiteSearch = website+linkSearch[3:]
result2 = requests.get(websiteSearch)
content2 = result2.text
soup2 = BeautifulSoup(content2, 'html.parser')
boxform = soup2.find('div', class_="wrapThis")
apellidos = boxform.find('input', id="name")
nombres = boxform.find('input', id="forename")
nacionalidad = boxform.find('select', id="nationality")
sexoRadio = boxform.find('div', class_="generalForm__genderPick generalForm__radioButton")
sexo= sexoRadio.find('input', id="sexId_placeholder")
edadrango1 = boxform.find('input', id="ageMin")
edadrango2 = boxform.find('input', id="ageMax")
send = boxform.find('button', id="submit")

elemntsForm = [apellidos,nombres,nacionalidad,sexo,edadrango1,edadrango2,send]

for i in elemntsForm:
    print(i)
    print("\n")



# with open(f'{interpol}.txt','w') as file:
#     file.write(data)