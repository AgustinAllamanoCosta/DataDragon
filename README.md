# DataDragon

### What is in this repo?

This repo contain the code to generate a groups of Node to simulate a Web3 Cloud Network with the ability to verify the content using ZK-STARKS Ziggy algoritmy and a groups of endpoints to genrate a data stream.

### How to run Nodes and Development proces

You have the docker-compose,yml file to run it use the command:

```bash
docker-compouse up
```

if you made some change in the API of the node you need to rebuild the docker image and then run the docker-compuse comando:

Build image locally:

```bash
./build_api.sh
```

Run nodes:

```bash
docker-compouse up
```

If you made change in the ZKP API or code, you need to re build the docker image as well:

Build image locally:

```bash
./build_zkp.sh
```

Run nodes:

```bash
docker-compouse up
```

### Publish images in to the Docker Repo

To publish each image yo need to run:

Base zkp:

```bash
docker push agustinallamano/zkp:latest
```

Node data-dagron:

```bash
docker push agustinallamano/data-dagron:latest
```
