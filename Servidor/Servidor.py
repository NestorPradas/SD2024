import grpc
from concurrent import futures
import Servicio_pb2
import Servicio_pb2_grpc
import pika
import docker
import redis
import signal
import sys
import yaml

class ServicioGRPC(Servicio_pb2_grpc.ClienteServidorServicer):
    def __init__(self):        

        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        file.close()

        self.client_port = config['grpc_client']['port'] 
        
        self.rabbit_ip = config['rabbit']['ip']

        self.redis_ip = config['redis']['ip']
        self.redis_port = config['redis']['port']

        self.todas_conexiones = {}
        self.cliente_redis = redis.StrictRedis(host=self.redis_ip, port=self.redis_port, db=0)
        super().__init__()

    def ConsultarUsuarios(self, request, context):
        lista = []
        print("[Servidor] Funcion ConsultarUsuarios")
        
        for nombre in self.todas_conexiones.keys():
            lista.append(nombre)

        return Servicio_pb2.UsuarioLista(array_usuarios=lista)
    
    def InicioSesion(self, request, context):
        print("[Servidor] Funcion InicioSesion")
        # self.todas_conexiones[request.Nombre] = request.IP # cambiar a redis
        self.cliente_redis.set(request.Nombre, request.IP)

        print("[Servidor] Cliente Conectado:", request.Nombre, ",", request.IP)

        response = Servicio_pb2.TodoOk(ok=1)
        return response
    
    def CerrarSesion(self, request, context):
        print("[Servidor] Funcion CerrarSesion")
        print("[Servidor] SesionCerrada", request.Nombre)
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(f'{self.rabbit_ip}'))
        channel = connection.channel()
        channel.exchange_delete(f"Privado: {request.Nombre}")

        # del self.todas_conexiones[request.Nombre] # cambiar a redis
        self.cliente_redis.delete(request.Nombre)
        
        channel.close()
        connection.close()

        response = Servicio_pb2.TodoOk(ok=1)
        return response
    
    def SolicitarConexion(self, request, context):  
        nombreSolicitante=str(request.NombreSolicitante)
        print("[Servidor] Funcion SolicitarConexion")
        print("[Servidor] Solicitante: ", nombreSolicitante)
        print("[Servidor] Solicitado: ", request.NombreSolicitado)

        #ipSolicitante = str(self.todas_conexiones[request.NombreSolicitante]) # cambiar a redis
        #ipSolicitado = str(self.todas_conexiones[request.NombreSolicitado]) # cambiar a redis

        ipSolicitante = self.cliente_redis.get(request.NombreSolicitante)
        ipSolicitado = self.cliente_redis.get(request.NombreSolicitado)

        if ipSolicitado is not None:
            ipSolicitado = ipSolicitado.decode('utf-8')
            if ipSolicitante is not None:
                ipSolicitante = ipSolicitante.decode('utf-8')
                channel = grpc.insecure_channel(ipSolicitado+f':{self.client_port}')
                stub = Servicio_pb2_grpc.ServidorServidorStub(channel)
                response = stub.SolicitarConexionServidor(Servicio_pb2.Session(Nombre=nombreSolicitante, IP=ipSolicitante))
                print("[Servidor] Respuesta de SolicitarConexion del cliente solicitado", response)
        else: 
            ipSolicitado = "No existe"

        response = Servicio_pb2.IpSolicitado(IP=ipSolicitado)

        return response
    
def start_redis():
    # Crear un cliente Docker
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    file.close()

    redis_image = config['redis']['image']
    redis_name = config['redis']['name']
    redis_ip = config['redis']['ip']
    redis_port = config['redis']['port']

    client = docker.from_env()
    try:
        contenedor = client.containers.get(redis_name)
        contenedor.start()
    except: 
        contenedor_config = {
            'image': f'{redis_image}',  # Utilizar la última imagen de Redis disponible en Docker Hub
            'detach': True,           # Ejecutar el contenedor en segundo plano
            'ports': {f'{redis_port}/tcp': (f'{redis_ip}', redis_port)},  # Mapear el puerto 6379 del contenedor al host
            'name': f'{redis_name}'  # Nombre del contenedor
        }

        # Crear el contenedor
        contenedor = client.containers.run(**contenedor_config)

    print("[Servidor] Contenedor Redis creado con éxito.")
    print("[Servidor] ID del contenedor:", contenedor.id)

    return contenedor

def start_rabbitMQ():
    # Crear un cliente Docker
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    file.close()

    rabbit_image = config['rabbit']['image']
    rabbit_name = config['rabbit']['name']
    rabbit_ip = config['rabbit']['ip']
    rabbit_port = config['rabbit']['port']
    rabbit_http = config['rabbit']['http']

    client = docker.from_env()
    try:
        contenedor = client.containers.get(f'{rabbit_name}')
        contenedor.start()
    except:
        # Configuración del contenedor RabbitMQ
        contenedor_config = {
            'image': f'{rabbit_image}',  # Utilizar la imagen RabbitMQ con el complemento de gestión
            'detach': True,                       # Ejecutar el contenedor en segundo plano
            'ports': {
                f'{rabbit_port}/tcp': (f'{rabbit_ip}', rabbit_port),  # Mapear el puerto 5672 del contenedor al host en la IP específica
                f'{rabbit_http}/tcp': (f'{rabbit_ip}', rabbit_http)  # Mapear el puerto 15672 del contenedor al host en la IP específica
            },
            'name': f'{rabbit_name}'      # Nombre del contenedor
        }

    # Crear el contenedor
        contenedor = client.containers.run(**contenedor_config)

    print("[Servidor] Contenedor RabbitMQ creado con éxito.")
    print("[Servidor] ID del contenedor:", contenedor.id)
    return contenedor

def serve():
    global redis_container
    global rabbitmq_container

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    file.close()

    grpc_server_ip = config['grpc_server']['ip']
    grpc_server_port = config['grpc_server']['port']

    signal.signal(signal.SIGINT, handler)
    redis_container = start_redis()
    rabbitmq_container = start_rabbitMQ()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Servicio_pb2_grpc.add_ClienteServidorServicer_to_server(ServicioGRPC(), server)
    server.add_insecure_port(f'{grpc_server_ip}:{grpc_server_port}')
    server.start()
    print(f"[Servidor] GRPC Listening on {grpc_server_ip}:{grpc_server_port}...")
    server.wait_for_termination()

def handler(signal, frame):
    print("[Servidor] Deteniendo contenedores...")
    redis_container.stop()
    rabbitmq_container.stop()
    print("[Servidor] Contenedores detenidos.")
    if input("¿Eliminar contenedores? ('y' para eliminar)\n") == 'y':
        redis_container.remove()
        rabbitmq_container.remove()
        print("[Servidor] Contenedores eliminados.")
    sys.exit(0)

if __name__ == '__main__':
    serve()
