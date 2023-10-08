import pytesseract
from PIL import Image
import PyPDF2

# Ruta al archivo PDF con una imagen
pdf_file_path = 'pdf/ConvocatoriaNvoIngreso.pdf'

# Crea un objeto PDF para escribir el texto extraído
pdf_output = PyPDF2.PdfWriter()

# Abre el archivo PDF con PyPDF2 para obtener el número de páginas
with open(pdf_file_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)  # Obten el número de páginas

    for page_number in range(num_pages):
        # Abre la página actual del PDF
        pdf_page = pdf_reader.pages[page_number]  # Usa 'pages' en lugar de 'getPage'

        # Extrae el texto de la imagen de la página
        image = Image.open('temp.png') # Debes proporcionar la ruta de la imagen, asegúrate de que exista
        text = pytesseract.image_to_string(image)

        # Agrega el texto extraído a la página PDF de salida
        pdf_page.mergePage(PyPDF2.PdfReader(text))

# Ruta para guardar el PDF de texto extraído
output_pdf_path = 'pdf/texto_extraido.pdf'

# Guarda el PDF de texto extraído en un archivo
with open(output_pdf_path, 'wb') as output_pdf_file:
    pdf_output.write(output_pdf_file)

# Imprime un mensaje de éxito
print(f"Texto extraído y guardado en '{output_pdf_path}'")
