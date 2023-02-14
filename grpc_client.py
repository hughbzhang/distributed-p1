from __future__ import print_function

import logging

import grpc
import grpc_chat_pb2
import grpc_chat_pb2_grpc
import sys, select
from IPython import embed

def run():
    print("Will try to start")
    port = str(5000)

    with grpc.insecure_channel('localhost:{}'.format(port)) as channel:
        client_stub = grpc_chat_pb2_grpc.ChatStub(channel)

        while True:

            new_message = client_stub.listen(grpc_chat_pb2.Dummy(dummy=""))
            if new_message.message != "":
                print(new_message.message)

            # Read input from terminal
            input_exists, _, _ = select.select( [sys.stdin], [], [], 5)

            if (input_exists):
                command = sys.stdin.readline().strip()
                response = client_stub.try_command(grpc_chat_pb2.Command(command=command))
                print("Server response: " + response.message)

if __name__ == '__main__':
    logging.basicConfig()
    run()
