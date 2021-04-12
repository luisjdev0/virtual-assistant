#ID para guardar los audios sin sobreescribirse
voiceid = 0

#Chequear acceso a internet
def is_connect():
    '''
    Comprueba si existe conexión a internet.
    '''
    from socket import gethostbyname, create_connection
    from data.info import SYSTEM_LOG
    SYSTEM_LOG.write("Verificando conexión para voz")
    try:
        gethostbyname("google.com")
        connection = create_connection(("google.com", 80), 1)
        connection.close()
        SYSTEM_LOG.write("Hay conexión")
        return True
    except:
        SYSTEM_LOG.write("No hay conexión")
        return False

#Función para TTS (Google o voz por ordenador según conexión a internet)
def speak(text):
    '''
    Hace que el asistente hable mediante TTS (Online Google Voice, Offline Downloaded Voice).

    @param text: Texto que dirá el asistente
    '''
    global voiceid
    from data.info import DIRS, SYSTEM_LOG
    SYSTEM_LOG.write(f"Hablando ({text})")
    import time
    
    #Intenta hablar indeterminadamente hasta que lo logra
    while True:
        try:
            #Si existe conexión, usará el servicio de google
            if is_connect():
                from gtts import gTTS
                from playsound import playsound
                voicedir = f"{DIRS['folders']['audio']}/{voiceid}.mp3"

                voice = gTTS(text, lang="es")
                voice.save(voicedir)
                playsound(voicedir)

                voiceid += 1
            #de lo contrario, se eligirá la voz instalada que fue configurada
            else:

                import pyttsx3
                from data.info import globaldata

                info = globaldata['assistant-data']

                engine = pyttsx3.init()
                engine.setProperty('voice', info['voice-id'])
                engine.setProperty('volume', info['voice-volume'])
                engine.setProperty('rate', info['voice-rate'])

                engine.say(text)
                engine.runAndWait()
            break
        except:
            time.sleep(1)

#Reconocimiento de voz

def recognize():
    '''
    Función para el reconocimiento de voz del asistente.
    '''
    from data.info import SYSTEM_LOG
    import speech_recognition as sr

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        if not recognizer.energy_threshold < 46:
            audio = recognizer.listen(source)
        else:
            return "N/M"

    try:
        result = recognizer.recognize_google(audio, language='es-CO').lower()
        SYSTEM_LOG.write(f"Se reconoció por voz ({result})")
        print(result)
        return result
    except:
        return "N/A"