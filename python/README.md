# Extra information about these modules

## Applications
The important files are the services, which runs the gRPC server:
- message_service.py
- user_service.py

There are client applications here, but they are just for testing. For example:
- message_client.py
- user_service.py

## Protos

Create gRPC python files for user proto:

```shell
python3 -m  grpc_tools.protoc -I protos --python_out=./user --grpc_python_out=./user protos/user.proto
```
Notice all out arguments references at the directory where the command will generate the files.