from concurrent import futures
import logging
import random

import grpc
import grpc_chat_pb2
import grpc_chat_pb2_grpc

class Chat(grpc_chat_pb2_grpc.ChatServicer):

    def listen(self, request, context):

        if random.random() < 0.1:
            return grpc_chat_pb2.Response(message="Hello")
        else:
            return grpc_chat_pb2.Response(message="")

    def try_command(self, request, context):
        return grpc_chat_pb2.Response(message="Got command {}".format(request.command))

def serve():
    port = str(5000)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_chat_pb2_grpc.add_ChatServicer_to_server(Chat(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
