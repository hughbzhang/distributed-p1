# Design Notebook

## Part 1

- One of the main design choices we made was to use the python module ''asyncio''. This allows us to execute the server actions concurrently without explicitly managing threads. This makes our code easier to check and avoid common bugs arising from trying to explicitly manage threads.
- For the wire protocol, we chose the simplest specification that allowed us to correctly implement the necessary functionality. Our protocol permits encoding of appropriately-formatted string data corresponding as a sequence of bytes that can be communicated over a socket.
- We highlight our usage of Python's ``select()'' utility. This allows us to monitor, from the client-side, for a socket corresponding to the server. It allows for the client to wait for asynchronous communication from the server.

## Part 2

- Complexity of code: Naturally, the code in part 2 is less complex. The use of gRPC allows us to abstract away certain details involved in implementing the wire protocol. This makes the code easier to understand, test and modify for other applications.
- Performance differences: TODO
- Buffer size: In part 1, the wire protocol specifies that the buffer size is 1024 bytes. This choice is arbitrary, but must be fixed at ahead of time. In constrast, in part 2, gRPC allows us to avoid having to explicitly specify the buffer size. Keeping this information ``private'' simplifies the code and overall design.