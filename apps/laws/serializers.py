from rest_framework import serializers
from .models import ExtractiveDocument
import re

class ExtractiveDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractiveDocument
        fields = ["title", "id"]

#class SitemapSerializer(serializers.ModelSerializer):
#    sitemap = serializers.SerializerMethodField()
#
#    class Meta:
#        model = ExtractiveDocument
#        fields = ['sitemap']
#
#    def get_sitemap(self, obj):
#        title = re.sub("(\s|\/)", "-", str(obj.title))
#        return "/laws/" + title + "-" + str(obj.source_id)

class SitemapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractiveDocument
        fields = ["id", "title"]
