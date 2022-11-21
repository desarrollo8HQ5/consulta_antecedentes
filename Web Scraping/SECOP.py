import os
import pandas as pd
import numpy as np


from sodapy import Socrata
client = Socrata(
    "https://www.datos.gov.co/resource/",
    "7lnu0vn916owvlhc2kwz8jonu",
    username="desarrollo9hq5@hq5.com.co",
    password="Hq5desarrollo:",
    timeout=10
)
client = Socrata("https://www.datos.gov.co/resource/", '7lnu0vn916owvlhc2kwz8jonu')

socrata_dataset_identifier = 'xvdy-vvsk'

print("Domain: {domain:}\nSession: {session:}\nURI Prefix: {uri_prefix:}".format(**client.__dict__))

results = client.get(socrata_dataset_identifier)
df = pd.DataFrame.from_dict(results)
df.head()