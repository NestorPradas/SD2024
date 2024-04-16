# SD2024

## Como iniciar el programa:

1. Iniciar docker y crear la imagen
2. Iniciar servidor
     python Servidor/Servidor.py
3. Iniciar clientes
     python Cliente/IniciarCliente.py

### Docker

#### Crear imagen
docker run -d --name rabbitmq -p 10.10.1.54:5672:5672 -p 10.10.1.54:15672:15672 rabbitmq:3.13-management

docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management

#### Parar la ejecucion del contenedor
docker stop rabbitmq

#### Reiniciar la ejecucion del contenedor
docker start rabbitmq

#### Eliminar el contenedor
docker rm rabbitmq
