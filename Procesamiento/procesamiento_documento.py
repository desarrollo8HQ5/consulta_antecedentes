# import module
from pdf2image import convert_from_path
import cv2
import numpy as np


# Store Pdf with convert_from_path function
images = convert_from_path('Procesamiento\\cc2.pdf',500,poppler_path=r'C:\Program Files\poppler-22.11.0\Library\bin')

for i in range(len(images)):
	# Save pages as images in the pdf
	images[i].save('Procesamiento\\page'+ str(i) +'.jpg', 'JPEG')

