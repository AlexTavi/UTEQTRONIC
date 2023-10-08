import speech_recognition as sr
import pyttsx3

motorVoz=pyttsx3.init()
voz=motorVoz.getProperty('voices')
motorVoz.setProperty('voice',voz[0].id)
motorVoz.setProperty('rate',150)

reconocedor = sr.Recognizer()

def hablar(text):
    motorVoz.say(text)
    motorVoz.runAndWait()

def reconocer():
    with sr.Microphone() as fuente:
        hablar("¡¡¡Hola!!! ¿Cómo puedo ayudar?")
        reconocedor.adjust_for_ambient_noise(fuente,duration=2)
        print(".")
        audio = reconocedor.listen(fuente)

    try:
        reconocido = reconocedor.recognize_google(audio, language="es")
        print("Te entendí: ", reconocido)
    except sr.UnknownValueError:
        hablar("No te entendí")
    except sr.RequestError as e:
        print("No puede reconocer; {0}".format(e))   

if __name__ == "__main__":
    reconocer()
