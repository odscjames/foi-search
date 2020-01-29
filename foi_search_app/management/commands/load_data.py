from django.core.management.base import BaseCommand, CommandError
import json
import hashlib
from elasticsearch import Elasticsearch
from foi_search import settings

class Command(BaseCommand):
    help = 'Loads Data Into Elasticsearch'

    def add_arguments(self, parser):
        parser.add_argument('uri')
        parser.add_argument('sourceid')

    def handle(self, *args, **options):

        es = Elasticsearch()
        es.indices.create(index=settings.ELASTICSEARCH_INDEX_WRITE, ignore=400, body={
            "mappings": {
                "properties": {
                    "question": {
                        "type": "text"
                    },
                    "link": {
                        "type": "keyword"
                    },
                    "source_id": {
                        "type": "keyword"
                    },
                    "source_title": {
                        "type": "keyword"
                    },
                    "source_link": {
                        "type": "keyword"
                    }
                }
            }
        })

        with open(options['uri']) as file:
            data = json.load(file)

        for item in data['data']:
            if 'id' not in item:
                item['id'] = hashlib.md5(item['link'].encode('utf-8')).hexdigest()

            es.index(
                index=settings.ELASTICSEARCH_INDEX_WRITE,
                id=options['sourceid'] + '-' + item['id'],
                body={
                    # The data
                    'question': item['question'],
                    'link': item['link'],
                    # The flattened information about the source
                    'source_id': options['sourceid'],
                    'source_title': data['title'],
                    'source_link': data['link'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded'))
