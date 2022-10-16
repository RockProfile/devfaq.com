# Devfaq.com Development

This directory contains the relevant files to setup a working development environment.

to get up and running first install Docker, the easiest way to do this on a Windows machine is to install
[Docker Desktop](https://www.docker.com/products/docker-desktop/)

Once installed and started run the following command:

```shell
docker-compose up
```

## What still needs to be done

* Creation of a default superuser
* Using a proper webserver
* Pre-populate the database with data

## FAQ

### My changes Do Not Display

This is usually caused by the docker container not updating. One way to force would be to do the following:

```shell
docker image rm dev_web
docker-compose up
```
