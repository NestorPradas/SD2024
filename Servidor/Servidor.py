import grpc
from concurrent import futures
import Servicio_pb2
import Servicio_pb2_grpc
import pika

class ServicioGRPC(Servicio_pb2_grpc.ClienteServidorServicer):
    def __init__(self):        
        self.todas_conexiones = {}
        super().__init__()

    # Solo de prueba, se debe eliminar y implementar en RabbitMQ
    def ConsultarUsuarios(self, request, context):
        lista = []
        print("[Servidor] Funcion ConsultarUsuarios")
        
        for nombre in self.todas_conexiones.keys():
            lista.append(nombre)

        return Servicio_pb2.UsuarioLista(array_usuarios=lista)
    
    def InicioSesion(self, request, context):
        print("[Servidor] Funcion InicioSesion")
        self.todas_conexiones[request.Nombre] = request.IP
        print("[Servidor] Cliente Conectado:", request.Nombre, ",", request.IP)

        # Añadir Sesion a RabbitMQ

        response = Servicio_pb2.TodoOk(ok=1)
        return response
    
    def CerrarSesion(self, request, context):
        print("[Servidor] Funcion CerrarSesion")
        print("[Servidor] SesionCerrada", request.Nombre)
        
        connection = pika.BlockingConnection(pika.ConnectionParameters('10.10.1.54'))
        channel = connection.channel()
        channel.exchange_delete(f"Privado: {request.Nombre}")

        del self.todas_conexiones[request.Nombre]
        
        response = Servicio_pb2.TodoOk(ok=1)
        return response
    
    def SolicitarConexion(self, request, context):  
        nombreSolicitante=str(request.NombreSolicitante)
        print("[Servidor] Funcion SolicitarConexion")
        print("[Servidor] Solicitante: ", nombreSolicitante)
        print("[Servidor] Solicitado: ", request.NombreSolicitado)

        ipSolicitante = str(self.todas_conexiones[request.NombreSolicitante])
        ipSolicitado = str(self.todas_conexiones[request.NombreSolicitado])
        channel = grpc.insecure_channel(ipSolicitado+':50050')
        stub = Servicio_pb2_grpc.ServidorServidorStub(channel)
        response = stub.SolicitarConexionServidor(Servicio_pb2.Session(Nombre=nombreSolicitante, IP=ipSolicitante))
        print("[Servidor] Respuesta de SolicitarConexion del cliente solicitado", response)

        response = Servicio_pb2.IpSolicitado(IP=ipSolicitado)

        return response
    
def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Servicio_pb2_grpc.add_ClienteServidorServicer_to_server(ServicioGRPC(), server)
    server.add_insecure_port('10.10.1.54:50051')
    server.start()
    print("[Servidor] GRPC Listening on 10.10.1.54:50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
