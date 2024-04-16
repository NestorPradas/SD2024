# SD2024

## Crear imagen
docker run -d --name rabbitmq -p 10.10.1.54:5672:5672 -p 10.10.1.54:15672:15672 rabbitmq:3.13-management

docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management

## Parar la ejecucion del contenedor
docker stop rabbitmq

## Reiniciar la ejecucion del contenedor
docker start rabbitmq

## Eliminar el contenedor
docker rm rabbitmq


