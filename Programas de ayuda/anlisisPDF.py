from PyPDF2 import PdfReader

reader = PdfReader("cedula_claudia_barrantes.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[1]
text = page.extract_text()
print(text)