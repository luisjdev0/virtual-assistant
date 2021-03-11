# Asistente Virtual (Casiopea v0.0.0.3)


## Descripción

Casiopea es un asistente virtual pseudointeligente, el cual está diseñado para optimizar el tiempo, está programado en python, usa interfaces graficas de Qt y Serialización en JSON. Aún se encuentra en desarollo.

## Log Cambios (v0.0.0.3)

- Ahora los comandos se ejecutan en un hilo llamado "hilo_comandos"
- Se agregó la carpeta "res/audio" donde se guardarán los archivos TTS
- Al finalizar la ejecución del programa, el hilo principal limpia los archivos en "audio"
- La función SPEAK ahora es controlada con una excepción y un while que espera hasta poder hablar
- Se añadió sistema de reconocimiento de voz
- Se añadieron dos hilos nuevos ('Speech-TT', 'Speech-TT-Status') para controlar el flujo de voz
- Los hilos añadidos, funcionan como daemons para terminarlos al finalizar la ejecución del programa.
- Se creó la función 'recognize' para el reconocimiento de voz
- Ahora se pueden ejecutar comandos por medio de la voz

## Log Cambios (v0.0.0.2)

- Carpetas requeridas creadas automáticamente.
- Se añadió el control para el reconocimiento de voz en la UI (Aún sin lógica)
- Se añadió fichero "commands-info.json" para control de comandos
- Se solucionó bug al cargar la "globaldata" (Funciona como LKEY :GLOBALDADA ID:)
- Ahora los archivos ".json" utilizan "UTF-8"
- Ahora cuando se cierra la ventana de ajustes (En primera configuración) corta la ejecución
- El mensaje "Hasta pronto" ahora se ejecuta desde el "closeEvent" de "main_window" y no al final del hilo main.py
- Ahora se pueden decodificar varias "LKEYS" en la misma línea CCF
- Se agregó el módulo "CCF_extra_functions.py" para las funciones adicionales CCF
- Se integró el sistema de lectura de comandos
- Se agregaron más "Keys" para decodificar CCF
- Ahora se puede enviar un comando pulsando la tecla "Enter"

## Log Cambios (v0.0.0.1)

- Se estructuró de forma completamente nueva.
- Obtuvo un ícono.
- Se integró interfaz gráfica Qt.
- Se integró script raíz "info.py"
- Se integró el menú de ajustes para la configuración inicial. Contiene:
    - Menú serializable.
    - Alias del usuario.
    - Nombre personalizable del asistente.
    - Configuración de voz offline.
    - Volumen de voz.
    - Velocidad de habla.
- Sistema de comandos CCF (Casiopea Comand File).
- Fichero init.CCF para la configuración inicial del asistente.
- Fichero main.CCF para la ventana principal del asistente.
- Control de voces (Google voz online, Voz generica descargada offline).
- Se integró interfaz principal (Aún en desarrollo).