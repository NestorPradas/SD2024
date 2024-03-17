import grpc
from concurrent import futures
import Servicio_pb2
import Servicio_pb2_grpc

class ServicioGRPC(Servicio_pb2_grpc.ClienteServidorServicer):
    def __init__(self):
        # Declarar array para conexxiones
        
        self.todas_conexiones = {}
        super().__init__()

    def InicioSesion(self, request, context):
        # Enviar la solicitud al servidor 2 y obtener la respuesta

        ## Añadir conexion al array
        self.todas_conexiones[request.Nombre] = request.IP
        print("Cliente Conectado: ", request.Nombre)
        print("IP Conectado: ", request.IP)

        response = Servicio_pb2.TodoOk(ok=1)
        return response
    
    def SolicitarConexion(self, request, context):  
        nombreSolicitante=str(request.NombreSolicitante)
        print("Solicitante: ", nombreSolicitante)
        print("Solicitado: ", request.NombreSolicitado)
        ipSolicitante = str(self.todas_conexiones[request.NombreSolicitante])

        channel = grpc.insecure_channel('localhost:50050')
        stub = Servicio_pb2_grpc.ServidorServidorStub(channel)
        response = stub.SolicitarConexionServidor(Servicio_pb2.Session(Nombre="Cliente1", IP="ipSolicitante"))
        print("Response received from server:", response)

        response = Servicio_pb2.IpSolicitado(IP=ipSolicitante)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Servicio_pb2_grpc.add_ClienteServidorServicer_to_server(ServicioGRPC(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    print("Central Server started. Listening on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
