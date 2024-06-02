# calculator-microservice

A Calculator implemented with microservices using synchronous communication

Building the Container Images with podman (macos/arm)

```
podman build -t calc-addition:latest --build-arg="APP_NAME=addition" .

podman build -t calc-multiplication:latest --build-arg="APP_NAME=multiplication" .

podman build -t calc-subtraction:latest --build-arg="APP_NAME=subtraction" .

podman build -t calc-division:latest --build-arg="APP_NAME=division" .
```

Buildind the images for Linux/Amd64:

```
podman build --platform=linux/amd64 -t calc-addition:latest --build-arg="APP_NAME=addition" .

podman build --platform=linux/amd64 -t calc-multiplication:latest --build-arg="APP_NAME=multiplication" .

podman build --platform=linux/amd64 -t calc-subtraction:latest --build-arg="APP_NAME=subtraction" .

podman build --platform=linux/amd64 -t calc-division:latest --build-arg="APP_NAME=division" .
```

Pushing the images to DockerHub;

```
podman push localhost/calc-addition:latest tinmancoding/calc-addition:latest

podman push localhost/calc-multiplication:latest tinmancoding/calc-multiplication:latest

podman push localhost/calc-subtraction:latest tinmancoding/calc-subtraction:latest

podman push localhost/calc-division:latest tinmancoding/calc-division:latest

```
