# Winnipeg Air Quality Django app

This an application that utilizes Django and City of Winnipeg's API

## Installation to run locally.
NOTE: The environment use is Linux, you can use WSL2 as well.

- After you clone the project you should cd in the project and initialized a python environment.
```bash
$ python3 -m venv env
```

- Then activate the environment
```bash
$ source env/bin/activate
```

- Install the requirements.txt, make sure you're in the directory where the requirements.txt is placed.
```bash
$ pip3 install -r requirements.txt
```

- Go in the project folder
```bash
$ cd wpgair
```

- Run the application
```
$ python3 manage.py runserver
```

## Running with Docker

You could run this with Docker, make sure Docker is installed.

- After cloning the repository, you could straight up build the docker file. You could change the name of the image (wpgair) to your liking.
```bash
$ sudo docker build -t wpgair -f Dockerfile .
```

- Run the Imaged built, You could change the port 8083 to your liking.
```bash
$ sudo docker run -p 8083:8000 wpgair
```

- Access the site using localhost:8083 or if you changed the port then replace 8083