# Design Notebook

## Part 1

- One of the main design choices we made was to use the python module ''asyncio''. This allows us to execute the server actions concurrently without explicitly managing threads. This makes our code easier to check and avoid common bugs arising from trying to explicitly manage threads.
- For the wire protocol, we chose the simplest specification that allowed us to correctly implement the necessary functionality. Our protocol permits encoding of appropriately-formatted string data corresponding as a sequence of bytes that can be communicated over a socket.
- We highlight our usage of Python's ``select()'' utility. This allows us to monitor, from the client-side, for a socket corresponding to the server. It allows for the client to wait for asynchronous communication from the server.
- For our design, we implemented two classes "User" and "ChatStore". These are just data structures we use to collect information about users. The server maintains a "ChatStore" object that is updated based on commands it receives from clients.

## Part 2

- Using gRPC we define "message" classes in grpc_chat.proto to describe the format of messages that can be sent back and forth between client and server. Such message objects contain fields like the name of the command, arguments of that command, and data for the command. The server implements a chat service that contains two functions: one that delivers unread messages to a client/user if they are logged in and another that handles requests made by clients.
- Complexity of code: Naturally, the code in part 2 is less complex. The use of gRPC allows us to abstract away certain details involved in implementing the wire protocol. This makes the code easier to understand, test and modify for other applications. For example, we can define and transfer abstract Message objects without needing to know the underlying specifications of the wire protocol.  Also, We no longer need to use asyncio or explicitly manage threads.
- Performance differences: Given the small scale nature of this application, we did not observe any significant performance differences between the two implementations. However, we do expect the gRPC version would scale better and easily accommodate more complex functionality.
- Buffer size: In part 1, the wire protocol specifies that the buffer size is 1024 bytes. This choice is arbitrary, but must be fixed at ahead of time. In contrast, in part 2, gRPC allows us to avoid having to explicitly specify the buffer size. Keeping this information ``private'' simplifies the code and overall design.
