import sys
sys.path.append('./')
from elasticsearch import NotFoundError

from config.config_es import INDEX_LAW, TYPE_DOCUMENT
from config.config_project import minimum_should_match_for_search
from constants.law_constant import DOCUMENT_TYPES, DEPARTMENT_TYPES, TOPIC_TYPES
from es_service.es_connection import elasticsearch_connection
from service.common.common import get_by_attribute_from_array_dict
from service.search_service.vblp_query_helper import get_source_default, get_sort_by_date_issued, get_sort_by_score, \
    get_filter_scope, get_condition_by_document_type, get_condition_by_department_type, get_condition_by_topic_type, \
    get_condition_should_by_departments, get_condition_should_by_topics
from service.search_service.vblp_searcher import search_title


def search_for_support(es, title, limit=5, _source=None, is_match_phrase=False, editor_setting=None):
    if (editor_setting.get('documentType') == get_by_attribute_from_array_dict(DOCUMENT_TYPES, 'name', 'Luật').get(
            'id')):
        # Luật

        filter_builder = []
        document_types_condition_should = []

        document_types_condition_should.append(get_condition_by_document_type("Luật"))
        # need update more document types

        document_types_condition = {
            "bool": {
                "should": [
                    document_types_condition_should
                ]
            }
        }

        if editor_setting.get('scopeId') == 1:
            filter_builder.append(get_filter_scope(scope='Toàn quốc'))

        department_types_condition = get_condition_should_by_departments(editor_setting.get('departmentIds'))

        topic_types_condition = get_condition_should_by_topics(editor_setting.get('topicIds'))

        if len(filter_builder) > 0:
            return search_title(es=es, title=title, limit=5, match_phrase=is_match_phrase, _source=get_source_default(),
                                editor_setting=editor_setting, minimum_should_match=minimum_should_match_for_search,
                                filter_builder=filter_builder, document_types_condition=document_types_condition,
                                department_types_condition=department_types_condition,
                                topic_types_condition=topic_types_condition)
    elif (editor_setting.get('documentType') == get_by_attribute_from_array_dict(DOCUMENT_TYPES, 'name',
                                                                                 'Nghị định').get(
        'id')):

        filter_builder = []
        document_types_condition_should = []

        document_types_condition_should.append(get_condition_by_document_type("Quyết định"))
        document_types_condition_should.append(get_condition_by_document_type("Nghị quyết"))
        document_types_condition_should.append(get_condition_by_document_type("Nghị định"))
        document_types_condition_should.append(get_condition_by_document_type("Thông tư liên tịch"))
        document_types_condition_should.append(get_condition_by_document_type("Luật"))
        document_types_condition_should.append(get_condition_by_document_type("Lệnh"))
        document_types_condition_should.append(get_condition_by_document_type("Pháp Lệnh"))
        document_types_condition_should.append(get_condition_by_document_type("Chỉ thị"))
        document_types_condition_should.append(get_condition_by_document_type("Nghị Quyết"))
        # need update more document types

        document_types_condition = {
            "bool": {
                "should": [
                    document_types_condition_should
                ]
            }
        }

        if editor_setting.get('scopeId') == 1:
            filter_builder.append(get_filter_scope(scope='Toàn quốc'))

        department_types_condition = get_condition_should_by_departments(editor_setting.get('departmentIds'))

        topic_types_condition = get_condition_should_by_topics(editor_setting.get('topicIds'))

        if len(filter_builder) > 0:
            return search_title(es=es, title=title, limit=5, match_phrase=is_match_phrase, _source=get_source_default(),
                                editor_setting=editor_setting, minimum_should_match=minimum_should_match_for_search,
                                filter_builder=filter_builder, document_types_condition=document_types_condition,
                                department_types_condition=department_types_condition,
                                topic_types_condition=topic_types_condition)
    else:
        filter_builder = []
        document_types_condition_should = []

        document_types_condition_should.append(get_condition_by_document_type("Quyết định"))
        document_types_condition_should.append(get_condition_by_document_type("Thông tư"))
        document_types_condition_should.append(get_condition_by_document_type("Nghị quyết"))
        document_types_condition_should.append(get_condition_by_document_type("Nghị định"))
        document_types_condition_should.append(get_condition_by_document_type("Thông tư liên tịch"))
        document_types_condition_should.append(get_condition_by_document_type("Luật"))
        document_types_condition_should.append(get_condition_by_document_type("Lệnh"))
        document_types_condition_should.append(get_condition_by_document_type("Pháp Lệnh"))
        document_types_condition_should.append(get_condition_by_document_type("Chỉ thị"))
        document_types_condition_should.append(get_condition_by_document_type("Nghị Quyết"))
        # need update more document types

        document_types_condition = {
            "bool": {
                "should": [
                    document_types_condition_should
                ]
            }
        }

        if editor_setting.get('scopeId') == 1:
            filter_builder.append(get_filter_scope(scope='Toàn quốc'))

        department_types_condition = get_condition_should_by_departments(editor_setting.get('departmentIds'))

        topic_types_condition = get_condition_should_by_topics(editor_setting.get('topicIds'))

        if len(filter_builder) > 0:
            return search_title(es=es, title=title, limit=5, match_phrase=is_match_phrase, _source=get_source_default(),
                                editor_setting=editor_setting, minimum_should_match=minimum_should_match_for_search,
                                filter_builder=filter_builder, document_types_condition=document_types_condition,
                                department_types_condition=department_types_condition,
                                topic_types_condition=topic_types_condition)


# search_title()

def example():
    es = elasticsearch_connection
    # search_content(es, content='BHXH', match_phrase=False)
    # search_title(es, title='BHXH', match_phrase=False)
    # get_by_id(es, '75724')
    # get_by_id(es, 'ds')
    search_for_support(es, title='chất thải công nghiệp', limit=10,
                       editor_setting={'documentType': 4, 'title': '', 'departmentIds': [], 'topicIds': [],
                                       'scopeId': 1})

# example()