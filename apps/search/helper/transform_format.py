from apps.search.helper.reader_helper import load_json, store_file


def convert_json_to_line(input_path, output_path):
    data = load_json(input_path)
    output = ''

    for idx, element in enumerate(data):
        if (idx == 0):
            output = element
        else:
            output += '\n' + element
    store_file(output, output_path)


def dictionary_to_array(data):
    output = []
    for item in data:
        output.append(item)
    return output