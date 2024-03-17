# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import Servicio_pb2 as Servicio__pb2


class ClienteServidorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.InicioSesion = channel.unary_unary(
                '/Servicio.ClienteServidor/InicioSesion',
                request_serializer=Servicio__pb2.Session.SerializeToString,
                response_deserializer=Servicio__pb2.TodoOk.FromString,
                )
        self.SolicitarConexion = channel.unary_unary(
                '/Servicio.ClienteServidor/SolicitarConexion',
                request_serializer=Servicio__pb2.Conectar.SerializeToString,
                response_deserializer=Servicio__pb2.IpSolicitado.FromString,
                )
        self.EnvioMensaje = channel.unary_unary(
                '/Servicio.ClienteServidor/EnvioMensaje',
                request_serializer=Servicio__pb2.Mensaje.SerializeToString,
                response_deserializer=Servicio__pb2.TodoOk.FromString,
                )
        self.CerrarSesion = channel.unary_unary(
                '/Servicio.ClienteServidor/CerrarSesion',
                request_serializer=Servicio__pb2.Session.SerializeToString,
                response_deserializer=Servicio__pb2.TodoOk.FromString,
                )


class ClienteServidorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def InicioSesion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SolicitarConexion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EnvioMensaje(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CerrarSesion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClienteServidorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'InicioSesion': grpc.unary_unary_rpc_method_handler(
                    servicer.InicioSesion,
                    request_deserializer=Servicio__pb2.Session.FromString,
                    response_serializer=Servicio__pb2.TodoOk.SerializeToString,
            ),
            'SolicitarConexion': grpc.unary_unary_rpc_method_handler(
                    servicer.SolicitarConexion,
                    request_deserializer=Servicio__pb2.Conectar.FromString,
                    response_serializer=Servicio__pb2.IpSolicitado.SerializeToString,
            ),
            'EnvioMensaje': grpc.unary_unary_rpc_method_handler(
                    servicer.EnvioMensaje,
                    request_deserializer=Servicio__pb2.Mensaje.FromString,
                    response_serializer=Servicio__pb2.TodoOk.SerializeToString,
            ),
            'CerrarSesion': grpc.unary_unary_rpc_method_handler(
                    servicer.CerrarSesion,
                    request_deserializer=Servicio__pb2.Session.FromString,
                    response_serializer=Servicio__pb2.TodoOk.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Servicio.ClienteServidor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ClienteServidor(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def InicioSesion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Servicio.ClienteServidor/InicioSesion',
            Servicio__pb2.Session.SerializeToString,
            Servicio__pb2.TodoOk.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SolicitarConexion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Servicio.ClienteServidor/SolicitarConexion',
            Servicio__pb2.Conectar.SerializeToString,
            Servicio__pb2.IpSolicitado.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EnvioMensaje(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Servicio.ClienteServidor/EnvioMensaje',
            Servicio__pb2.Mensaje.SerializeToString,
            Servicio__pb2.TodoOk.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CerrarSesion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Servicio.ClienteServidor/CerrarSesion',
            Servicio__pb2.Session.SerializeToString,
            Servicio__pb2.TodoOk.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ServidorServidorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SolicitarConexionServidor = channel.unary_unary(
                '/Servicio.ServidorServidor/SolicitarConexionServidor',
                request_serializer=Servicio__pb2.Session.SerializeToString,
                response_deserializer=Servicio__pb2.TodoOk.FromString,
                )


class ServidorServidorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SolicitarConexionServidor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServidorServidorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SolicitarConexionServidor': grpc.unary_unary_rpc_method_handler(
                    servicer.SolicitarConexionServidor,
                    request_deserializer=Servicio__pb2.Session.FromString,
                    response_serializer=Servicio__pb2.TodoOk.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Servicio.ServidorServidor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ServidorServidor(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SolicitarConexionServidor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Servicio.ServidorServidor/SolicitarConexionServidor',
            Servicio__pb2.Session.SerializeToString,
            Servicio__pb2.TodoOk.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)