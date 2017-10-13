from django.contrib import admin
from .models import *


# Register your models here.
class userproAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


admin.site.register(userpro, userproAdmin)

admin.site.register(filed1)
admin.site.register(filed2)
admin.site.register(filed3)


class registeredAdmin(admin.ModelAdmin):
    list_display = ('domain', 'ip', 'name', 'department', 'use', 'https', 'Review_status', 'RecordId', 'updatetime')
    search_fields = ('domain', 'ip', 'name', 'department', 'use', 'https', 'Review_status', 'RecordId', 'updatetime')


admin.site.register(registered, registeredAdmin)


class mail_listAdmin(admin.ModelAdmin):
    list_display = ('mail_address', 'mail_name')
    search_fields = ('mail_address', 'mail_name')


admin.site.register(mail_list, mail_listAdmin)
