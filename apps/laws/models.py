from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class DocumentMetaDataTerm(models.Model):
    term_id = models.BigAutoField(20, primary_key=True, unique=True)
    name = models.CharField(max_length=255, unique=True)
    last_update_time = models.DateTimeField()  # Ngày cập nhật meta văn bản (editor)
##Lưu trữ tên các thuộc tính trong ExtractiveDocumentMetaData
##VD: term_id      name
##      1      collection_source

##ExtractiveDocumentMetaData
##VD: meta_id      term_id      collection_source
##      1             1              <string>


class ExtractiveDocument(models.Model):
    id = models.BigAutoField(20, primary_key=True, unique=True)
    source_id = models.BigIntegerField(20, unique=True) #id trích xuất từ url
    source = models.CharField(max_length=225)
    url = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    history = models.CharField(max_length=600, blank=True, null=True)
    html_text = models.TextField()
    full_text = models.TextField()
    last_update_time = models.DateTimeField(blank=True, null=True) #Ngày cập nhật văn bản (crawler)


class ExtractiveDocumentMetaData(models.Model):
    meta_id = models.BigAutoField(20, primary_key=True, unique=True)
    extractive_document_id = models.ForeignKey(ExtractiveDocument, on_delete=models.CASCADE)
    term_id = models.ForeignKey(DocumentMetaDataTerm, on_delete=models.CASCADE)

    term_value = ArrayField(models.CharField(max_length=225))
    last_update_time = models.DateTimeField()  # Ngày cập nhật metadata của văn bản (crawler)

    constraints = [
        models.UniqueConstraint(fields=['extractive_document_id', 'term_id'], name='unique_extractive_document__document_term')
    ]


class RelationType(models.Model):
    id = models.BigAutoField(20, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    last_update_time = models.DateTimeField(blank=True, null=True)  # Ngày cập nhật liên hệ của văn bản (crawler)


class ExtractiveDocumentSchema(models.Model):
    schema_id = models.BigAutoField(20, primary_key=True, unique=True)
    source_id = models.ForeignKey(ExtractiveDocument, on_delete=models.CASCADE, related_name="extractive_document_source")
    destination_id = models.ForeignKey(ExtractiveDocument, on_delete=models.CASCADE, related_name="extractive_document_destination")
    relation_type_id = models.ForeignKey(RelationType, on_delete=models.CASCADE)
    last_update_time = models.DateTimeField()  # Ngày cập nhật schema của văn bản (crawler)

    constraints = [
        models.UniqueConstraint(fields=['destination_id', 'source_id'],
                                name='unique_destination_id__source_id')
    ]


class SelfDraftedDocument(models.Model):
    id = models.BigIntegerField(20, primary_key=True, unique=True)
    title = models.CharField(max_length=45)
    content = models.TextField()
    author = models.CharField(max_length=255)
    created_time = models.DateTimeField() #Ngày soạn thảo văn bản
    last_update_time = models.DateTimeField()  # Ngày cập nhật văn bản (editor)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)


class SelfDraftedDocumentMetaData(models.Model):
    meta_id = models.BigIntegerField(20, primary_key=True, unique=True)
    term_value = models.CharField(max_length=1500)
    last_update_time = models.DateTimeField()  # Ngày cập nhật meta văn bản (editor)
    self_drafted_document_id = models.ForeignKey(SelfDraftedDocument, on_delete=models.CASCADE)
    term_id = models.ForeignKey(DocumentMetaDataTerm, on_delete=models.CASCADE)

