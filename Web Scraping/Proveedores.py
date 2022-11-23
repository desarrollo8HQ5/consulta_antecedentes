import os
import PyPDF2
import pandas as pd
import os
from re import split
pdfFile = open ('Web Scraping/Proveedores-Ficticios-31-07-2021.pdf','rb')

pdfReader = PyPDF2.PdfFileReader(pdfFile)

Pages = pdfReader.numPages
# print(Pages)
Encripted = pdfReader.isEncrypted
# print(Encripted)
info = pdfReader.documentInfo
# print(info)

pageObj = pdfReader.getPage(0)
# print(pageObj.extract_text())


# Ajuste de datos
dataProvedores = pd.DataFrame(columns=['Nombres','Apellidos','Documento', 'Lugar','Provedores_Ficticios'])

#Importar datos
filename = "Datos/Datos Gestion Documental Corregidos.csv"
fullpath = os.path.join(filename)
archivo = pd.read_csv(fullpath)
nombres = archivo["nombres_y_apellidos"].iloc[0:20]


#Tratamiento de datos del dataframe
nombres= nombres.str.split(' ', expand=True)
nombres = nombres.rename(columns={0:'primer nombre', 1:'segundo nombre', 2:'primer apellido',3:'segundo apellido'})

# Datos de consulta
Direccion = []
Nit = []
PrimerNombre = []
SegundoNombre = []
PrimerApellido = []
SegundoApelldio = []

for x in nombres.index:

    #Solicitud automatica
    PrimerNombre.append(nombres["primer nombre"][x])
    SegundoNombre.append(nombres["segundo nombre"][x])
    PrimerApellido.append(nombres["primer apellido"][x])
    SegundoApelldio.append(nombres["segundo apellido"][x])
    Nit.append(archivo["documento"][x])
    Encontrado = False
    Result = ""
    Direccion = ""
    #Recorre todas las paginas
    for y in range(0, pdfReader.numPages):
        pageObj = pdfReader.getPage(y)
        infoPDF = pageObj.extract_text()
        #busca la coincidencias en todas las paginas
        if str(Nit[x]) in infoPDF:
            PageNum = y
            pageFind = pdfReader.getPage(PageNum)
            pageFind = str(pageFind.extract_text())
            posicion= pageFind.find(Nit[x])
            antes = pageFind[posicion-40:posicion]
            despues =  pageFind[posicion:posicion+100]
            ParteAnterior = antes.count(' ')
            PartePosterior = despues.count(' ')
            cadena = (antes+despues).split()
            for i in cadena:
                if i in Nit[x]:
                    posicionCadena = cadena.index(i)
                    Direc=cadena[posicionCadena-1]
                    Direccion = ''.join([i for i in Direc if not i.isdigit()])
                    Nit = cadena[posicionCadena]
                    NombreCompleto = cadena[posicionCadena+1] +' '+ cadena[posicionCadena+2] +' '+ cadena[posicionCadena+3] +' '+cadena[posicionCadena+4]
                    Resolucion = cadena[posicionCadena+5]
                    Fecha1 = cadena[posicionCadena+6] 
                    Publicacion = cadena[posicionCadena+7]+ ' ' +cadena[posicionCadena+8]
                    Fec2 = cadena[posicionCadena+9]
                    Fecha2 = split('\D+',Fec2)
                    Fecha2 = '/'.join(Fecha2)
                    Fecha2 = Fecha2[:-1]
                    Result = Direccion +" "+Resolucion +" "+Fecha1+" "+Publicacion+" "+Fecha2
                    print(Result)
                    filanew = [PrimerNombre[x]+" "+SegundoNombre[x],PrimerApellido[x]+" "+SegundoApelldio[x],Nit[x],Direccion,Result]
                    dataProvedores.loc[x] =filanew
                    Encontrado = True

        else:
            if Encontrado != True:
                Encontrado = True
                Result = "No Se encontraron datos para esta persona"
                Direccion ="null"
                filanew = [PrimerNombre[x]+" "+SegundoNombre[x],PrimerApellido[x]+" "+SegundoApelldio[x],Nit[x],Direccion,Result]
                dataProvedores.loc[x] =filanew
                print(Result)


dataProvedores.to_csv('Archivos/Antecedentes.csv', index=True)
