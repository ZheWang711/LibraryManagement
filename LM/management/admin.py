from django.contrib import admin
from management.models import *

admin.site.register(MyUser)
admin.site.register(Record)
admin.site.register(Img)
admin.site.register(MySubjectRelations)
admin.site.register(Subject)
admin.site.register(MyNews)