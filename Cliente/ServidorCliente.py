import grpc
from concurrent import futures
import Servicio_pb2
import Servicio_pb2_grpc
from ChatWindow import ChatWindow
from queue import Queue

class ServicioGRPCServidorCliente(Servicio_pb2_grpc.ServidorServidorServicer, Servicio_pb2_grpc.ClienteServidorServicer):
    def __init__(self, nombre):
        self.nombre = nombre
        self.private_chats = {}
        super().__init__()

    def SolicitarConexionServidor(self, request, context):
        print("Mensaje recibido:", request.Nombre)
        print("Mensaje recibido:", request.IP)
        if request.Nombre not in self.private_chats:
            self.private_chats[request.Nombre] = ((request.IP, Queue()))
            self.chat_window = ChatWindow(self.nombre, request.Nombre,self.private_chats[request.Nombre][1], self.private_chats[request.Nombre][0])
            self.chat_window.start()
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
        print("SesionCerrada", request.Nombre)
        print("ip: ", request.IP)

        del self.private_chats[request.Nombre]
        
        #self.chat_window.close()
        
        response = Servicio_pb2.TodoOk(ok=1)
        return response
        

def serve(IP):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servidor=ServicioGRPCServidorCliente("Cliente")
    Servicio_pb2_grpc.add_ServidorServidorServicer_to_server(servidor, server)
    Servicio_pb2_grpc.add_ClienteServidorServicer_to_server(servidor, server)
    server.add_insecure_port(IP)
    server.start()
    print("Servidor iniciado. Escuchando en el puerto 50050...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve("localhost:50050")
