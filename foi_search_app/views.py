from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from foi_search  import settings
import json
from math import ceil

def index(request):
    return render(request, 'foi_search_app/index.html', {})


def search(request):

    search_query = request.GET.get('search')
    page_number = int(request.GET.get('page', 1))

    elastic_query = {
        # For paging purposes, we are just going to be lazy and say we always want all hits.
        "track_total_hits": True,
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
        "size": settings.SEARCH_PAGE_RESULTS_PER_PAGE,
        "from": ((page_number - 1) * settings.SEARCH_PAGE_RESULTS_PER_PAGE)
    }

    es = Elasticsearch()
    res = es.search(index=settings.ELASTICSEARCH_INDEX_READ, body=elastic_query)

    context = {
        'stats_by_source': [],
        'search_query': search_query,
        'page_number': page_number,
        'results': [],
        'total_results_count': res['hits']['total']['value'],
        'total_pages': ceil(res['hits']['total']['value'] / settings.SEARCH_PAGE_RESULTS_PER_PAGE),
        'show_page_prev': (True if page_number > 1 else False),
    }
    context['show_page_next'] = (True if page_number < context['total_pages'] else False)
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