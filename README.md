# NEWS OGC Services
A django application to consume WMS, WCS services offered by geoserver for Water Balance Models. 

## Environment 

Create a `.env` (consumed by dotenv) file at root of project containing your parameters: 

```
ALLOWED_HOSTS=*
DEBUG=True
SECRET_KEY=examplesecret
DB_HOST=localhost
DB_PORT=5432
DB_USER=myuser
DB_PASSWORD=mypassword
```

To setup up python environmnet: 

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Docker
There are two docker-compose setups available, development and production. The development configuration, `dokcer-compose.yml` 
simply runs the django web server. 

`docker-compose up -d`

The production configuration uses gunicorn as a webserver and nginx as a reverse proxy. 

`docker-compose -f docker-compose.prod.yml up -d`

For static files to function, you'll need to run `collectstatic` from within the webserver container.

```
docker exec -it news_ogc_web /bin/bash
python manage.py collectstatic
```