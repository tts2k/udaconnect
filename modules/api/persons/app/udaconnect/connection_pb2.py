# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: connection.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x63onnection.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"B\n\rPersonMessage\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\"\x88\x01\n\x0fLocationMessage\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x11\n\tperson_id\x18\x02 \x01(\x05\x12\x10\n\x08latitude\x18\x03 \x01(\t\x12\x11\n\tlongitude\x18\x04 \x01(\t\x12\x31\n\rcreation_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x95\x01\n\x12\x46indContactMessage\x12\x11\n\tperson_id\x18\x01 \x01(\x05\x12.\n\nstart_date\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_date\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06meters\x18\x04 \x01(\x05\"W\n\x11\x43onnectionMessage\x12\"\n\x08location\x18\x01 \x01(\x0b\x32\x10.LocationMessage\x12\x1e\n\x06person\x18\x02 \x01(\x0b\x32\x0e.PersonMessage\"=\n\x12\x43onnectionResponse\x12\'\n\x0b\x63onnections\x18\x01 \x03(\x0b\x32\x12.ConnectionMessage2M\n\x11\x43onnectionService\x12\x38\n\x0c\x46indContacts\x12\x13.FindContactMessage\x1a\x13.ConnectionResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'connection_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PERSONMESSAGE']._serialized_start=53
  _globals['_PERSONMESSAGE']._serialized_end=119
  _globals['_LOCATIONMESSAGE']._serialized_start=122
  _globals['_LOCATIONMESSAGE']._serialized_end=258
  _globals['_FINDCONTACTMESSAGE']._serialized_start=261
  _globals['_FINDCONTACTMESSAGE']._serialized_end=410
  _globals['_CONNECTIONMESSAGE']._serialized_start=412
  _globals['_CONNECTIONMESSAGE']._serialized_end=499
  _globals['_CONNECTIONRESPONSE']._serialized_start=501
  _globals['_CONNECTIONRESPONSE']._serialized_end=562
  _globals['_CONNECTIONSERVICE']._serialized_start=564
  _globals['_CONNECTIONSERVICE']._serialized_end=641
# @@protoc_insertion_point(module_scope)