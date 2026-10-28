"""
Asistente de voz básico (gratis).

Instalación:
    pip install SpeechRecognition pyttsx3 pyaudio ollama

Opcional (respuestas con IA local):
    1) Instala Ollama desde ollama.com
    2) ollama pull llama3.2:3b

Uso:
    python jarvis.py
    Di "Jarvis" + tu pregunta. Di "Jarvis apágate" para salir.
"""

import datetime
import speech_recognition as sr
import pyttsx3

# --- Configuración ---
NOMBRE = "jarvis"
IDIOMA = "es-PE"          # reconocimiento de voz
MODELO = "llama3.2:3b"    # modelo de Ollama (si está instalado)

# --- Voz (salida) ---
voz = pyttsx3.init()
voz.setProperty("rate", 170)
for v in voz.getProperty("voices"):
    if "spanish" in v.name.lower() or "es" in v.id.lower():
        voz.setProperty("voice", v.id)
        break


def hablar(texto):
    print(f"Jarvis: {texto}")
    voz.say(texto)
    voz.runAndWait()


# --- Oído (entrada) ---
reconocedor = sr.Recognizer()


def escuchar():
    with sr.Microphone() as mic:
        reconocedor.adjust_for_ambient_noise(mic, duration=0.5)
        print("Escuchando...")
        try:
            audio = reconocedor.listen(mic, timeout=8, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return None
    try:
        texto = reconocedor.recognize_google(audio, language=IDIOMA)
        print(f"Tú: {texto}")
        return texto.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        hablar("No puedo conectarme al servicio de reconocimiento.")
        return None


# --- Cerebro ---
historial = [{
    "role": "system",
    "content": "Eres Jarvis, un asistente personal. Responde en español, "
               "de forma breve y directa, máximo dos frases.",
}]


def responder(texto):
    # Comandos simples (funcionan sin IA)
    if "hora" in texto:
        return "Son las " + datetime.datetime.now().strftime("%H:%M")
    if "fecha" in texto or "día es hoy" in texto:
        return "Hoy es " + datetime.datetime.now().strftime("%d de %B de %Y")

    # Respuesta con IA local (si Ollama está disponible)
    try:
        import ollama
        historial.append({"role": "user", "content": texto})
        resp = ollama.chat(model=MODELO, messages=historial)
        respuesta = resp["message"]["content"]
        historial.append({"role": "assistant", "content": respuesta})
        return respuesta
    except Exception:
        return "No tengo un modelo de IA conectado, pero puedo decirte la hora o la fecha."


# --- Bucle principal ---
def main():
    hablar("Sistema activo.")
    while True:
        texto = escuchar()
        if not texto or NOMBRE not in texto:
            continue

        pedido = texto.replace(NOMBRE, "").strip()

        if "apágate" in pedido or "apagate" in pedido:
            hablar("Hasta luego.")
            break
        if not pedido:
            hablar("Dime.")
            continue

        hablar(responder(pedido))


if __name__ == "__main__":
    main()
