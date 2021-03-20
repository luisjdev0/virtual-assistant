# Asistente Virtual (Casiopea v0.0.0.5)


## Descripción

Casiopea es un asistente virtual pseudointeligente, el cual está diseñado para optimizar el tiempo, está programado en python, usa interfaces graficas de Qt, Serialización en JSON, Encodificación en un sistema personalizado llamado CCF (Casiopea Command File) y Sistema de comandos (adición/administración) Aún se encuentra en desarollo.

## Log Cambios (v0.0.0.5)
### Administrador de comandos

- Se modificó la UI del administrador de comandos.
- Se creo la clase "edit_commands_window" para el administrador de comandos.
- Se agregó el comando que ejecuta el administrador de comandos.
- Se agregó la key que ejecuta el administrador de comandos mediante CCF.
- Ahora se pueden eliminar comandos desde el administrador.
- Ahora se pueden editar/modificar comandos desde el administrador.
- Ahora las CCFkeys se ven como listas en el administrador de comandos.
- Ahora se pueden ver las keys de cada comando en el administrador de comandos.
- Ahora al agregar un comando, se verifica su existencia para modificarlo.
- Se optimizó el código de la administración de comandos.
- Ahora en la ventana principal pone el mensaje "Comandos"
- Ahora existe una Splash Screen al cargar el programa (Provisional).
- Ahora se dispone del "icon.ico"
- Se agregó el botón "Crear comando" desde el administrador de comandos.


## Log Cambios (v0.0.0.4)
### Creación de comandos [+Optimización]

- Se Añadió sistema de creación de comandos
- Ahora el "App.exec_()" se ejecuta desde el main.py.
- La ventana de ajustes ahora se puede abrir con el comando "ajustes".
- Las ventanas secundarias ahora son variables de "main_window".
- Ahora al guardar la información, el asistente dice "Guardardando la información".
- La clase "gui_controller" ya no es estática.
- Ahora se puede accerder a la main window desde la variable "W_WINDOW".
- Se mejoró sutilmente el código de la configuración inicial.
- Se revisó el código a rasgos generales, se comentó y optimizó..
    - Se comentó mejor el módulo "data/info.py".
    - Se comentó mejor el módulo "res/modules/CCF_extra_functions.py".
    - Se comentó y optimizó el módulo "res/modules/command_manager.py".
    - Se comentó y optimizó el módulo "res/modules/jls_base.py".
    - Se comentó mejor el módulo "res/modules/load_jls.py".
    - Se comentó mejor el módulo "res/modules/voice_controller.py".
    - Se comentó mejor el módulo "res/modules/UI_manager.py".
    - Se comentó mejor el módulo "main.py".
- Debe hacerse revisión de "QCoreApplication::exec:: The event loop is already running" al ejecutar ajustes.
- Ahora el caracter que delimita los LKEYS es "|" debido a que ":" es muy frecuente en URLs.
- Se agregó la LKEY "EXECUTE" para ejecutar comandos CMD.
- Se agregó la clase "default_commands" para los comandos que usa el asistente por defecto.
- Se agregó la función "decode_document" para decodificar una hoja de comandos CCF desde texto plano
- Se añadieron más Keys

## Log Cambios (v0.0.0.3)
### Hilos y Reconocimiento de voz

- Ahora los comandos se ejecutan en un hilo llamado "hilo_comandos"
- Se agregó la carpeta "res/audio" donde se guardarán los archivos TTS
- Al finalizar la ejecución del programa, el hilo principal limpia los archivos en "audio"
- La función SPEAK ahora es controlada con una excepción y un while que espera hasta poder hablar
- Se añadió sistema de reconocimiento de voz
- Se añadieron dos hilos nuevos ('Speech-TT', 'Speech-TT-Status') para controlar el flujo de voz
- Los hilos añadidos, funcionan como "daemons" para terminarlos al finalizar la ejecución del programa.
- Se creó la función 'recognize' para el reconocimiento de voz
- Ahora se pueden ejecutar comandos por medio de la voz

## Log Cambios (v0.0.0.2)
### Sistema de comandos

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
### Primeros pasos

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