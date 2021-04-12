# Asistente Virtual (Casiopea v0.0.0.7)


## Descripción

Casiopea es un asistente virtual pseudointeligente, el cual está diseñado para optimizar el tiempo, está programado en python, usa interfaces graficas de Qt, Serialización en JSON, Encodificación en un sistema personalizado llamado CCF (Casiopea Command File) y Sistema de comandos (adición/administración) Aún se encuentra en desarollo.

## Log Cambios (v0.0.0.7)

### Cambios generales

- Se agregó un splash screen.
- Se documentó el código actual.
- Se mejoró el módulo que detectaba si las claves eran únicas al crear/modificar comandos.
- Se modificó la función de reconocimiento de voz.
- Ahora si no se detecta micrófono finaliza los hilos de reconocimiento de voz en main_window.
- Ahora los hilos del main_window arrancan en showEvent().
- Ahora el administrador de comandos lista los comandos desde el show_event().
- Los comandos funcionan por voz correctamente.
- Ahora los hilos en el main_window están en un diccionario.
- Ahora las ventanas secundarias (ej panel de ajustes) están en un diccionario.
- Ahora el micrófono reconoce si está activado o no.
- El sistema Speech to Text retorna "N/M" o "N/A" si no hay micrófono o no reconoce respectivamente.
- Se creó la clase "other_window_base" para ventanas nor principales.
- Ahora las clases de las ventanas no principales, heredan de "other_window_base".
- Se añadió el archivo "bugs.md" en donde se registrarán todos los bugs encontrados.
- Se retiró del repositorio de git "res/user-data/".
- Se controló una excepción de reconocimiento de voz en los hilos de main_window al entrar en showEvent.

### Sistema de log

- Se mejoró el sistema de log en general.
- Ahora el logfile se actualiza con cada escritura.
- La estructura del timeline del log, ahora es [HH:MM:SS].
- Se agregó el nombre del hilo desde el cual se escribe el log.

### Sistema de espera

- Se integró sistema de espera del asistente.
- El titulo de la ventana principal cambia según está o no en espera.
- Ahora se puede ver en el main_window si el sistema está en espera o no.
    - Se pueden usar los siguientes comandos para entrar en espera:
        - "Espera".
        - "desactivate".
        - "silencio".
    - Para salir del modo espera hay que decir el nombre del asistente.
- Se agregó la key "listen" en globaldata para controlar el modo espera del asistente.
- Los comandos no ejecutan si el asistente está en espera.

### Sistema de interacción con la UI por voz

- Ahora se puede interactuar por voz con los botones de la UI en pantalla.
- Se agregó el diccionario "voice_rules" donde se relacionan los botones y el comando por voz.
- Ahora cada ventana secundaria cuenta con su hilo de reconocimiento de voz.
- Ahora la variable in_focus controla el foco de cada ventana.
- El método focus_info ahora gestiona el foco de las ventanas.

## Log Cambios (v0.0.0.6) algunas pequeñas mejoras

### Cambios generales

- Se añadió .gitignore al proyecto.
- Se gestionó para que el repositorio no tenga en cuenta algunos directorios.
- Se comentaron todas las clases y funciones del proyecto.
- Se integró sistema de log al proyecto.

### Mejoras en ajustes

- Se agregó el botón "borrar datos" en el panel de ajustes.
- Ahora se pueden borrar los datos desde el menu de ajustes.
- Ahora se pueden ver la "user-data" en el panel de ajustes.
- Cuando se modifican los ajustes en el panel, se recarga la información.

### Mejoras en sistema de comandos

- Ahora se actualizan los comandos del administrador cuando se hace focus.
- Ahora al modificar comandos, se visualiza el texto en UTF-8.
- Ahora la pantalla de crear comandos se limpia cuando se pretende crear uno nuevo.
- Ahora los comandos se leen en minúsculas, así mismo, las keys se convierten en minúsculas.
- Ahora no se pueden crear comandos con keys repetidas.

## Log Cambios (v0.0.0.5)

### Cambios Generales

- Se solucionó "QCoreApplication::exec:: The event loop is already running"
- Ahora en la ventana principal pone el mensaje "Comandos"
- Ahora existe una Splash Screen al cargar el programa (Provisional).
- Ahora se dispone del "icon.ico"

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
- Se agregó el botón "Crear comando" desde el administrador de comandos.


## Log Cambios (v0.0.0.4)

### Cambios generales

- Ahora el "App.exec_()" se ejecuta desde el main.py.
- La ventana de ajustes ahora se puede abrir con el comando "ajustes".
- Las ventanas secundarias ahora son variables de "main_window".
- Ahora al guardar la información, el asistente dice "Guardardando la información".
- La clase "gui_controller" ya no es estática.
- Ahora se puede accerder a la main window desde la variable "W_WINDOW".
- Ahora el caracter que delimita los LKEYS es "|" debido a que ":" es muy frecuente en URLs.
- Se agregó la LKEY "EXECUTE" para ejecutar comandos CMD.

### Optimización

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

### Sistema de Creación de Comandos

- Se Añadió sistema de creación de comandos
- Debe hacerse revisión de "QCoreApplication::exec:: The event loop is already running" al ejecutar ajustes.
- Se agregó la clase "default_commands" para los comandos que usa el asistente por defecto.
- Se agregó la función "decode_document" para decodificar una hoja de comandos CCF desde texto plano
- Se añadieron más Keys

## Log Cambios (v0.0.0.3)

### Cambios Generales

- Se agregó la carpeta "res/audio" donde se guardarán los archivos TTS.
- La función SPEAK ahora es controlada con una excepción y un while que espera hasta poder hablar

### Hilos

- Ahora los comandos se ejecutan en un hilo llamado "hilo_comandos"
- Al finalizar la ejecución del programa, el hilo principal limpia los archivos en "audio"
- Los hilos añadidos, funcionan como "daemons" para terminarlos al finalizar la ejecución del programa.

### Reconocimiento de voz

- Se añadió sistema de reconocimiento de voz
- Se añadieron dos hilos nuevos ('Speech-TT', 'Speech-TT-Status') para controlar el flujo de voz
- Se creó la función 'recognize' para el reconocimiento de voz
- Ahora se pueden ejecutar comandos por medio de la voz

## Log Cambios (v0.0.0.2)

### Cambios Añadidos
- Carpetas requeridas creadas automáticamente.
- Se solucionó bug al cargar la "globaldata" (Funciona como LKEY :GLOBALDADA ID:)
- Ahora los archivos ".json" utilizan "UTF-8"

### Sistema de comandos

- Se integró el sistema de lectura de comandos
- Se agregaron más "Keys" para decodificar CCF
- Ahora se puede enviar un comando pulsando la tecla "Enter"
- Ahora se pueden decodificar varias "LKEYS" en la misma línea CCF
- Se añadió fichero "commands-info.json" para control de comandos
- Se agregó el módulo "CCF_extra_functions.py" para las funciones adicionales CCF

### UI

- Se añadió el control para el reconocimiento de voz en la UI (Aún sin lógica)
- Ahora cuando se cierra la ventana de ajustes (En primera configuración) corta la ejecución
- El mensaje "Hasta pronto" ahora se ejecuta desde el "closeEvent" de "main_window" y no al final del hilo main.py

## Log Cambios (v0.0.0.1)

### Sistemas y Cambios añadidos

- Se estructuró de forma completamente nueva.
- Sistema de comandos CCF (Casiopea Comand File).
- Fichero init.CCF para la configuración inicial del asistente.
- Fichero main.CCF para la ventana principal del asistente.
- Control de voces (Google voz online, Voz generica descargada offline).

### UI

- Obtuvo un ícono.
- Se integró interfaz gráfica Qt.
- Se integró script raíz "info.py"
- Se integró interfaz principal (Aún en desarrollo).
- Se integró el menú de ajustes para la configuración inicial. Contiene:
    - Menú serializable.
    - Alias del usuario.
    - Nombre personalizable del asistente.
    - Configuración de voz offline.
    - Volumen de voz.
    - Velocidad de habla.