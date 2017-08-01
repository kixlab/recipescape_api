# Recipescape API

## Tagger API

### How to insert recipes to DB

Prepare DB and create `.env` file according to `env` in repo. `manage.py` loads environment variables from `.env` 

0. Install dependencies
```commandline
pip install -r requirements.txt
```

1. Launch [Stanford CoreNLP Server](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html)
```commandline
docker run -p 9000:9000 --name coreNLP --rm -i -t motiz88/corenlp
```

2. Run insert script. Let's say that we want to put recipes for potato salad
```commandline
python manage.py import_recipe --json_dirs ./recipes/potato_salad --name potato_salad
```