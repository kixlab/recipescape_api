# Recipescape API

## Tagger API

### How to insert recipes to DB

Prepare DB and create `.env` file according to `env` in repo. `manage.py` and `wsgi.py` loads environment variables from `.env` 

0. Install dependencies
```commandline
pip install -r requirements.txt
```

1. Launch [Stanford CoreNLP Server](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html)
```commandline
docker run -p 9000:9000 --name coreNLP --rm -it motiz88/corenlp
```

2. Run insert script. Let's say that we want to put recipes for potato salad
```commandline
python manage.py import_recipe --json_dirs ./recipes/potato_salad --name potatosalad
```

3. Run cluster script. For dummy cluster,
```commandline
python manage.py make_cluster --title potatosalad_dummy --dishname potatosalad
```
Check out `recipe_api/management/commans/make_cluster.py` and `_dummy_cluster.py` for writing real clustering scripts

### Running locally
```commandline
python manage.py collectstatic
gunicorn -w 5 recipescape_api.wsgi
caddy
```

### Running using Docker

1. Restore DB
```commandline
docker-compose up -d db
cat ${DUMP_FILE} | docker exec -i ${CONTAINER_NAME} psql -Upostgres
```

2. Develop mode
```commandline
docker-compose up
```

3. ~~Production~~ Deploy mode
```commandline
docker-compose -f docker-compose.yml -f docker-compose.deploy.yml up
```

## Recipe API
[Quick swagger documentation](https://app.swaggerhub.com/apis/zxzl/recipescape/1.0.0)
