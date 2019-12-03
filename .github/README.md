# SFDS Accela microservice.py [![CircleCI](https://badgen.net/circleci/github/SFDigitalServices/accela-microservice-py/master)](https://circleci.com/gh/SFDigitalServices/accela-microservice-py) [![Coverage Status](https://coveralls.io/repos/github/SFDigitalServices/accela-microservice-py/badge.svg?branch=master)](https://coveralls.io/github/SFDigitalServices/accela-microservice-py?branch=master)

### Sample Usage
Install Pipenv (if needed)
> $ pip install --user pipenv

Install included packages
> $ pipenv install

Start WSGI Server
> (accela-microservice-py)$ pipenv run gunicorn 'service.microservice:start_service()'

Open with cURL or web browser  
> Get Records: Gets the requested Accela record(s) via IDs.

> (accela-microservice-py)$ curl http://127.0.0.1:8000/records/{ids} 

> Create Record: Creates a new, full record in Accela

> (accela-microservice-py) $ curl -X POST 'http://127.0.0.1:8000/records?fields=customId,id' -d '{"type":{"id":"Planning-Project-Project-PRJ"}, "name": "Accela Test Example", "description": "Example Testing of Accela API"}'
 