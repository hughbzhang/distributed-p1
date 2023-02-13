# Server application

import asyncio
import socket 
import re
import action
from typing import Union

# data
class User:
    def __init__(self, name: str):
        self._name = name

        # Store backlog of messages
        self._messages = []

        # Keep track of connection for this user
        self._connection = None

    # Asychronously log in and acquire backlog of messages
    async def connect(self, loop, sock: socket):
        self._connection = sock

        # flush stored messages
        for message in self._messages:
            await self.send_message(loop, message + '\n')
    
    # Log off
    def disconnect(self):
        self._connection = None
    
    # check if user is online
    def status(self):
        return self._connection != None

    # Asynchronously send message
    async def send_message(self, loop, text: str):
        if self.status():
           await loop.sock_sendall(self._connection, action.encode_message(action.STRING, text.encode()))
        else:
            self._messages.append(text)

    
class ChatStore:
    def __init__(self):
        # key: user name str
        # value: User class
        self._users = {}

    # create a new user
    def create_user(self, name: str, sock: socket):
        if name in self._users:
            return action.NOTOK
        else:    
            self._users[name] = User(name)
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

    # set whether a user is online, asynchronously
    async def connect(self, name: str, loop, sock):
        if name in self._users:
            await self._users[name].connect(loop, sock)
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

    # Asynchronously send message
    async def send_message(self, loop, name: str, text: str) -> bool:
        if name in self._users:
            await self._users[name].send_message(loop, text)
            return True
        else:
            return False

# Instance of server object
store = ChatStore()

# Asynchronously reply to query from client
async def reply(connection: socket,
            loop: asyncio.AbstractEventLoop) -> None:
    try:
        name = ''

        # Keep receiving queries from client
        while message := await loop.sock_recv(connection, 1024):
            
            # Figure out which action on what data
            [action_name, data] = action.decode_message(message)
            print("ACTION: ", action_name)

            # Create a new account
            if(action_name == "create"):
                user = data[0]
                status = store.create_user(user, connection)

                # Send confirmation message concurrently
                await loop.sock_sendall(connection, action.encode_message(status, b''))
            
            # Connect to a specific user to receive messages
            elif(action_name == 'connect'):
                name = data[0]

                # Wait until connecting to the requested user, if possible
                status = action.OK if await store.connect(name, loop, connection) else action.NOTOK

                # Concurrently send status message
                await loop.sock_sendall(connection, action.encode_message(status, b''))
            
            # Delete account
            elif(action_name == 'delete'):
                user = data[0]
                store.delete_user(user)
                if user == name:
                    name = ''
                
                # Concurrently send status message
                await loop.sock_sendall(connection, action.encode_message(action.OK, b''))
            
            # List users
            elif(action_name == 'list'):
                pattern = data[0] if len(data) >= 1 else None
                users = store.list_users(pattern)
                
                # Concurrently send status message
                await loop.sock_sendall(connection, action.encode_message(action.LIST, action.encode_list(users)))
            
            # Send a message to a specific user
            elif(action_name == 'send'):
                [user, text] = data
                status = action.OK if await store.send_message(loop, user, text) else action.NOTOK

                await loop.sock_sendall(connection, action.encode_message(status, b''))
            else:
                await loop.sock_sendall(connection, action.encode_message(action.NOTOK, b''))

    # Catch exceptions, report them, don't crash
    except Exception as ex:
        print(ex)
    finally:
        store.disconnect(name)
        connection.close()


# Asynchronously listen
async def listen(server_socket: socket,
                                loop: asyncio.AbstractEventLoop):
    # Keep listening
    while True:

        # Accept a connection
        connection, address = await loop.sock_accept(server_socket)
        
        # Continue listening 
        connection.setblocking(False)
        print(f"Got a connection from {address}")

        # Concurrently reply to newly formed connection
        asyncio.create_task(reply(connection, loop))

# Asyncronous main function; start here
async def main():
    # Set up a socket and start listening
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 3000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    # Listen for response
    await listen(server_socket, asyncio.get_event_loop())

asyncio.run(main())