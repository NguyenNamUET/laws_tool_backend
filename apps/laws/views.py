from django.shortcuts import render
from .models import ExtractiveDocument, ExtractiveDocumentMetaData
from .serializers import ExtractiveDocumentSerializer, SitemapSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import views
from rest_framework.renderers import JSONRenderer
from django.db.models import F
import re

import numpy as np
import json

from apps.search.service.search_service.vblp_searcher import search_title
from apps.search.es_service.es_connection import elasticsearch_connection

from keras.models import load_model
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy
from keras.preprocessing.sequence import pad_sequences



s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
def remove_accents(input_str):
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s

class ExtractiveDocumentList(generics.ListAPIView):
    queryset = ExtractiveDocument.objects.all()
    serializer_class = ExtractiveDocumentSerializer


class ExtractiveDocumentDetail(generics.RetrieveAPIView):
    queryset = ExtractiveDocument.objects.all()
    serializer_class = ExtractiveDocumentSerializer


class Sitemap(views.APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        joins = ExtractiveDocumentMetaData.objects.select_related('extractive_document_id')\
                                                 .annotate(doc_title=F('extractive_document_id__title'))\
                                                 .filter(term_id_id=5)\
                                                 .values_list('extractive_document_id_id','term_value', 'doc_title')

        start = self.request.query_params.get('from', 0)
        size = self.request.query_params.get('size', 2000)

        sitemaps = ["/van-ban/"
                    + remove_accents(re.sub("(\-)+", "-", (re.sub("(\s|\/|\.|\:|\,)", "-", doc[1][0])))) +"/"
                    + remove_accents(re.sub("(\s|\/|\.|\:)", "-", doc[2]))
                    + "-" + str(doc[0])
                    for doc in joins[int(start):min(int(start) + int(size), len(joins))]]
        return Response({"sitemaps": sitemaps, "docs_count": len(joins)})


class SearchDocInDoc(views.APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        id = self.request.query_params.get('id', 1)
        doc_text = ExtractiveDocument.objects.filter(id=id).values_list("full_text")[0][0]

        regex = '''(((([cC] *h *ỉ *t *h *ị|[c|C] *ô *n *g *v *ă *n|[đĐ] *i *ề *u *ư *ớ *c *q *u *ố *c *t *ế|[hH] *i *ế *n *p *h *á *p|[lL] *ệ *n *h|[lL] *u *ậ *t|[nN] *g *h *ị *đ *ị *n *h|[nN] *g *h *ị *đ *ị *n *h *t *h *ư|[nN] *g *h *ị *q *u *y *ế *t|[pP] *h *á *p *l *ệ *n *h|[qQ] *u *y *ế *t *đ *ị *n *h|[sS] *ắ *c *l *ệ *n *h|[tT] *h *ô *n *g *t *ư *(l *i *ê *n *t *ị *c *h)?|[vV] *ă *n *b *ả *n *(h *ợ *p *n *h *ấ *t)?|[hH] *ư *ớ *n *g *d *ẫ *n|[cC] *ô *n *g *b *á *o|[tT] *h *ô *n *g *đ *i *ệ *n|[kK] *ế *h *o *ạ *c *h|[cC] *h *ư *ơ *n *g *t *r *ì *n *h|[tT] *ờ *t *r *ì *n *h|[dD] *ự *t *h *ả *o *n *g *h *ị *đ *ị *n *h|[dD] *ự *t *h *ả *o *q *u *y *ế *t *đ *ị *n *h|[cC] *a *m *k *ế *t|[tT] *h *ô *n *g *b *á *o|[tT] *u *y *ê *n *b *ố|[pP] *h *ụ *l *ụ *c|[hH] *i *ệ *p *đ *ị *n *h *(c *h *u *n *g)?|[tT] *h *ỏ *a *t *h *u *ậ *n|[vV] *ă *n *k *i *ệ *n)) *(số)? *)*((\d+[\/\-]?)+([aăâbcdđeêghiklmnoôơpqrstuưvxywAĂÂBCDĐEÊGHIKLMNOÔƠPQRSTUƯVXYW]+\d*[\/\-\.\:]?\d*)+|([aăâbcdđeêghiklmnoôơpqrstuưvxywAĂÂBCDĐEÊGHIKLMNOÔƠPQRSTUƯVXYW]+([\:\-]?\d+)+(\w+[\/\:]?)+)))'''
        all_found_documents = [found[0] for found in re.findall(regex, str(doc_text).replace("\n", " "))]
        return Response({"found": all_found_documents})



def load_jsonl_from_json(file_json_path):
    try:
        with open(file_json_path, 'rt') as f:
            file_content = f.read()
            obj = json.loads(file_content)
            return obj
    except Exception as e:
        print(e)


def tokenize(sentence):
    return re.findall(r"[\w']+|[.,!?;/-]", sentence.lower())


def to_label(output, shape0=1000, shape1=3):
    tags = {0: "O",
            1: "B-Văn bản pháp luật", 2: "I-Văn bản pháp luật"}
    output = output.reshape(shape0, shape1)
    label = np.array(output).argmax(axis=1)
    label_txt = [tags.get(l) for l in label]
    return label_txt

ALL_DOC_TYPE_REGEX = "[b|B] *ộ *l *u *ậ *t|[b|B] *ả *n *g *h *i|[b|B] *i *ê *n *b *ả *n|[c|C] *ô *n *g *v *ă *n|[c|C] *ô *n *g *ư *ớ *c|[d|D] *ự *t *h *ả *o|[h|H] *i *ệ *p *đ *ị *n *h|[đ|Đ] *i *ề *u *l *ệ|[t|T] *i *ê *u *c *h *u *ẩ *n|[c|C] *h *ỉ *t *h *ị|[đ|Đ] *i *ề *u *ư *ớ *c *q *u *ố *c *t *ế|[h|H] *i *ế *n *p *h *á *p|[l|L] *ệ *n *h|[l|L] *u *ậ *t|[n|N] *g *h *ị *đ *ị *n *h( *t *h *ư *)?|[n|N] *g *h *ị *q *u *y *ế *t|[p|P] *h *á *p *l *ệ *n *h|[q|Q] *u *y *ế *t *đ *ị *n *h|[s|S] *ắ *c *l *ệ *n *h|[t|T] *h *ô *n *g *t *ư( *l *i *ê *n *t *ị *c *h *)?|[v|V] *ă *n *b *ả *n( *h *ợ *p *n *h *ấ *t *)?|[h|H] *ư *ớ *n *g *d *ẫ *n|[c|C] *ô *n *g *b *á *o|[t|T] *h *ô *n *g *đ *i *ệ *n|[k|K] *ế *h *o *ạ *c *h|[c|C] *h *ư *ơ *n *g *t *r *ì *n *h|[t|T] *ờ *t *r *ì *n *h|[d|D] *ự *t *h *ả *o *n *g *h *ị *đ *ị *n *h|[d|D] *ự *t *h *ả *o *q *u *y *ế *t *đ *ị *n *h|[c|C] *a *m *k *ế *t|[t|T] *h *ô *n *g *b *á *o|[t|T] *u *y *ê *n *b *ố|[p|P] *h *ụ *l *ụ *c|[h|H] *i *ệ *p *đ *ị *n *h( *c *h *u *n *g *)?|[t|T] *h *ỏ *a *t *h *u *ậ *n|[v|V] *ă *n *k *i *ệ *n"
#loaded_model = load_model('apps/laws/model/model1007_epoch10.h5', custom_objects={'CRF': CRF,
#                                                                         'crf_loss': crf_loss,
#                                                                         'crf_viterbi_accuracy': crf_viterbi_accuracy})

#wordIndex = load_jsonl_from_json("apps/laws/model/wordIndex1007_300k.json")


class SearchDocInDoc(views.APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        loaded_model = load_model('apps/laws/model/model1007_epoch10.h5', custom_objects={'CRF': CRF,
                                                                         'crf_loss': crf_loss,
                                                                         'crf_viterbi_accuracy': crf_viterbi_accuracy})

        wordIndex = load_jsonl_from_json("apps/laws/model/wordIndex1007_300k.json")
        data = {
            'doc_text': '',
            'from': 0,
            'size': 5,
	    'minimum_should_match':"80",
            'time_range': None,
            'match_phrase': False,
            'sorted_by': 1,
        }
        request_data = request.data
        for key, value in request_data.items():
            data[key] = value
        

        doc_text = data["doc_text"]
        print("doc_text: ", doc_text)
        # regex = '''(((([cC] *h *ỉ *t *h *ị|[c|C] *ô *n *g *v *ă *n|[đĐ] *i *ề *u *ư *ớ *c *q *u *ố *c *t *ế|[hH] *i *ế *n *p *h *á *p|[lL] *ệ *n *h|[lL] *u *ậ *t|[nN] *g *h *ị *đ *ị *n *h|[nN] *g *h *ị *đ *ị *n *h *t *h *ư|[nN] *g *h *ị *q *u *y *ế *t|[pP] *h *á *p *l *ệ *n *h|[qQ] *u *y *ế *t *đ *ị *n *h|[sS] *ắ *c *l *ệ *n *h|[tT] *h *ô *n *g *t *ư *(l *i *ê *n *t *ị *c *h)?|[vV] *ă *n *b *ả *n *(h *ợ *p *n *h *ấ *t)?|[hH] *ư *ớ *n *g *d *ẫ *n|[cC] *ô *n *g *b *á *o|[tT] *h *ô *n *g *đ *i *ệ *n|[kK] *ế *h *o *ạ *c *h|[cC] *h *ư *ơ *n *g *t *r *ì *n *h|[tT] *ờ *t *r *ì *n *h|[dD] *ự *t *h *ả *o *n *g *h *ị *đ *ị *n *h|[dD] *ự *t *h *ả *o *q *u *y *ế *t *đ *ị *n *h|[cC] *a *m *k *ế *t|[tT] *h *ô *n *g *b *á *o|[tT] *u *y *ê *n *b *ố|[pP] *h *ụ *l *ụ *c|[hH] *i *ệ *p *đ *ị *n *h *(c *h *u *n *g)?|[tT] *h *ỏ *a *t *h *u *ậ *n|[vV] *ă *n *k *i *ệ *n)) *(số)? *)*((\d+[\/\-]?)+([aăâbcdđeêghiklmnoôơpqrstuưvxywAĂÂBCDĐEÊGHIKLMNOÔƠPQRSTUƯVXYW]+\d*[\/\-\.\:]?\d*)+|([aăâbcdđeêghiklmnoôơpqrstuưvxywAĂÂBCDĐEÊGHIKLMNOÔƠPQRSTUƯVXYW]+([\:\-]?\d+)+(\w+[\/\:]?)+)))'''
        # all_found_documents = [found[0] for found in re.findall(regex, str(doc_text).replace("\n", " "))]
        all_found_documents = []

        for sentence in re.compile("[\;\.](?=\s*[ẠẢẤẦẨẪẬẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝAĂÂBCDĐEÊGHIĨŨKLMNOÔƠPQRSTUƯVXYW])").split(doc_text):
            sentence = re.sub("\s{2,}", " ", sentence.replace("\n", " "))
            if len(re.findall(ALL_DOC_TYPE_REGEX, sentence)) > 0:
                print("sentence: ", sentence, "\n")
                indexed_sentence = [[wordIndex.get(s, 0) for s in tokenize(sentence)]]
                indexed_sentence = pad_sequences(maxlen=1000, sequences=indexed_sentence, padding="post", value=0)
                pred_labels = loaded_model.predict(indexed_sentence)
                zip_sentence_label = list(zip(tokenize(sentence), to_label(pred_labels)))

                ent = ""
                for word, tag in zip_sentence_label:
                    if tag == "B-Văn bản pháp luật":
                        ent = word + " "
                    elif tag == "I-Văn bản pháp luật" and len(ent)>0:
                        ent += word + " "
                    else:
                        if len(ent) > 0 and ent not in all_found_documents:
                            all_found_documents.append(ent)
                            ent = ""


        detailed_found_document = []
        for ent in all_found_documents:
            print(ent)
            obj = {"text": ent, "detailed": []}
            if len(ent) > 0:
                es_search = search_title(es=elasticsearch_connection,
                                         title=ent,
                                         match_phrase=data["match_phrase"],
                                         minimum_should_match=data["minimum_should_match"],
                                         sorted_by=data["sorted_by"],
                                         start=data["from"],
                                         limit=data["size"],
                                         time_range=data["time_range"])

                
                if len(es_search) > 0:
                    for searched_es in es_search["hits"]["hits"]:
                        detail = searched_es["_source"]["attribute"]
                        detail["url"] = searched_es["_source"]["url"]
                        obj["detailed"].append(detail)

                detailed_found_document.append(obj)
        return Response({"found": detailed_found_document})
