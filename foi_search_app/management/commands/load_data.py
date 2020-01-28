from django.core.management.base import BaseCommand, CommandError
import json
import hashlib
from elasticsearch import Elasticsearch


class Command(BaseCommand):
    help = 'Loads Data Into Elasticsearch'

    def add_arguments(self, parser):
        parser.add_argument('uri')
        parser.add_argument('sourceid')

    def handle(self, *args, **options):

        es = Elasticsearch()
        es.indices.create(index='foisearch', ignore=400)

        with open(options['uri']) as file:
            data = json.load(file)

        for item in data['data']:
            if 'id' not in item:
                item['id'] = hashlib.md5(item['link'].encode('utf-8')).hexdigest()

            es.index(
                index="foisearch",
                id=options['sourceid'] + '-' + item['id'],
                body={
                    'question': item['question'],
                    'link': item['link'],
                    'source_title': data['title'],
                    'source_link': data['link'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded'))
