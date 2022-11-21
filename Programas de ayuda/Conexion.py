import requests
import urllib

# param = urllib.parse.urlencode({"authtoken":"token_here", 
#   "scope":"creatorapi",
#   "zc_ownername":"owner_here",
#   "criteria":'(PacienteSL=="Abilio Alfredo Finotti")'})

# url = "https://creatorapp.zohopublic.com/hq5colombia/hq5/report-perma/Analisis_de_datos_Gesti_n_documental_desarrollo/wMH2gqH6zegA28TMRO0Pum2FspUEkR06GNbkjGKtrjYz9Vqt6HSU19faEDOY5ayaUpjKdjaa1COC20zNFsT6xfyz2vtbqOvx2uDO".format("sample", "Employee_View", param)

# requests.get(url).content

import pandas as pd

url="https://creatorapp.zohopublic.com/hq5colombia/hq5/csv/Analisis_de_datos_Gesti_n_documental_desarrollo/wMH2gqH6zegA28TMRO0Pum2FspUEkR06GNbkjGKtrjYz9Vqt6HSU19faEDOY5ayaUpjKdjaa1COC20zNFsT6xfyz2vtbqOvx2uDO"
c=pd.read_csv(url)
print(c)
