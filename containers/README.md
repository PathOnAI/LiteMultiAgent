# Building your Lite Multi Agent app using Docker

Following these steps to build the docker image of an isolated setup environment.

## Step 1: Install Docker
Refer to the [official Docker instructions](https://docs.docker.com/get-docker/) to download docker application and set up a [docker hub](https://hub.docker.com) account.

## Step 2: Build a Docker Image
Go to the project folder
```bash
cd LiteMultiAgent
```

and build the docker image
```bash
docker build -t lite-multi-agent-img-base -f containers/Dockerfile .
```

## Step 3: Run the Docker Container
Once the image is built, you can run a container using the following command:
```bash
docker run -d --name lite-multi-agent-container-base lite-multi-agent-img-base
```

If you want to run the container and mount a directory from your local machine so that changes can be saved locally, you can use the -v option:
```bash
docker run -d --name lite-multi-agent-container-base -v /Users/yourusername/my-project/LiteMultiAgent:/app lite-multi-agent-img-base
```

## Step 4: Access the Container
```bash
docker exec -it lite-multi-agent-container-base /bin/bash
```

You can use ```docker stop``` or ```docker kill``` command to terminate the container. 
