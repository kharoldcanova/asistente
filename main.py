# -*- coding: utf-8 -*-

import speech_recognition as sr
import pyttsx3
import json
import spacy

# Configuración del reconocimiento de voz
r = sr.Recognizer()

# Configuración de la generación de voz
engine = pyttsx3.init()

# Obtener una lista de voces disponibles
voices = engine.getProperty('voices')

# Seleccionar una voz femenina en español
for voice in voices:
    if "Microsoft Hilda" in voice.name and voice.languages and voice.languages[0] == 'es-es':
        engine.setProperty('voice', voice.id)
        break

# Configurar la velocidad y el tono de la voz
engine.setProperty('rate', 180) # Velocidad de la voz
engine.setProperty('pitch', 80) 

# Cargar el modelo de lenguaje natural de spaCy
nlp = spacy.load("es_core_news_sm")

# Cargar el archivo JSON con las respuestas del asistente
with open("responses.json") as f:
    respuestas = json.load(f)

# Función para generar la respuesta del asistente de voz utilizando el modelo de spaCy
def generate_response(text):
    # Analizar el texto utilizando el modelo de spaCy
    doc = nlp(text)
    
    # Buscar la respuesta adecuada en el archivo JSON utilizando el modelo de spaCy
    for respuesta in respuestas:
        if respuesta["pattern"] in doc.text.lower():
            return respuesta["response"]
    
    # Si no se encuentra una respuesta adecuada, devolver un mensaje predeterminado
    return "Lo siento, no pude entender lo que dijiste."
# Función para hacer que el asistente de voz hable
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Función principal del asistente de voz
def assistant():
    # Escuchar la entrada de voz del usuario
    with sr.Microphone() as source:
        print("Di algo...")
        audio = r.listen(source)
    
    try:
        # Convertir la entrada de voz en texto
        text = r.recognize_google(audio, language='es-ES')
        print("Usuario:", text)
        
        # Generar una respuesta del asistente
        response = generate_response(text)
        print("Asistente:", response)
        
        # Hacer que el asistente hable la respuesta
        speak(response)
        
    except Exception as e:
        print(e)
    
# Ejecutar el asistente de voz en un bucle continuo
while True:
    assistant()
