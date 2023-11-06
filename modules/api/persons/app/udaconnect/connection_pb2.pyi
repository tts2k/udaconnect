from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PersonMessage(_message.Message):
    __slots__ = ["id", "first_name", "last_name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    first_name: str
    last_name: str
    def __init__(self, id: _Optional[int] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ...) -> None: ...

class LocationMessage(_message.Message):
    __slots__ = ["id", "person_id", "latitude", "longitude", "creation_time"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PERSON_ID_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    person_id: int
    latitude: str
    longitude: str
    creation_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., person_id: _Optional[int] = ..., latitude: _Optional[str] = ..., longitude: _Optional[str] = ..., creation_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FindContactMessage(_message.Message):
    __slots__ = ["person_id", "start_date", "end_date", "meters"]
    PERSON_ID_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    METERS_FIELD_NUMBER: _ClassVar[int]
    person_id: int
    start_date: _timestamp_pb2.Timestamp
    end_date: _timestamp_pb2.Timestamp
    meters: int
    def __init__(self, person_id: _Optional[int] = ..., start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., meters: _Optional[int] = ...) -> None: ...

class ConnectionMessage(_message.Message):
    __slots__ = ["location", "person"]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    PERSON_FIELD_NUMBER: _ClassVar[int]
    location: LocationMessage
    person: PersonMessage
    def __init__(self, location: _Optional[_Union[LocationMessage, _Mapping]] = ..., person: _Optional[_Union[PersonMessage, _Mapping]] = ...) -> None: ...

class ConnectionResponse(_message.Message):
    __slots__ = ["connections"]
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[ConnectionMessage]
    def __init__(self, connections: _Optional[_Iterable[_Union[ConnectionMessage, _Mapping]]] = ...) -> None: ...
