import grpc
from concurrent import futures
import Servicio_pb2
import Servicio_pb2_grpc
from ChatWindow import ChatWindowGRPC
from queue import Queue

import yaml

class ServicioGRPCServidorCliente(Servicio_pb2_grpc.ServidorServidorServicer, Servicio_pb2_grpc.ClienteServidorServicer):
    def __init__(self, nombre):
        self.nombre = nombre
        self.private_chats = {}

        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        file.close()

        self.client_port = config['grpc_client']['port'] 

        super().__init__()

    def SolicitarConexionServidor(self, request, context):
        print("Conectado con", request.Nombre, "de Ip", request.IP)
        if request.Nombre not in self.private_chats:
            q = Queue()
            chat_window = ChatWindowGRPC(self.nombre, request.Nombre, q, request.IP + f":{self.client_port}")

            self.private_chats[request.Nombre] = ((request.IP, q, chat_window))
            self.private_chats[request.Nombre][2].start()

            response = Servicio_pb2.TodoOk(ok=1)
        else:
            response = Servicio_pb2.TodoOk(ok=0)
        return response
    
    def EnvioMensaje(self, request, context):
        print(request.NombreRemitente)
        print(request.MensajeRemitente)
        try:
            self.private_chats[request.NombreRemitente][1].put(request.MensajeRemitente)
            response = Servicio_pb2.TodoOk(ok=1)
        except KeyError:
            response = Servicio_pb2.TodoOk(ok=0)

        return response
    
    def CerrarSesion(self, request, context):
        self.private_chats[request.Nombre][1].put("Desconectado")
        self.private_chats[request.Nombre][2].conectado = False
        
        del self.private_chats[request.Nombre]
        
        response = Servicio_pb2.TodoOk(ok=1)
        return response
        

def serve(IP, nombre):
    with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

    file.close()

    client_port = config['grpc_client']['port'] 

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servidor=ServicioGRPCServidorCliente(nombre)
    Servicio_pb2_grpc.add_ServidorServidorServicer_to_server(servidor, server)
    Servicio_pb2_grpc.add_ClienteServidorServicer_to_server(servidor, server)
    server.add_insecure_port(str(IP)+ f':{client_port}')
    server.start()
    print("Servidor iniciado. Escuchando en el puerto 50050...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve("localhost", "Cliente1")
