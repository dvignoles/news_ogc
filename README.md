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