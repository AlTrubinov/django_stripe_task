Django_stripe_task
-------------

Installation
-------------

1. Clone repo
2. Open project folder in terminal
3. Check that docker and docker-compose are installed:
``` bash
$ docker -v
$ docker-compose -v
```
4. Input next commands in terminal:
``` bash
$ sudo docker-compose up —build
$ sudo docker-compose run web python3 manage.py migrate
$ sudo docker-compose run web python3 manage.py createsuperuser
$ sudo docker-compose up
``` 