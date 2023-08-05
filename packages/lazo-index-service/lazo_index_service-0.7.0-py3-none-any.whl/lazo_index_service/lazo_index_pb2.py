# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lazo_index.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='lazo_index.proto',
  package='lazo_index',
  syntax='proto3',
  serialized_options=b'\n\027edu.nyu.vida.lazo_indexP\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x10lazo_index.proto\x12\nlazo_index\";\n\x10\x43olumnIdentifier\x12\x12\n\ndataset_id\x18\x01 \x01(\t\x12\x13\n\x0b\x63olumn_name\x18\x02 \x01(\t\"W\n\x0c\x43olumnValues\x12\x0e\n\x06values\x18\x01 \x03(\t\x12\x37\n\x11\x63olumn_identifier\x18\x02 \x01(\x0b\x32\x1c.lazo_index.ColumnIdentifier\"_\n\x08\x44\x61taPath\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x03 \x01(\t\x12\x38\n\x12\x63olumn_identifiers\x18\x02 \x03(\x0b\x32\x1c.lazo_index.ColumnIdentifier\"W\n\x0eLazoSketchData\x12\x1b\n\x13number_permutations\x18\x01 \x01(\x05\x12\x13\n\x0bhash_values\x18\x02 \x03(\x12\x12\x13\n\x0b\x63\x61rdinality\x18\x03 \x01(\x12\"J\n\x12LazoSketchDataList\x12\x34\n\x10lazo_sketch_data\x18\x01 \x03(\x0b\x32\x1a.lazo_index.LazoSketchData\"3\n\x07\x44\x61taset\x12\x12\n\ndataset_id\x18\x01 \x01(\t\x12\x14\n\x0c\x63olumn_names\x18\x02 \x03(\t\"\x12\n\x03\x41\x63k\x12\x0b\n\x03\x61\x63k\x18\x01 \x01(\x08\"\x16\n\x05Value\x12\r\n\x05value\x18\x01 \x01(\t\"F\n\x10LazoQueryResults\x12\x32\n\rquery_results\x18\x01 \x03(\x0b\x32\x1b.lazo_index.LazoQueryResult\"V\n\x0fLazoQueryResult\x12,\n\x06\x63olumn\x18\x01 \x01(\x0b\x32\x1c.lazo_index.ColumnIdentifier\x12\x15\n\rmax_threshold\x18\x02 \x01(\x02\"R\n\x14LazoQueryResultsList\x12:\n\x14\x63olumn_query_results\x18\x01 \x03(\x0b\x32\x1c.lazo_index.LazoQueryResults2\xd9\x04\n\tLazoIndex\x12\x43\n\tIndexData\x12\x18.lazo_index.ColumnValues\x1a\x1a.lazo_index.LazoSketchData\"\x00\x12G\n\rIndexDataPath\x12\x14.lazo_index.DataPath\x1a\x1e.lazo_index.LazoSketchDataList\"\x00\x12O\n\x15GetLazoSketchFromData\x12\x18.lazo_index.ColumnValues\x1a\x1a.lazo_index.LazoSketchData\"\x00\x12S\n\x19GetLazoSketchFromDataPath\x12\x14.lazo_index.DataPath\x1a\x1e.lazo_index.LazoSketchDataList\"\x00\x12\x38\n\x0eRemoveSketches\x12\x13.lazo_index.Dataset\x1a\x0f.lazo_index.Ack\"\x00\x12@\n\tQueryData\x12\x11.lazo_index.Value\x1a\x1c.lazo_index.LazoQueryResults\"\x00(\x01\x12I\n\rQueryDataPath\x12\x14.lazo_index.DataPath\x1a .lazo_index.LazoQueryResultsList\"\x00\x12Q\n\x13QueryLazoSketchData\x12\x1a.lazo_index.LazoSketchData\x1a\x1c.lazo_index.LazoQueryResults\"\x00\x42\x1b\n\x17\x65\x64u.nyu.vida.lazo_indexP\x01\x62\x06proto3'
)




_COLUMNIDENTIFIER = _descriptor.Descriptor(
  name='ColumnIdentifier',
  full_name='lazo_index.ColumnIdentifier',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dataset_id', full_name='lazo_index.ColumnIdentifier.dataset_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='column_name', full_name='lazo_index.ColumnIdentifier.column_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=91,
)


_COLUMNVALUES = _descriptor.Descriptor(
  name='ColumnValues',
  full_name='lazo_index.ColumnValues',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='lazo_index.ColumnValues.values', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='column_identifier', full_name='lazo_index.ColumnValues.column_identifier', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=93,
  serialized_end=180,
)


_DATAPATH = _descriptor.Descriptor(
  name='DataPath',
  full_name='lazo_index.DataPath',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='lazo_index.DataPath.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='lazo_index.DataPath.url', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='column_identifiers', full_name='lazo_index.DataPath.column_identifiers', index=2,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=182,
  serialized_end=277,
)


_LAZOSKETCHDATA = _descriptor.Descriptor(
  name='LazoSketchData',
  full_name='lazo_index.LazoSketchData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='number_permutations', full_name='lazo_index.LazoSketchData.number_permutations', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hash_values', full_name='lazo_index.LazoSketchData.hash_values', index=1,
      number=2, type=18, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cardinality', full_name='lazo_index.LazoSketchData.cardinality', index=2,
      number=3, type=18, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=279,
  serialized_end=366,
)


_LAZOSKETCHDATALIST = _descriptor.Descriptor(
  name='LazoSketchDataList',
  full_name='lazo_index.LazoSketchDataList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='lazo_sketch_data', full_name='lazo_index.LazoSketchDataList.lazo_sketch_data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=368,
  serialized_end=442,
)


_DATASET = _descriptor.Descriptor(
  name='Dataset',
  full_name='lazo_index.Dataset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dataset_id', full_name='lazo_index.Dataset.dataset_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='column_names', full_name='lazo_index.Dataset.column_names', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=444,
  serialized_end=495,
)


_ACK = _descriptor.Descriptor(
  name='Ack',
  full_name='lazo_index.Ack',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ack', full_name='lazo_index.Ack.ack', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=497,
  serialized_end=515,
)


_VALUE = _descriptor.Descriptor(
  name='Value',
  full_name='lazo_index.Value',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='lazo_index.Value.value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=517,
  serialized_end=539,
)


_LAZOQUERYRESULTS = _descriptor.Descriptor(
  name='LazoQueryResults',
  full_name='lazo_index.LazoQueryResults',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query_results', full_name='lazo_index.LazoQueryResults.query_results', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=541,
  serialized_end=611,
)


_LAZOQUERYRESULT = _descriptor.Descriptor(
  name='LazoQueryResult',
  full_name='lazo_index.LazoQueryResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='column', full_name='lazo_index.LazoQueryResult.column', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_threshold', full_name='lazo_index.LazoQueryResult.max_threshold', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=613,
  serialized_end=699,
)


_LAZOQUERYRESULTSLIST = _descriptor.Descriptor(
  name='LazoQueryResultsList',
  full_name='lazo_index.LazoQueryResultsList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='column_query_results', full_name='lazo_index.LazoQueryResultsList.column_query_results', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=701,
  serialized_end=783,
)

_COLUMNVALUES.fields_by_name['column_identifier'].message_type = _COLUMNIDENTIFIER
_DATAPATH.fields_by_name['column_identifiers'].message_type = _COLUMNIDENTIFIER
_LAZOSKETCHDATALIST.fields_by_name['lazo_sketch_data'].message_type = _LAZOSKETCHDATA
_LAZOQUERYRESULTS.fields_by_name['query_results'].message_type = _LAZOQUERYRESULT
_LAZOQUERYRESULT.fields_by_name['column'].message_type = _COLUMNIDENTIFIER
_LAZOQUERYRESULTSLIST.fields_by_name['column_query_results'].message_type = _LAZOQUERYRESULTS
DESCRIPTOR.message_types_by_name['ColumnIdentifier'] = _COLUMNIDENTIFIER
DESCRIPTOR.message_types_by_name['ColumnValues'] = _COLUMNVALUES
DESCRIPTOR.message_types_by_name['DataPath'] = _DATAPATH
DESCRIPTOR.message_types_by_name['LazoSketchData'] = _LAZOSKETCHDATA
DESCRIPTOR.message_types_by_name['LazoSketchDataList'] = _LAZOSKETCHDATALIST
DESCRIPTOR.message_types_by_name['Dataset'] = _DATASET
DESCRIPTOR.message_types_by_name['Ack'] = _ACK
DESCRIPTOR.message_types_by_name['Value'] = _VALUE
DESCRIPTOR.message_types_by_name['LazoQueryResults'] = _LAZOQUERYRESULTS
DESCRIPTOR.message_types_by_name['LazoQueryResult'] = _LAZOQUERYRESULT
DESCRIPTOR.message_types_by_name['LazoQueryResultsList'] = _LAZOQUERYRESULTSLIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ColumnIdentifier = _reflection.GeneratedProtocolMessageType('ColumnIdentifier', (_message.Message,), {
  'DESCRIPTOR' : _COLUMNIDENTIFIER,
  '__module__' : 'lazo_index_pb2'
  # @@protoc_insertion_point(class_scope:lazo_index.ColumnIdentifier)
  })
_sym_db.RegisterMessage(ColumnIdentifier)

ColumnValues = _reflection.GeneratedProtocolMessageType('ColumnValues', (_message.Message,), {
  'DESCRIPTOR' : _COLUMNVALUES,
  '__module__' : 'lazo_index_pb2'
  # @@protoc_insertion_point(class_scope:lazo_index.ColumnValues)
  })
_sym_db.RegisterMessage(ColumnValues)

DataPath = _reflection.GeneratedProtocolMessageType('DataPath', (_message.Message,), {
  'DESCRIPTOR' : _DATAPATH,
  '__module__' : 'lazo_index_pb2'
  # @@protoc_insertion_point(class_scope:lazo_index.DataPath)
  })
_sym_db.RegisterMessage(DataPath)

LazoSketchData = _reflection.GeneratedProtocolMessageType('LazoSketchData', (_message.Message,), {
  'DESCRIPTOR' : _LAZOSKETCHDATA,
  '__module__' : 'lazo_index_pb2'
  # @@protoc_insertion_point(class_scope:lazo_index.LazoSketchData)
  })
_sym_db.RegisterMessage(LazoSketchData)

LazoSketchDataList = _reflection.GeneratedProtocolMessageType('LazoSketchDataList', (_message.Message,), {
  'DESCRIPTOR' : _LAZOSKETCHDATALIST,
  '__module__' : 'lazo_index_pb2'
  # @@protoc_insertion_point(class_scope:lazo_index.LazoSketchDataList)
  })
_sym_db.RegisterMessage(LazoSketchDataList)

Dataset = _reflection.GeneratedProtocolMessageType('Dataset', (_message.Message,), {
  'DESCRIPTOR' : _DATASET,
  '__module__' : 'lazo_index_pb2'
  # @@protoc_insertion_point(class_scope:lazo_index.Dataset)
  })
_sym_db.RegisterMessage(Dataset)

Ack = _reflection.GeneratedProtocolMessageType('Ack', (_message.Message,), {
  'DESCRIPTOR' : _ACK,
  '__module__' : 'lazo_index_pb2'
  # @@protoc_insertion_point(class_scope:lazo_index.Ack)
  })
_sym_db.RegisterMessage(Ack)

Value = _reflection.GeneratedProtocolMessageType('Value', (_message.Message,), {
  'DESCRIPTOR' : _VALUE,
  '__module__' : 'lazo_index_pb2'
  # @@protoc_insertion_point(class_scope:lazo_index.Value)
  })
_sym_db.RegisterMessage(Value)

LazoQueryResults = _reflection.GeneratedProtocolMessageType('LazoQueryResults', (_message.Message,), {
  'DESCRIPTOR' : _LAZOQUERYRESULTS,
  '__module__' : 'lazo_index_pb2'
  # @@protoc_insertion_point(class_scope:lazo_index.LazoQueryResults)
  })
_sym_db.RegisterMessage(LazoQueryResults)

LazoQueryResult = _reflection.GeneratedProtocolMessageType('LazoQueryResult', (_message.Message,), {
  'DESCRIPTOR' : _LAZOQUERYRESULT,
  '__module__' : 'lazo_index_pb2'
  # @@protoc_insertion_point(class_scope:lazo_index.LazoQueryResult)
  })
_sym_db.RegisterMessage(LazoQueryResult)

LazoQueryResultsList = _reflection.GeneratedProtocolMessageType('LazoQueryResultsList', (_message.Message,), {
  'DESCRIPTOR' : _LAZOQUERYRESULTSLIST,
  '__module__' : 'lazo_index_pb2'
  # @@protoc_insertion_point(class_scope:lazo_index.LazoQueryResultsList)
  })
_sym_db.RegisterMessage(LazoQueryResultsList)


DESCRIPTOR._options = None

_LAZOINDEX = _descriptor.ServiceDescriptor(
  name='LazoIndex',
  full_name='lazo_index.LazoIndex',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=786,
  serialized_end=1387,
  methods=[
  _descriptor.MethodDescriptor(
    name='IndexData',
    full_name='lazo_index.LazoIndex.IndexData',
    index=0,
    containing_service=None,
    input_type=_COLUMNVALUES,
    output_type=_LAZOSKETCHDATA,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='IndexDataPath',
    full_name='lazo_index.LazoIndex.IndexDataPath',
    index=1,
    containing_service=None,
    input_type=_DATAPATH,
    output_type=_LAZOSKETCHDATALIST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetLazoSketchFromData',
    full_name='lazo_index.LazoIndex.GetLazoSketchFromData',
    index=2,
    containing_service=None,
    input_type=_COLUMNVALUES,
    output_type=_LAZOSKETCHDATA,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetLazoSketchFromDataPath',
    full_name='lazo_index.LazoIndex.GetLazoSketchFromDataPath',
    index=3,
    containing_service=None,
    input_type=_DATAPATH,
    output_type=_LAZOSKETCHDATALIST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RemoveSketches',
    full_name='lazo_index.LazoIndex.RemoveSketches',
    index=4,
    containing_service=None,
    input_type=_DATASET,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='QueryData',
    full_name='lazo_index.LazoIndex.QueryData',
    index=5,
    containing_service=None,
    input_type=_VALUE,
    output_type=_LAZOQUERYRESULTS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='QueryDataPath',
    full_name='lazo_index.LazoIndex.QueryDataPath',
    index=6,
    containing_service=None,
    input_type=_DATAPATH,
    output_type=_LAZOQUERYRESULTSLIST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='QueryLazoSketchData',
    full_name='lazo_index.LazoIndex.QueryLazoSketchData',
    index=7,
    containing_service=None,
    input_type=_LAZOSKETCHDATA,
    output_type=_LAZOQUERYRESULTS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_LAZOINDEX)

DESCRIPTOR.services_by_name['LazoIndex'] = _LAZOINDEX

# @@protoc_insertion_point(module_scope)
