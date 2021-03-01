voiceid = 0

#Chequear acceso a internet
def is_connect():
    from socket import gethostbyname, create_connection, error
    try:
        gethostbyname("google.com")
        connection = create_connection(("google.com", 80), 1)
        connection.close()
        return True
    except:
        return False

#Función para TTS
def speak(text):
    global voiceid
    #Si existe conexión, usará el servicio de google
    if is_connect():
        from gtts import gTTS
        from playsound import playsound
        from os import remove
        from time import sleep
        voicedir = f"res/{voiceid}.mp3"
        voice = gTTS(text, lang="es")
        voice.save(voicedir)
        playsound(voicedir)
        remove(voicedir)
        voiceid += 1
    #de lo contrario, se eligirá la voz instalada que fue configurada
    else:

        #try:

        import pyttsx3
        from data.info import globaldata

        info = globaldata['assistant-data']

        engine = pyttsx3.init()
        engine.setProperty('voice', info['voice-id'])
        engine.setProperty('volume', info['voice-volume'])
        engine.setProperty('rate', info['voice-rate'])

        engine.say(text)
        engine.runAndWait()
        
        #except:
            
            #print(text)
