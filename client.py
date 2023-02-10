# Client application

import socket
import action
import sys
import select
import asyncio

# Receive message along a socket
def listener(s: socket):

    # Decode message received and status
    [resp_name, data] = action.decode_message(s.recv(1024))
    if(resp_name == action.OK):
        print("Action succeeded")
    elif(resp_name == action.NOTOK):
        print('Action failed')
    elif(resp_name == action.ERROR):
        print('Server error')
    else: 
        print("Server: " + ", ".join(data))

# Send a message along socket
def reader(s: socket, line: str):
    
    # Parse
    command = line.split()
    action_name = command[0]
    args = command[1:]
    
    if(len(args) > 1):
        args = [args[0], " ".join(args[1:])]

    # Send command+message along socket.
    s.sendall(action.encode_message(action_name, action.encode_list(args)))

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to server at this location
        s.connect(('localhost', 3000))
        
        # Keep repeating
        while True:
            try:
                # List of sockets, including the one we just connected to
                sockets_list = [sys.stdin, s]

                # Use select utility to figure out which ones are on read mode
                read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

                for socks in read_sockets:
                    # Client reads a message from server  
                    if socks == s:
                        listener(s)

                    # Client wants to send a message to server; specified by writing command + message in stdin.
                    # See documentation for how command+message should be formatted.  
                    else:
                        reader(s, sys.stdin.readline().rstrip())
            except:
                break


main()