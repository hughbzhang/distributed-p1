from concurrent import futures
import logging
import random

import grpc
import grpc_chat_pb2
import grpc_chat_pb2_grpc
from IPython import embed

# Server application

import asyncio
import socket
import re
import action
from typing import Union
from collections import defaultdict

class ChatStore:
    def __init__(self):
        # key: user name str
        # value: User class
        self._users = {}
        self.unsent_messages = defaultdict(list)

    # create a new user
    def create_user(self, name: str):
        if name in self._users:
            return action.NOTOK
        else:
            self._users[name] = name
            return action.OK

    # delete users
    def delete_user(self, name: str):
        if name in self._users:
            del self._users[name]
            print("Deleted user {}".format(name))
        else:
            print("User {} not found".format(name))

    # list users
    def list_users(self, pattern: str = '*'):
        return list(filter(lambda user_name: re.search(pattern, user_name), self._users.keys()))

    def connect(self, name: str):
        if name in self._users:
            return True
        else:
            return False

    # Log off
    def disconnect(self, name: str):
        if name in self._users:
            self._users[name].disconnect()
            return True
        else:
            return False

    # Queue up message for sending
    def send_message(self, name: str, text: str) -> bool:
        self.unsent_messages[name].append(text)
        print("Name {} has {} messages".format(name, len(self.unsent_messages[name])))
        return True

# Instance of server object
store = ChatStore()

def execute_command(command: grpc_chat_pb2.Command):

    # Parse command, args, data
    try:
        action_name, data = command.command.split()[0], command.command.split()[1:]
    except Exception as ex:
        return action.NOTOK, ex

    print("ACTION: ", action_name)
    extra_data = {"command": action_name}

    try:
        # Create a new account
        if(action_name == "create"):
            user = data[0]
            status = store.create_user(user)

        # Connect to a specific user to receive messages
        elif(action_name == 'connect'):
            name = data[0]

            # Wait until connecting to the requested user, if possible
            status = action.OK if store.connect(name) else action.NOTOK
            extra_data["user"] = name

        # Delete account
        elif(action_name == 'delete'):
            user = data[0]
            status = store.delete_user(user)
            if user == name:
                name = ''

        # List users
        elif(action_name == 'list'):
            pattern = data[0] if len(data) >= 1 else None
            users = store.list_users(pattern)
            status = action.OK

        # Send a message to a specific user
        elif(action_name == 'send'):
            [user, text] = data
            status = action.OK if store.send_message(user, text) else action.NOTOK
    except Exception as ex:
        print (ex)
        status = action.NOTOK

    return status, extra_data

class Chat(grpc_chat_pb2_grpc.ChatServicer):

    def listen(self, request, context):
        message = ""

        while len(store.unsent_messages[request.name]) > 0:
            raw_message = store.unsent_messages[request.name].pop(0)
            message += "Message: " + raw_message + "\n\n"
            print("Sending message " + raw_message)

        return grpc_chat_pb2.Response(message=message)

    def try_command(self, request, context):

        status, extra_data = execute_command(request)

        if extra_data["command"] == "connect":
            return grpc_chat_pb2.Response(message="Connection successful for user {}".format(extra_data["user"]), name=extra_data["user"])
        else:
            return grpc_chat_pb2.Response(message="Got command ||{}||".format(request.command))

def serve():
    port = str(3000)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_chat_pb2_grpc.add_ChatServicer_to_server(Chat(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
