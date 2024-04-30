# SD2024
Aplicacion de chat para equipos en la misma red
- Iniciar chat privado si conocemos el nombre con el que se ha registrado otro usuario
- Iniciar chat publico exista o no el nombre del chat
- Descubrir que chats publicos hay disponibles y que clientes estan conectados
- Enviar mensajes anonimos a cualquier usuario aleatoriamente

## Dependencias
- grpc
- grpcio-tools
- Docker
- socket
- tkinter as tk
- threading
- yaml
- pika
- queue
- time
- requests
- random
- signal
- sys
- redis
- concurrent

## Iniciar la aplicacion
1. Modificar la configuracion en todos los archivos "config.yaml", como minimo indicar la IP del servidor y el puerto, si vamos a tener el servidor donde puede haber un usuario, los puertos para GRPC deben ser distintos.
2. Tener docker instalado y en ejecucion en el equipo donde se va a ejecutar el servidor. Si no estan las imagenes necesarias, seran descargadas automaticamente al iniciar el servidor.
3. En el quipo que declaremos como servidor, ejecutar el archivo start-server.sh
4. En los equipos declarados como clientes, ejecutar el archivo start-client.sh

## Crear el ejecutable de cliente
Si deaseamos que esto sea una aplicacion de escritorio, en la misma carpeta donde se encuentra el archivo EjecutarCliente.py, ejecutar el siguiente comando:
- pyinstaller -F --noconsole --onefile --add-data "config.yaml;." EjecutarCliente.py

Necesario: pip install pyinstaller

Ademas, debemos copiar el archivo "config.yaml" en la carpeta donde se encuentra el ejecutable.
