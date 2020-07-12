import gzip, csv
import os
import json
import subprocess


def get_content_by_gz(file_path):
    with gzip.open(file_path, 'rt') as f:
        file_content = f.read()
    return file_content


def get_content(file_path):
    with open(file_path) as f:
        s = f.read()
    return s


def get_files_in_folder(folder_path):
    files_absolute_path = []
    files_name = None
    for root, dirs, files in os.walk(os.path.abspath(folder_path)):
        files_name = files
        for file in files:
            files_absolute_path.append(os.path.join(root, file))
    return files_absolute_path, files_name


def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def store_json(object, file_output_path):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    with open(file_output_path, 'w') as fp:
        json.dump(object, fp, ensure_ascii=False, sort_keys=True, indent=1)


def store_file(content, file_output_path, is_append=False):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    if(is_append):
        with open(file_output_path, 'a+') as fh:
            fh.write(str(content))
    else:
        with open(file_output_path, 'w+') as fh:
            fh.write(str(content))


def store_gz(content, file_output_path):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    print('prepare store gz', file_output_path)
    with gzip.open(file_output_path, 'wb') as f:
        f.write(content.encode('utf-8'))


def store_jsons_perline_in_file(jsons_obj, file_output_path, is_append=False):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    if (is_append):
        with gzip.open(file_output_path, 'ab') as f:
            for json_obj in jsons_obj:
                f.write((json.dumps(json_obj, ensure_ascii=False) + '\n').encode('utf-8'))
    else:
        with gzip.open(file_output_path, 'wb') as f:
            for json_obj in jsons_obj:
                f.write((json.dumps(json_obj, ensure_ascii=False) + '\n').encode('utf-8'))


def get_content_from_csv_callback(file_input_path, process_callback):
    with open(file_input_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            process_callback(row)


def get_content_from_csv(file_input_path):
    output = []
    with open(file_input_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            output.append(row)
    return output


def list_uid_to_csv(list_uid, file_path):
    with open(file_path, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for data in list_uid:
            wr.writerow([int(data)])
            # wr.writerow([data])


def wccount(file_path):
    out = subprocess.Popen(['wc', '-l', file_path],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT
                           ).communicate()[0]
    return int(out.partition(b' ')[0])


def wcgzcount(file_path):
    count = 0
    try:
        bashCommand = "zcat " + file_path + " | wc -l"
        # print(bashCommand)
        out = os.popen(bashCommand)
        data = out.read()
        count = int(data.split('\n')[0])
        out.close()
    except Exception as e:
        print(e)
    return count


def count_line_all_gz(folder_path):
    # print('count ', folder_uid_path)
    # files_absolute_path, files_name = get_files_in_folder(folder_path)
    count = 0
    bashCommand = "unpigz -c " + folder_path + "/*.gz | wc -l"
    # print(bashCommand)
    try:
        print('prepare: ', bashCommand)
        out = os.popen(bashCommand)
        data = out.read()
        count = int(data.split('\n')[0])
        out.close()
    except Exception as e:
        print(e)
    print('counted', count, ': ', bashCommand)
    return count


def load_jsonl_from_gz(file_gz_path, min_length_per_line=5):
    output_objs = []
    for text in get_content_by_gz(file_gz_path).split('\n'):
        try:
            if len(text) >= min_length_per_line:
                obj = json.loads(text)
                output_objs.append(obj)
        except Exception as e:
            print(e)
    return output_objs


# print(get_content_by_gz('/mnt/e/wp/startup/meowbees/data/shopee/output/sitemap/sitemap.categories.xml.gz'))
# files_absolute_path, files_name = get_files_in_folder('/mnt/e/wp/startup/meowbees/data/shopee/output/sitemap')

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start

def is_exist_file(file_path):
    return os.path.isfile(file_path)