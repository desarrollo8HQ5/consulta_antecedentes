import pandas as pd
import numpy as np
from tabula.io import read_pdf

filename = 'Web Scraping/Proveedores-Ficticios-31-07-2021.pdf'

pfl = read_pdf(input_path=filename, pages=1, output_format="dataframe")
print(pfl[1])