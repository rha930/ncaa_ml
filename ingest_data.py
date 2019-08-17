from elasticsearch import helpers, Elasticsearch
import csv
import yaml
es = Elasticsearch()

with open('ncaa_config.yml', 'r') as f:
    config = yaml.load(f)
DATA_DIR = config['DATA_DIR']
with open(f'{DATA_DIR}/kenpom_data.csv') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='kenpom_data', doc_type='allyears')
    

