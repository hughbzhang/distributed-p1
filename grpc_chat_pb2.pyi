from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Command(_message.Message):
    __slots__ = ["command"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    command: str
    def __init__(self, command: _Optional[str] = ...) -> None: ...

class Dummy(_message.Message):
    __slots__ = ["dummy"]
    DUMMY_FIELD_NUMBER: _ClassVar[int]
    dummy: str
    def __init__(self, dummy: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
