import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # Importa urljoin para crear URLs absolutas

# URL base de la UTEQ
base_url = "https://www.uteq.edu.mx"

# Palabra clave a buscar
keyword = "UTEQ"

# Realizar la solicitud HTTP a la página principal
response = requests.get(base_url)

# Comprobar si la solicitud fue exitosa
if response.ok:  # Verifica si la solicitud fue exitosa
    # Analizar el contenido HTML de la página
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar todos los enlaces en la página
    links = soup.find_all('a')
    
    # Iterar a través de los enlaces
    for link in links:
        # Obtener la URL del enlace
        relative_url = link.get('href')
        
        # Convertir la URL relativa en una URL absoluta
        absolute_url = urljoin(base_url, relative_url)
        
        # Realizar una solicitud HTTP a la página enlazada
        subpage_response = requests.get(absolute_url)
        
        # Comprobar si la solicitud fue exitosa
        if subpage_response.ok:  # Verifica si la solicitud fue exitosa
            # Analizar el contenido HTML de la página enlazada
            subpage_soup = BeautifulSoup(subpage_response.text, 'html.parser')
            
            # Buscar la palabra clave en el contenido de la página
            if keyword in subpage_soup.text:
                # Obtener el título de la página
                title = subpage_soup.title.text.strip()
                
                # Imprimir el título y la URL de la página que contiene la palabra clave
                print(f"Título: {title}")
                print(f"URL: {absolute_url}")
                print("-" * 50)
else:
    print("No se pudo acceder al sitio web de la UTEQ.")
