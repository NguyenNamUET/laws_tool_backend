from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Setting)
admin.site.register(DocumentTemplate)
admin.site.register(ErrorDescription)
admin.site.register(Info)
admin.site.register(SystemMessage)
