import requests
from bs4 import BeautifulSoup
import re

# URL del sitio web para buscar subdominios
url = "https://uteq.edu.mx"

# Realiza una solicitud GET a la página web
response = requests.get(url)

# Verifica si la solicitud fue exitosa
if response.status_code == 200:
    # Utiliza BeautifulSoup para analizar el contenido HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Encuentra todos los enlaces en la página
    links = soup.find_all("a", href=True)
    
    # Patrón de expresión regular para extraer subdominios
    subdomain_pattern = r"https?://([^/]+)/"
    
    # Almacena los subdominios únicos en un conjunto (set)
    subdomains = set()
    
    for link in links:
        href = link["href"]
        match = re.match(subdomain_pattern, href)
        if match:
            subdomains.add(match.group(1))
    
    # Imprime los subdominios encontrados
    for subdomain in subdomains:
        print(subdomain)
else:
    print("Error al hacer la solicitud HTTP:", response.status_code)
