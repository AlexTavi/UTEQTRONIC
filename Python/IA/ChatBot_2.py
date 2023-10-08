import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import requests
import speech_recognition as sr
import pyttsx3

motorVoz=pyttsx3.init()
voz=motorVoz.getProperty('voices')
motorVoz.setProperty('voice',voz[0].id)
motorVoz.setProperty('rate',150)

reconocedor = sr.Recognizer()

lemmatizer = WordNetLemmatizer()

# Import your previously saved files
intents = json.loads(open('C:/Users/taviz/Desktop/Python/IA/json/intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

# Function to clean up sentences and lemmatize words
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Function to convert words to bag of words (0s and 1s)
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Function to predict the category of a sentence
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res == np.max(res))[0][0]
    category = classes[max_index]
    return category

# Function to fetch the current time from a website (you can replace the URL)
def fetch_current_time():
    try:
        # Use the WorldTimeAPI to get the current time in Mexico City
        url = 'http://worldtimeapi.org/api/timezone/America/Mexico_City'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            current_time = data['datetime']
            date, time = current_time.split("T")
            time,_=time.split(".")
            return date,time
        else:
            return "Could not fetch the time."
    except Exception as e:
        return str(e)
    else:
        return "Could not fetch the time."

# Chat loop
def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i['responses'])
            break
    return result.encode('utf-8')  # Codificar la respuesta en UTF-8 antes de devolverla

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
        return reconocido
    except sr.UnknownValueError:
        return "No te entendí"
    except sr.RequestError as e:
        print("No puede reconocer; {0}".format(e))   

# Chat loop
while True:
    message = reconocer()
    if 'time' in message.lower() or 'day' in message.lower():
        current_time = fetch_current_time()
        hablar(current_time)
    elif 'salir' or'adios'or 'bye'or'hasta luego' in message.lower():
        ints = predict_class(message)
        res = get_response(ints, intents)
        hablar(res.decode('utf-8'))
        break
    else:
        ints = predict_class(message)
        res = get_response(ints, intents)
        hablar(res.decode('utf-8'))  # Decodificar la respuesta en UTF-8 antes de imprimir

