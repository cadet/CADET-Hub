# Cadethub setup for docker swarm

## Preparation (according to https://docs.docker.com/engine/swarm/stack-deploy/)

1. create a local docker registry

```
docker service create --name registry --publish published=5000,target=5000 registry:2
```

2. Check its status with docker service ls:

```
docker service ls
```

3. Check that it’s working with `curl`:

```
curl http://localhost:5000/v2/
```

4. push all the images to the registry

```
docker-compose push
```

## Start the stack

```
docker stack deploy --compose-file docker-compose_swarm.yml cadethub
```