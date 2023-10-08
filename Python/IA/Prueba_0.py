import speech_recognition as sr
import pyttsx3

name = "gato"
escuchar=sr.Recognizer()
motorVoz=pyttsx3.init()
voz=motorVoz.getProperty('voices')
motorVoz.setProperty('voice',voz[0].id)
motorVoz.setProperty('rate',150)

def hablar(text):
    motorVoz.say(text)
    motorVoz.runAndWait()

def escuchando():
    rec = "" 
    try:
        with sr.Microphone() as fuente:
            escuchar.adjust_for_ambient_noise(fuente, duration=2)
            hablar("Escuchando...")
            pc=escuchar.listen(fuente)
            rec=escuchar.recognize_google(pc,language="es")
            rec=rec.lower()
            if name in rec:
                rec=rec.replace(name,'')
    except:
        pass
    return rec

def iniciar():
    rec=escuchando()
    if 'hola' in rec:
        hablar("Holaaa")
    else:
        hablar("nada")

if __name__== '__main__':
    iniciar()