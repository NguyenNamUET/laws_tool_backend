import sys
sys.path.append('./')
from elasticsearch import NotFoundError
from apps.search.helper.transform_format import dictionary_to_array
from apps.search.config.config_es import INDEX_LAW, TYPE_DOCUMENT
# from apps.search.es_service.es_connection import elasticsearch_connection
from apps.search.service.search_service.vblp_query_helper import get_source_default, get_sort_by_date_issued, get_sort_by_score, \
    get_filter_scope, get_aggregations_of_fields, range_issued_date, get_sort_by_enforced_date
from datetime import date


def search_match_all(es, limit=5, start=0, sort_by=None, document_field = None, document_types_condition=None):
    sort = get_sort_by_score()
    if sort_by == 1:
        sort = get_sort_by_date_issued()
    elif sort_by == 2:
        sort = get_sort_by_enforced_date()
    _source = get_source_default()
    query = {
        "track_total_hits": True,
        "query": {
            "bool": {
              "must": [
                {
                  "match_all": {}
                }
              ]                                                                                                                                                                                                                }                                                                                                                                                                                                              },
        "aggs": get_aggregations_of_fields(),
        "sort": sort,
        "_source": _source,
        "from": start,
        "size": limit
    }
    if document_types_condition is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.document_type' : document_types_condition }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if document_field is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.document_field' : document_field }}]
        query.get('query').get('bool').update({'must': new_must_query})
        
    print(f'querySearchContent: {query}')
    res = es.search(index=INDEX_LAW, doc_type=TYPE_DOCUMENT, body=query)
    print("Got %d Hits:" % res['hits']['total']['value'])
    # print(res)
    if res['hits']['total']['value'] == 0:
        return {}
    return res


def get_by_id(es, id):
    try:
        res = es.get(index=INDEX_LAW, doc_type=TYPE_DOCUMENT, id=id)
        return res['_source']
    except NotFoundError:
        print('not found')
        return {}


def search_content(es, content, time_range = None, match_phrase=False, minimum_should_match = '50',
                   limit=5, start=0, _source=None, doc_status = None, document_types_condition=None, document_field = None, issuing_body = None, signer = None, sorted_by=1 ,  editor_setting=None):
    keyword = content
    query = {}
    if _source is None:
        _source = get_source_default()
    if time_range is None:
        gte = "1940-01-01"
        lte = date.today().strftime("%Y-%m-%d")
    else:
        gte = time_range['gte']
        lte = time_range['lte']

    if sorted_by == 1:
        sort = get_sort_by_score()
    elif sorted_by == 2:
        sort = get_sort_by_date_issued()
    else:
        sort = get_sort_by_date_issued(desc=False)

    print(match_phrase)
    if match_phrase:
        query = {
            "track_total_hits": True,
            "query": {
                "bool": {
                    "should" : [],
                    "must": [
                        {
                            "bool" : {
                                "should" : [
                                    {
                                        "match_phrase": {
                                            "attribute.official_number": keyword
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "title": keyword
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "attribute.document_info": keyword
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "full_text": keyword
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "range": range_issued_date(gte, lte)
                        }

                    ]
                }
            },
            "aggs": get_aggregations_of_fields(),
            "sort": sort,
            "_source": _source,
            'from': start,
            "size": limit
        }
    else:
        query = {
            "track_total_hits": True,
            "query": {
                "bool": {
                    "should" : [],
                    "must":[
                        {
                        "bool" : {
                                "should" : [
                                    {
                                        "match": {
                                            "attribute.official_number": {
                                                "query": keyword,
                                                # "minimum_should_match": minimum_should_match + '%'
                                            }
                                        }
                                    },
                                    {
                                        "match": {
                                            "title": {
                                                "query": keyword,
                                                # "minimum_should_match": minimum_should_match + '%'
                                            }
                                        }
                                    },
                                    {
                                        "match": {
                                            "attribute.document_info": {
                                                "query": keyword,
                                                # "minimum_should_match": minimum_should_match + '%'
                                            }
                                        }
                                    },
                                    {
                                        "match": {
                                            "full_text": {
                                                "query": keyword,
                                                # "minimum_should_match": minimum_should_match + '%'
                                            }
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "range": range_issued_date(gte, lte)
                        }
                    ]
                }
            },
            "aggs": get_aggregations_of_fields(),
            "sort": sort,
            "_source": _source,
            'from': start,
            "size": limit
        }

    # filter_builder = []
    # if 'scopeId' in editor_setting:
    #     if editor_setting.get('scopeId') == 1:
    #         filter_builder.append(get_filter_scope(scope='Toàn quốc'))
    # if len(filter_builder) > 0:
    #     query.get('query').get('bool').update({'filter': filter_builder})

    if document_types_condition is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.document_type' : document_types_condition }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if doc_status is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.document_info' : doc_status }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if issuing_body is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.issuing_body/office/signer' : issuing_body }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if signer is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.issuing_body/office/signer' : signer }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if document_field is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.document_field' : document_field }}]
        query.get('query').get('bool').update({'must': new_must_query})

    print(f'querySearchContent: {query}')
    res = es.search(index=INDEX_LAW, doc_type=TYPE_DOCUMENT, body=query)
    print("Got %d Hits:" % res['hits']['total']['value'])
    # print(res['aggregations'])
    if res['hits']['total']['value'] == 0:
        return {}
    for hit in res['hits']['hits']:
        print(hit["_source"])
    return res


def search_title(es, title, limit=5, start = 0, time_range = None,  match_phrase=False, _source=None,minimum_should_match="50",
                 doc_status = None, document_types_condition=None, document_field = None, issuing_body = None, signer = None, sorted_by=1 , editor_setting=None):
    keyword = title
    query = {}

    if _source is None:
        _source = get_source_default()
    if time_range is None:
        gte = "1940-01-01"
        lte = date.today().strftime("%Y-%m-%d")
    else:
        gte = time_range['gte']
        lte = time_range['lte']

    if sorted_by == 1:
        sort = get_sort_by_score()
    elif sorted_by == 2:
        sort = get_sort_by_date_issued()
    else:
        sort = get_sort_by_date_issued(desc=False)

    if match_phrase:
        query = {
            "track_total_hits": True,
            "query": {
                "bool": {
                    "should": [

                    ],
                    "must": [
                        {
                            "bool": {
                                "should": [
                                    {
                                        "match_phrase": {
                                            "title": keyword
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "attribute.document_info": keyword
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "range": range_issued_date(gte, lte)
                        }
                    ],
                    "must_not": []
                }
            },
            "aggs": get_aggregations_of_fields(),
            "sort": sort,
            "_source": _source,
            'from': start,
            "size": limit
        }
    else:
        query = {
            "track_total_hits": True,
            "query": {
                "bool": {
                    "should": [

                    ],
                    "must": [
                        {
                            "bool": {
                                "should": [
                                    {
                                        "match":{
                                            "title": {
                                                "query": keyword,
                                                "minimum_should_match": minimum_should_match + '%'
                                            }
                                        }
                                    },
                                    {
                                        "match": {
                                            "attribute.document_info": {
                                                "query": keyword,
                                                "minimum_should_match": minimum_should_match + '%'
                                            }

                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "range": range_issued_date(gte, lte)
                        }
                    ],
                    "must_not": []
                }
            },
            "aggs": get_aggregations_of_fields(),
            "sort": sort,
            "_source": _source,
            'from': start,
            "size": limit
        }

    if document_types_condition is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.document_type' : document_types_condition }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if doc_status is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.document_info' : doc_status }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if issuing_body is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.issuing_body/office/signer' : issuing_body }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if signer is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.issuing_body/office/signer' : signer }}]
        query.get('query').get('bool').update({'must':  new_must_query})

    if document_field is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.document_field' : document_field }}]
        query.get('query').get('bool').update({'must': new_must_query})

    # if filter_builder is not None and len(filter_builder) > 0:
    #     query.get('query').get('bool').update({'filter': filter_builder})

    print(f'query: {query}')
    res = es.search(index=INDEX_LAW, doc_type=TYPE_DOCUMENT, body=query)
#    print("Got %d Hits:" % res['hits']['total']['value'])
    # print(res['aggregations'])
    if res['hits']['total']['value'] == 0:
        return {}
    #for hit in res['hits']['hits']:
    #    print(hit["_source"])
    #    print ("-------------------------------------------------")
    #    pass
    print(f'result: {res}')
    return res


def search_codes(es, code,time_range = None, limit=5, start=0,  match_phrase=False, _source=None,
                 doc_status = None, document_types_condition=None, document_field = None, issuing_body = None, signer = None, sorted_by=1, editor_setting=None):
    query = {}

    if _source is None:
        _source = get_source_default()
    should_query = []
    if time_range is None:
        gte = "1940-01-01"
        lte = date.today().strftime("%Y-%m-%d")
    else:
        gte = time_range['gte']
        lte = time_range['lte']

    if sorted_by == 1:
        sort = get_sort_by_score()
    elif sorted_by == 2:
        sort = get_sort_by_date_issued()
    else:
        sort = get_sort_by_date_issued(desc=False)

    if match_phrase:
        query = {
            "track_total_hits": True,
            "query": {
                "bool": {
                    "should" : [],
                    "must":[ {
                        "match_phrase": {
                                "attribute.official_number": code
                            }
                        },
                        {
                            "range": range_issued_date(gte, lte)
                        }

                    ]
                }
            },
            "aggs": get_aggregations_of_fields(),
            "sort": sort,
            "_source": _source,
            'from': start,
            "size": limit
        }
    else:
        query = {
            "track_total_hits": True,
            "query": {
                "bool": {
                    "should" : [],
                    "must":[ {
                        "match": {
                                "attribute.official_number": code
                            }
                        },
                        {
                            "range": range_issued_date(gte, lte)
                        }

                    ]
                }
            },
            "aggs": get_aggregations_of_fields(),
            "sort": sort,
            "_source": _source,
            'from': start,
            "size": limit
        }

    if document_types_condition is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.document_type' : document_types_condition }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if doc_status is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.document_info' : doc_status }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if issuing_body is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.issuing_body/office/signer' : issuing_body }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if signer is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.issuing_body/office/signer' : signer }}]
        query.get('query').get('bool').update({'must': new_must_query})

    if document_field is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{ 'match_phrase' : { 'attribute.document_field' : document_field }}]
        query.get('query').get('bool').update({'must': new_must_query})

    res = es.search(index=INDEX_LAW, doc_type=TYPE_DOCUMENT, body=query)
    print("Got %d Hits:" % res['hits']['total']['value'])
    if res['hits']['total']['value'] == 0:
        return {}
    for hit in res['hits']['hits']:
        print(hit["_source"])
    return res


def recommend_search(es,document_fields, limit=5,start=0, _source=None,
                     doc_status=None, time_range=None, sorted_by=1):
    query = {}

    if _source is None:
        _source = get_source_default()

    if time_range is None:
        gte = "1940-01-01"
        lte = date.today().strftime("%Y-%m-%d")
    else:
        gte = time_range['gte']
        lte = time_range['lte']

    if sorted_by == 1:
        sort = get_sort_by_score()
    elif sorted_by == 2:
        sort = get_sort_by_date_issued()
    else:
        sort = get_sort_by_date_issued(desc=False)

    document_fields_query = []
    for field in document_fields:
        field_query = {'match_phrase': {'attribute.document_field': {'query': field}}}
        document_fields_query.append(field_query)

    query = {
        "track_total_hits": True,
        "query": {
            "bool": {
                "should" : [],
                "must": [
                    {
                        "bool" : {
                            "should" : document_fields_query
                        }
                    },
                    {
                        "range": range_issued_date(gte, lte)
                    }
                ]
            }
        },
        "aggs": get_aggregations_of_fields(),
        "sort": sort,
        "_source": _source,
        'from': start,
        "size": limit
    }
    
    if doc_status is not None:
        must_query = dictionary_to_array(query.get('query').get('bool')['must'])
        new_must_query = must_query + [{'match_phrase': {'attribute.document_info': doc_status }}]
        query.get('query').get('bool').update({'must': new_must_query})

    print("recommend query: ", query)
    res = es.search(index=INDEX_LAW, doc_type=TYPE_DOCUMENT, body=query)
    print("Got %d Hits:" % res['hits']['total']['value'])
    if res['hits']['total']['value'] == 0:
        return {}
    for hit in res['hits']['hits']:
        print(hit["_source"])
    return res
  


def multifield_search(es, keyword, search_dict, time_range = None, limit = 5, start = 0,
                      minimum_should_match = "50", _source=None, keyword_match_phrase=False, sorted_by=1):
    #frontend post data
    #{'search':[field1__value1, field1__value2, field2__value1, field2__value2, ..., fieldM__valueN]
    #Backend process: {"field1":[value1, value2], "field2":[value1,value2],...}

    query = {}
    keyword_query = {}
    if keyword_match_phrase:
        keyword_query = {
                            "bool": {
                                    "should": [
                                        {
                                            "match_phrase": {
                                                "attribute.official_number": keyword
                                            }
                                        },
                                        {
                                            "match_phrase": {
                                                "title": keyword
                                            }
                                        },
                                        {
                                            "match_phrase": {
                                                "attribute.document_info": keyword
                                            }
                                        },
                                        {
                                            "match_phrase": {
                                                "full_text": keyword
                                            }
                                        }
                                    ]
                                }
                            }
    else:
        keyword_query = {
                            "bool": {
                                "should": [
                                    {
                                        "match":{
                                            "title": {
                                                "query": keyword,
                                                "minimum_should_match": minimum_should_match + '%'
                                            }
                                        }
                                    },
                                    {
                                        "match": {
                                            "attribute.document_info": {
                                                "query": keyword,
                                                "minimum_should_match": minimum_should_match + '%'
                                            }

                                        }
                                    }
                                ]
                            }
                        }
    


    if _source is None:
        _source = get_source_default()

    if time_range is None:
        gte = "1940-01-01"
        lte = date.today().strftime("%Y-%m-%d")
    else:
        gte = time_range['gte']
        lte = time_range['lte']

    if sorted_by == 1:
        sort = get_sort_by_score()
    elif sorted_by == 2:
        sort = get_sort_by_date_issued()
    else:
        sort = get_sort_by_date_issued(desc=False)


    if len(search_dict) == 1:
        match_phrase_query = []
        for field, values in search_dict.items():
            field_query__text = "attribute."+str(field)
            for value in values:
                match_field = {
                    "match_phrase": {
                        field_query__text: {
                            "query": value,
                        }
                    }
                }
                match_phrase_query.append(match_field)

        query = {
            "track_total_hits": True,
            "query": {
                "bool": {
                    "should" : [],
                    "must": [
                        {
                            "bool" : {
                                "should" : match_phrase_query
                            }
                        },
                        keyword_query
                    ]
                }
            },
            "aggs": get_aggregations_of_fields(),
            "sort": sort,
            "_source": _source,
            'from': start,
            "size": limit
        }

    else:
        match_phrase_must_query = []
        for field, values in search_dict.items():
            field_query__text = "attribute."+str(field)
            match_phrase_should_query = []
            for value in values:
                match_field = {
                    "match_phrase": {
                        field_query__text: {
                            "query": value,
                        }
                    }
                }
                match_phrase_should_query.append(match_field)

            one_field_query = {
                                "bool": {
                                    "should": match_phrase_should_query
                                }
                              }

            match_phrase_must_query.append(one_field_query)

        query = {
            "track_total_hits": True,
            "query": {
                "bool": {
                    "should": [],
                    "must": match_phrase_must_query+[keyword_query]
                }
            },
            "aggs": get_aggregations_of_fields(),
            "sort": sort,
            "_source": _source,
            'from': start,
            "size": limit
        }

    must_query = dictionary_to_array(query.get('query').get('bool')['must'])
    add_time_range_query = must_query+[{"range": range_issued_date(gte, lte)}]
    query.get('query').get('bool').update({'must': add_time_range_query})

    
    print("multi :", query)
    res = es.search(index=INDEX_LAW, doc_type=TYPE_DOCUMENT, body=query)
    print("Got %d Hits:" % res['hits']['total']['value'])
    if res['hits']['total']['value'] == 0:
        return {}

    return res



def example():
    es = elasticsearch_connection
    # search_content(es, content="35/2015/TT-NHNN", time_range={"gte" : "2010-01-01", "lte" : "2020-01-01"},  match_phrase=False,
    #                editor_setting={'documentType': 4, 'title': '', 'departmentIds': [], 'topicIds': [],
    #                                'scopeId': 1})
    # search_title(es, title='35/2015/TT-NHNN', doc_status="Hết hiệu lực", document_types_condition='Thông tư', issuing_body="Ngân hàng Nhà nước Việt Nam",
    #              signer='Nguyễn Phước Thanh', match_phrase=False, sorted_by=2)
    # get_by_id(es, '75724')
    # get_by_id(es, 'ds')
    search_codes(es,  '185/2007/NĐ-CP', time_range={"gte" : "2007-01-01", "lte" : "2020-01-01"}, match_phrase=True)

# example()

