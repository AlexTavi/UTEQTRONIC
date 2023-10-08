import tensorflow as tf
import numpy as np

# Conjunto de datos de entrenamiento (preguntas y respuestas ficticias)
questions = ["¿Cómo estás?", "¿Cuál es tu nombre?", "¿Qué hora es?"]
answers = ["Estoy bien, gracias.", "Soy un chatbot.", "No tengo reloj."]

# Tokenización de preguntas y respuestas
tokenizer = tf.keras.layers.TextVectorization(output_sequence_length=20)  # Asegura que todas las secuencias tengan la misma longitud
tokenizer.adapt(questions + answers)
vocab_size = len(tokenizer.get_vocabulary())
embedding_dim = 256

# Preparación de datos de entrenamiento
input_sequences = tokenizer(questions)
output_sequences = tokenizer(answers)

# Modelo de chatbot
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, mask_zero=True),
    tf.keras.layers.LSTM(128),
    tf.keras.layers.Dense(vocab_size, activation='softmax')
])

# Compilación del modelo
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Entrenamiento del modelo
model.fit(input_sequences, output_sequences, epochs=100)

# Función para generar respuestas
def generate_response(input_text):
    input_sequence = tokenizer(input_text)
    predicted_sequence = model.predict(input_sequence)
    predicted_word_index = np.argmax(predicted_sequence, axis=-1)
    return tokenizer.sequences_to_texts(predicted_word_index)[0]

# Interacción con el chatbot
while True:
    user_input = input("Usuario: ")
    if user_input.lower() == 'salir':
        break
    response = generate_response(user_input)
    print("Chatbot:", response)
