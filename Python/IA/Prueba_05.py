import tensorflow as tf
import joblib
import numpy as np

# Define el modelo y la información de entrenamiento
modelo = None
tokenizer = None
preguntas_encoded = None
respuestas_encoded = None

# Intenta cargar el modelo y la información de entrenamiento desde archivos
try:
    modelo = tf.keras.models.load_model("chatbot_model")
    tokenizer = joblib.load("tokenizer.pkl")
    preguntas_encoded = np.load("preguntas_encoded.npy")
    respuestas_encoded = np.load("respuestas_encoded.npy")
    print("Modelo y datos de entrenamiento cargados.")
except (OSError, ImportError):
    print("No se encontraron archivos previamente entrenados. Se creará un nuevo modelo.")

# Si no se encuentran archivos previamente entrenados, crea un nuevo modelo y datos de entrenamiento
if modelo is None:
    # Tu código para definir y entrenar un nuevo modelo aquí

    # Guardar el modelo y los datos de entrenamiento
    modelo.save("chatbot_model")
    joblib.dump(tokenizer, "tokenizer.pkl")
    np.save("preguntas_encoded.npy", preguntas_encoded)
    np.save("respuestas_encoded.npy", respuestas_encoded)
    print("Modelo y datos de entrenamiento guardados.")

# Resto del código para la inferencia y la interacción con el usuario


# Función para realizar inferencia con el chatbot
def chatbot_inference(input_text):
    input_sequence = tokenizer([input_text])
    predicted_sequence = modelo.predict(input_sequence)
    predicted_text = tokenizer.sequences_to_texts(np.argmax(predicted_sequence, axis=-1))[0]
    return predicted_text

# Bucle para interactuar con el chatbot
print("Chatbot: ¡Hola! ¿En qué puedo ayudarte hoy?")
while True:
    user_input = input("Tú: ")
    if user_input.lower() == "salir":
        break
    response = chatbot_inference(user_input)
    print("Chatbot:", response)

print("Chatbot: Hasta luego. ¡Vuelve pronto!")

