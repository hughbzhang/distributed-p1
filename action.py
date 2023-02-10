# Wire protocol

BUF_SIZE = 1024
ACTION_ID_SIZE = 15
DELIMITER = ","

# Status messages
OK = 'ok'
NOTOK = 'notok'
STRING = 'string'
LIST = 'list'
ERROR ='error'

def encode_message(action: str, payload: bytes) -> bytes:
    action_bytes = action.encode('utf-8')

    # First 15 bytes are reserved for action
    return action_bytes + b"\0" * (ACTION_ID_SIZE-len(action_bytes)) + payload

def decode_message(data: bytes):
    action = data[:ACTION_ID_SIZE].decode('utf-8').rstrip('\0')
    args = decode_list(data[ACTION_ID_SIZE:])

    return [action, args]


# For en/decoding data and arguments, not including action
def encode_list(list):
    return DELIMITER.join(list).encode('utf-8')

def decode_list(list_bytes):
    return list_bytes.decode('utf-8').rstrip('\0').split(DELIMITER)

