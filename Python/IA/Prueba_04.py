import requests
from bs4 import BeautifulSoup
import speech_recognition as sr
import pyttsx3

# Web scraping
def web_scraping():
    url = 'http://uteq.edu.mx'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = soup.find_all('div', class_='noticia')

    headlines = []
    for noticia in noticias:
        titulo = noticia.find('h2').text
        fecha = noticia.find('span', class_='fecha').text
        headlines.append(f'{fecha}: {titulo}')

    return headlines

# Reconocimiento de voz
def escuchar_pregunta():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Háblame...")
        recognizer.adjust_for_ambient_noise(source,duration=2)
        audio = recognizer.listen(source)
    return audio

# Texto a voz
def hablar_respuesta(respuesta):
    engine = pyttsx3.init()
    engine.say(respuesta)
    engine.runAndWait()

# Ejecutar el chatbot
if __name__ == "__main__":
    while True:
        try:
            # Escuchar pregunta
            pregunta_audio = escuchar_pregunta()
            pregunta_texto = sr.Recognizer().recognize_google(pregunta_audio, language="es-ES")
            print("Pregunta: " + pregunta_texto)

            # Realizar web scraping
            noticias = web_scraping()
            respuesta = "Aquí tienes las últimas noticias de la UTEQ:\n" + "\n".join(noticias)

            # Responder
            print(respuesta)
            hablar_respuesta(respuesta)

        except sr.UnknownValueError:
            print("No se pudo entender la pregunta")
        except sr.RequestError:
            print("Error al conectar con el servicio de reconocimiento de voz")
