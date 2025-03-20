import blackboxprotobuf

with open('_tmp_bak','rb') as f:
    data = f.read()

deserial_data,message_type = blackboxprotobuf.protobuf_to_json(data)
print(deserial_data)
print(message_type)

