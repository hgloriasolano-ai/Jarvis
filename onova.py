# Onova - Asistente de voz basico con palabra de activacion
# Instalar: pip install SpeechRecognition pyttsx3 pyaudio

import datetime
import speech_recognition as sr
import pyttsx3

NOMBRE = "Onova"

# Formas en que el reconocimiento puede escribir "Onova"
VARIANTES = [
    "o nova", "onova", "onoba", "o noba", "honova", "h onova",
    "onuva", "o nueva", "onueva", "nova", "nueva",
]
# Se ordenan de mas larga a mas corta para borrar primero la mas especifica
VARIANTES.sort(key=len, reverse=True)

voz = pyttsx3.init()
voz.setProperty("rate", 170)

reconocedor = sr.Recognizer()


def hablar(texto):
    print(NOMBRE + ":", texto)
    voz.say(texto)
    voz.runAndWait()


def escuchar():
    with sr.Microphone() as mic:
        reconocedor.adjust_for_ambient_noise(mic, duration=0.5)
        print("Escuchando...")
        audio = reconocedor.listen(mic, phrase_time_limit=8)
    try:
        texto = reconocedor.recognize_google(audio, language="es-PE")
        print("Tu:", texto)
        return texto.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        hablar("No hay conexion a internet.")
        return ""


def detectar_nombre(texto):
    """Devuelve (fue_llamada, pedido_sin_el_nombre)."""
    for v in VARIANTES:
        if v in texto:
            return True, texto.replace(v, "", 1).strip(" ,.")
    return False, texto


def responder(texto):
    if "hola" in texto:
        return "Hola, soy " + NOMBRE + ". En que puedo ayudarte?"
    if "hora" in texto:
        return "Son las " + datetime.datetime.now().strftime("%H:%M")
    if "fecha" in texto or "dia es hoy" in texto:
        return "Hoy es " + datetime.datetime.now().strftime("%d/%m/%Y")
    if "tu nombre" in texto or "como te llamas" in texto:
        return "Me llamo " + NOMBRE + "."
    return "No entendi. Puedes repetirlo?"


hablar("Hola, soy " + NOMBRE + ". Llamame por mi nombre. Di salir para terminar.")

while True:
    texto = escuchar()
    if texto == "":
        continue

    llamada, pedido = detectar_nombre(texto)
    if not llamada:
        continue  # no la llamaron, la ignora

    if "salir" in pedido or "adios" in pedido or "apagate" in pedido:
        hablar("Hasta luego.")
        break
    if pedido == "":
        hablar("Dime.")
        continue

    hablar(responder(pedido))
