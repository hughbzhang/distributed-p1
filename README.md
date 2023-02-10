# Design Exercise: Wire Protocols


## Instructions

### Prerequisites
Use Python 3.8 and ayncio.

1. Run "python3.8 server.py"
2. Run "python3.8 client.py"

### Usage
The client application supports the following commands, via stdin.

1. **CREATE**: "create user" creates a new user named "user". Error will be returned if "user" already exists.
2. **CONNECT**: "connect user" receives any queued up messages for "user". After calling this, "user" will immediately receive any messages sent to it.
3. **DELETE**: "delete user" deletes the user named "user", if it exists. Unread messages to "user" will be deleted as well.
4. **LIST**: "list pattern" lists all users matching the regex "pattern". 
5. **SEND**: "send user msg" sends "msg" to user "user", if it exists. If "user" doesn't exist, error is returned. If "user" is logged in and has invoked "connect user" already, then "msg" will be delivered immediately. If "user" is not loogged in, but exists, "msg" will be added to a queue. The next time "user" logs in and invokes "connect user", all messages in the queue will be delivered.


## Wire protocol

This protocol permits transmission of strings of the form "command args data", where "command" is one of {create, connect, delete, list, send}, "args" denotes a list of arguments (such as usernames), and "data" is a string (e.g. message). To encode "command args data":
- First 15 bytes correspond to UTF8 encoding of "command", padded with null bytes as needed. So, null byte(s) will separate the command part from the arguments/data part.
- Next bytes correspond to UTF8 encoding of "args"
- Next bytes correspond to UTF8 encoding of "data"
- If "args" or "data" contain multiple space-separated strings, they get replaced by UTF8 encoding of those comma-separated strings.
- Buffer size is 1024 bytes.

## TODO

### P1
- Comment code: DONE
- Check 5 functions: DONE
    - Document instructions: DONE
    - EXample usage
- Specify wire protocol: DONE
- Client/server on separate machines?
- Set up Github repo?
- Notebook: design choices
- Big endian vs little endian?

### P2