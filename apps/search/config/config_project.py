import os

# coding: utf-8


# folder_input_path
folder_output_path = os.environ.get('folder_output_path', '/run/media/kodiak/New Volume/Documents/data/20181202/')

ES_IP = os.environ.get('ES_IP', '112.137.142.8')
ES_USER = os.environ.get('ES_USER', 'user')
ES_PASS = os.environ.get('ES_PASS', '12345678')
ES_PORT = os.environ.get('ES_PORT', '9202')

minimum_should_match_for_search = "100"
