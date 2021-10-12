ghz --insecure \
    -r 200 \
    -n 1000 \
    --proto ../grpc/examples/protos/helloworld.proto \
    --call helloworld.Greeter.SayHello \
    -d '{"name":"Joe"}' \
    0.0.0.0:50051
