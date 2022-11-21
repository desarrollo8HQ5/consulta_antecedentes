from PIL import Image
import os
from pytesseract import *

# pytesseract.tesseract_cmd = r'C:\Users\CO-225\AppData\Local\Tesseract-OCR\tesseract.exe'


# im = Image.open('captcha4.png')
# captcha = pytesseract.image_to_string(im, config='-psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKMNLOPKRSTUVWXYZ')
# captcha = captcha.replace(" ", "").strip()
# print(captcha)

import pytesseract
captcha = pytesseract.image_to_string()
captcha = captcha.replace(" ", "").strip()
print(captcha)