from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views  import APIView
from apps.search.service.search_service.vblp_searcher import search_content, get_by_id, search_title, search_codes, search_match_all, multifield_search, recommend_search
from apps.search.es_service.es_connection import elasticsearch_connection
import ast
import json

class SearchMatchAll(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        #print(elasticsearch_connection.get(index="law_tech", doc_type="_doc", id=1))
        size = 5
        start = 0
        sorted_by = None
        document_type = None
        document_field = None
        request_data = request.data
        if 'size' in request_data:
            size = request_data['size']
        if 'from' in request_data:
            start = request_data['from']
        if 'sorted_by' in request_data:
            sorted_by = request_data['sorted_by']
        if 'document_type' in request_data:
            document_type = request_data['document_type']
        if 'document_field' in request_data:
            document_field = request_data['document_field']
        document = search_match_all(elasticsearch_connection, limit=size, start=start, sort_by=sorted_by, document_types_condition=document_type,
                                  document_field=document_field)
        return Response(document)


class GetById(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, id):
        try:
            print('prepare find', id)
            document = get_by_id(elasticsearch_connection, id)
            return Response(document)
        except:
            return Response({})


class SearchContent(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = {
            'content' : 'Bảo hiểm xã hội',
            'from' : 0,
            'size' : 5,
            'time_range' : None,
            'match_phrase' : False,
            'doc_status' : None,
            'document_types_condition' : None,
            'document_field': None,
            'issuing_body' : None,
            'signer' : None,
            'sorted_by' : 1,
            'editor_setting' : None
        }
        request_data = request.data
        for key, value in request_data.items():
            data[key] = value
        if data['time_range'] is not None:
            try:
                data['time_range'] = ast.literal_eval(data['time_range'])
            except:
                data['time_range'] = data['time_range']
        print (data)
        document = search_content(elasticsearch_connection, content=data['content'], time_range=data['time_range'],
                                  match_phrase=data['match_phrase'],
                                  start=data['from'],
                                  limit=data['size'], doc_status=data['doc_status'],
                                  document_types_condition=data['document_types_condition'],
                                  document_field=data['document_field'],
                                  issuing_body=data['issuing_body'],
                                  signer=data['signer'], sorted_by=data['sorted_by'],
                                  editor_setting=data['editor_setting'])
        return Response(document)


class SearchTitle(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = {
            'title' : 'Bảo hiểm xã hội',
            'from' : 0,
            'size' : 5,
            'time_range' : None,
            'match_phrase' : False,
            'doc_status' : None,
            'document_types_condition' : None,
            'document_field': None,
            'issuing_body' : None,
            'signer' : None,
            'sorted_by' : 1,
            'editor_setting' : None
        }
        request_data = request.data
        print("search title: ", request_data)
        for key, value in request_data.items():
            data[key] = value
        if data['time_range'] is not None:
            try:
                data['time_range'] = ast.literal_eval(data['time_range'])
            except:
                data['time_range'] = data['time_range']
        print (data)
        document = search_title(elasticsearch_connection, title=data['title'], time_range=data['time_range'],
                                  match_phrase=data['match_phrase'],
                                  start=data['from'],
                                  limit=data['size'], doc_status=data['doc_status'],
                                  document_types_condition=data['document_types_condition'],
                                  document_field=data['document_field'],
                                  issuing_body=data['issuing_body'],
                                  signer=data['signer'], sorted_by=data['sorted_by'],
                                  editor_setting=data['editor_setting'])
        return Response(document)


class SearchCodes(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = {
            'code' : '190/2007/NĐ-CP',
            'from' : 0,
            'size' : 5,
            'time_range' : None,
            'match_phrase' : False,
            'doc_status' : None,
            'document_types_condition' : None,
            'document_field': None,
            'issuing_body' : None,
            'signer' : None,
            'sorted_by' : 1,
            'editor_setting' : None
        }
        request_data = request.data
        for key, value in request_data.items():
            data[key] = value
        if data['time_range'] is not None:
            try:
                data['time_range'] = ast.literal_eval(data['time_range'])
            except:
                data['time_range'] = data['time_range']
        print (data)
        document = search_codes(elasticsearch_connection, code=data['code'], time_range=data['time_range'],
                                  match_phrase=data['match_phrase'],
                                  start=data['from'],
                                  limit=data['size'], doc_status=data['doc_status'],
                                  document_types_condition=data['document_types_condition'],
                                  document_field=data['document_field'],
                                  issuing_body=data['issuing_body'],
                                  signer=data['signer'], sorted_by=data['sorted_by'],
                                  editor_setting=data['editor_setting'])
        return Response(document)


class RecommendSearch(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = {
            'document_fields': ["Tài chính", "Kế toán"],
            'from': 0,
            'size': 5,
            'time_range': None,
            'doc_status': None,
            'sorted_by': 1
        }
        request_data = request.data
        for key, value in request_data.items():
            data[key] = value

        if data['time_range'] is not None:
            try:
                data['time_range'] = ast.literal_eval(data['time_range'])
            except:
                data['time_range'] = data['time_range']
        print("recommend request: ", data)
        document = recommend_search(elasticsearch_connection,
                                    document_fields=data['document_fields'],
                                    start=data['from'],
                                    limit=data['size'],
                                    time_range=data['time_range'],
                                    doc_status=data['doc_status'],
                                    sorted_by=data['sorted_by'])
        return Response(document)


class MultiFieldSearch(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = {
        'title': 'công',
        'search_dict': ["document_field__Thuế", "document_field__Môi trường",
                        "issuing_body/office/signer__Ngọc", "issuing_body/office/signer__Dương"],
        'from': 0,
        'size': 5,
        'match_phrase': False,
        'time_range': None,
        'sorted_by': 1
        }
        request_data = request.data
        print("multi search: ", request_data)
        for key, value in request_data.items():
            if key == "search_dict":
                new_search_dict = {}
                for item in value:
                    f = item[:item.find("__")]
                    v = item[item.find("__") + 2:]
                    if new_search_dict.get(f, "") == "":
                        new_search_dict[f] = [v]
                    else:
                        new_search_dict[f] += [v]
                data['search_dict'] = new_search_dict
            else:
                data[key] = value

        if data['time_range'] is not None:
            try:
                data['time_range'] = ast.literal_eval(data['time_range'])
            except:
                data['time_range'] = data['time_range']
        
        document = multifield_search(elasticsearch_connection,
                                     keyword=data['title'],
                                     keyword_match_phrase=data["match_phrase"],
                                     search_dict=data['search_dict'],
                                     time_range=data['time_range'],
                                     start=data['from'],
                                     limit=data['size'],
                                     sorted_by=data['sorted_by'])
        
        return Response(document)

