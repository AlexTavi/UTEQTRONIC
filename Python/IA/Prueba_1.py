import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to recognize speech from the microphone
def recognize_speech():
    with sr.Microphone() as source:
        print("Speak something in Spanish...")
        recognizer.adjust_for_ambient_noise(source,duration=1)
        audio = recognizer.listen(source)  # Listen to the microphone input

    try:
        # Recognize the speech using Google Web Speech API with Spanish language
        recognized_text = recognizer.recognize_google(audio, language="es-ES")
        print("Recognized text (in Spanish):", recognized_text)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))   

if __name__ == "__main__":
    recognize_speech()
