from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch


def index(request):
    return render(request, 'foi_search_app/index.html', {})


def search(request):

    search_query = request.GET.get('search')

    elastic_query = {
        "query": {
            "simple_query_string": {
                "query": search_query,
                "fields": ["question"],
                "default_operator": "and"
            }
        }
    }

    es = Elasticsearch()
    res = es.search(index="foisearch", body=elastic_query)

    context = {
        'search_query': search_query,
        'results': []
    }
    for hit in res['hits']['hits']:
        context['results'].append(hit['_source'])


    return render(request, 'foi_search_app/search.html', context)
