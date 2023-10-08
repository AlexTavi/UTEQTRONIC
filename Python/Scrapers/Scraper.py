import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import PyPDF2
import re
import glob
import string

url_uteq = 'https://admisiones.uteq.edu.mx/?x=1/'

def status_code_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        s = BeautifulSoup(r.text, 'lxml')
    else:
        print('Error: El estado de la solicitud no es correcto')
        s = None
    return s

def find_links_informes(s):
    informes_links = []
    if s:
        li_elements = s.find_all('li')
        for li in li_elements:
            a_element = li.find('a', class_='informes')
            if a_element and 'href' in a_element.attrs:
                informes_links.append(urljoin(url_uteq, a_element['href']))
    return informes_links

def sanitize_filename(filename):
    # Remove query parameters by splitting the filename at "?"
    filename_without_query = filename.split('?')[0]
    
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized_filename = ''.join(c if c in valid_chars else '_' for c in filename_without_query)
    return sanitized_filename

def download_pdf(url, output_dir):
    r = requests.get(url)
    if r.status_code == 200:
        # Obtain the filename from the URL
        filename = os.path.join(output_dir, sanitize_filename(url.split('/')[-1]))
        with open(filename, 'wb') as f:
            f.write(r.content)
        print(f'Se descargó: {filename}')
    else:
        print(f'Error al descargar el archivo desde {url}')

def extract_text_from_pdf(pdf_path, page_number):
    pdfFileObj = open(pdf_path, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    
    # Check if the specified page number is valid
    if page_number < len(pdfReader.pages):
        pageObj = pdfReader.pages[page_number]
        text = pageObj.extract_text()
        pdfFileObj.close()
        return text
    else:
        pdfFileObj.close()
        print(f'Error: Page number {page_number} is out of range in {pdf_path}')
        return None

if __name__ == '__main__':
    s = status_code_url(url_uteq)
    informes_links = find_links_informes(s)
    
    if informes_links:
        # Crear un directorio para guardar los archivos descargados
        output_dir = 'pdf'
        os.makedirs(output_dir, exist_ok=True)
        
        for i, link in enumerate(informes_links, start=1):
            print(f'Descargando enlace {i}: {link}')
            download_pdf(link, output_dir)
    else:
        print('No se encontraron enlaces de informes.')
    
    # Obtener la lista de archivos PDF en el directorio 'pdf'
    pdf_files = glob.glob('pdf/*.pdf')
    
    if pdf_files:
        # Ordenar la lista de archivos por fecha de modificación (el más reciente primero)
        pdf_files.sort(key=os.path.getmtime, reverse=True)
        
        # Tomar el archivo PDF más reciente
        latest_pdf = pdf_files[0]
        
        page_number = 0  # Cambia el número de página si es necesario
        text = extract_text_from_pdf(latest_pdf, page_number)
        
        if text:
            # Search for the word "trámite" in el archivo PDF más reciente
            match = re.search(r'\bTrámite\b', text, re.IGNORECASE)
            
            if match:
                # Get the starting position of the match
                start_position = match.start()
                
                # Find the position of the first period (.) after "trámite"
                end_position = text.find('.', start_position)
            
                if end_position != -1:
                    # Get the text from "trámite" to the first period (.)
                    text_until_period = text[start_position:end_position]
            
                    # Print the result
                    print(text_until_period)
    else:
        print('No se encontraron archivos PDF en el directorio "pdf".')
