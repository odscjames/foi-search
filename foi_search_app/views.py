from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from foi_search  import settings
import json

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
        },
        "aggs": {
            "source_id": {
                "terms": {"field": "source_id"}
            }
        },
        "size": settings.SEARCH_PAGE_RESULTS_PER_PAGE
    }

    es = Elasticsearch()
    res = es.search(index=settings.ELASTICSEARCH_INDEX_READ, body=elastic_query)

    context = {
        'stats_by_source': [],
        'search_query': search_query,
        'results': []
    }
    for hit in res['hits']['hits']:
        item = hit['_source']
        item['id'] = hit['_id']
        context['results'].append(item)
    for data in res['aggregations']['source_id']['buckets']:
        context['stats_by_source'].append({
            'key': data['key'],
            'doc_count': data['doc_count'],
        })

    return render(request, 'foi_search_app/search.html', context)


def view(request, data_id):

    es = Elasticsearch()
    res = es.get(index=settings.ELASTICSEARCH_INDEX_READ, id=data_id)

    context = {
        'result': res['_source']
    }

    return render(request, 'foi_search_app/view.html', context)

def stats(request):

    elastic_query = {
        "aggs": {
            "source_id": {
                "terms": {"field": "source_id"}
            }
        }
    }

    es = Elasticsearch()
    res = es.search(index=settings.ELASTICSEARCH_INDEX_READ, body=elastic_query)

    context = {
        'stats_by_source': []
    }
    for data in res['aggregations']['source_id']['buckets']:
        context['stats_by_source'].append({
            'key': data['key'],
            'doc_count': data['doc_count'],
        })

    return render(request, 'foi_search_app/stats.html', context)