import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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

def download_pdf(url, output_dir):
    r = requests.get(url)
    if r.status_code == 200:
        # Obtener el nombre del archivo desde la URL
        filename = os.path.join(output_dir, url.split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(r.content)
        print(f'Se descargó: {filename}')
    else:
        print(f'Error al descargar el archivo desde {url}')

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
