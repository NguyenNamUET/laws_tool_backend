import sys
sys.path.append('./')
import os
from concurrent.futures import ThreadPoolExecutor

from config.config_project import folder_output_path
from helper.reader_helper import load_jsonl_from_gz
from es_service.es_connection import elasticsearch_connection, insert_doc

def index_record(file, id):
    try:
        law_document = load_jsonl_from_gz(file)
        law_document.update({'id': str(id)})
        #print(row_dict)
        # print(row['url'])
        # print(row['Tên VB'])
        # print(row['Toàn văn'])
        # print(row['VB Tiếng anh'])
        # print(row['Thuộc tính'])
        # print(row['Lịch sử'])
        # print(row['VB Liên Quan'])
        # print(row['Lược đồ'])
        # break
        index_document_law_to_es(law_document)
    except Exception as e:
        print("------------------------------------------------------------------------------")
        print('error: ', e)

def get_gz_path(base_path):
    files = []
    for r, d, f in os.walk(base_path):
        for file in f:
            if '.gz' in file:
                files.append(os.path.join(r, file))
    return files


def load_vbpl(raw_path):
    files = get_gz_path(raw_path)
    executor = ThreadPoolExecutor(max_workers=50)

    for idx, file in enumerate(files):
        executor.submit(index_record, file)


def index_document_law_to_es(law_document):
    es = elasticsearch_connection
    index = "law_tech"
    doc_type = '_doc'
    id = law_document.get('id')
    print(id)
    insert_doc(es, index, doc_type, id, law_document, verbose=True)


def execute():
    raw_path = folder_output_path + '/vbpl/raw'
    load_vbpl(raw_path)

# time.sleep(30)
execute()
