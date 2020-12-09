# ApiDockerBasicCrud

This is a basic tutorial to setup the project

## Dev 
The following instructions are used to start the development environment.

`$ pip install -r requirements-dev.txt`

`./manage.py makemigrations`

`./manage.py migrate`

`./manage.py createsuperuser`

`./manage.py runserver`

### Run tests
Here the platform tests will be performed.
`./manage.py test`

## Production

First make a copy of the environment configuration file and complete with your own.

`cp .env.example .env`

Now, edit your conf. Don't forget to change the production and debug flags to True.

`vim .env`


Run docker compose.

`docker-compose up --build -d`

Now, aply migrations, statics and superuser.

`docker-compose run web python3 manage.py migrate`

`docker-compose run web python3 manage.py collectstatic`

`docker-compose run web python3 manage.py createsuperuser`

You can now access the configured ip. 