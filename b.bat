set VER=v1.0.3.1
docker build . -t srregistry88.azurecr.io/task-operator:%VER%
docker push srregistry88.azurecr.io/task-operator:%VER%

