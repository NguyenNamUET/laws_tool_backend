from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(DocumentMetaDataTerm)
admin.site.register(ExtractiveDocument)
admin.site.register(ExtractiveDocumentMetaData)
admin.site.register(RelationType)
admin.site.register(ExtractiveDocumentSchema)
admin.site.register(SelfDraftedDocument)
admin.site.register(SelfDraftedDocumentMetaData)

