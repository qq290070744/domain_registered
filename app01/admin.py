from django.contrib import admin
from .models import *
import datetime, xadmin
from django.http import HttpResponse
import csv
from xadmin import views


# Register your models here.
class userproAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


admin.site.register(userpro, userproAdmin)

admin.site.register(Department)

admin.site.register(filed1)

admin.site.register(filed2)


class OrderItemInline(admin.TabularInline):
    model = maohao_info
    raw_id_fields = ['name', 'DepartmenT', 'maohao', 'phone', 'times', 'use']


class maohaoAdmin(admin.ModelAdmin):
    list_display = ('name', 'DepartmenT', 'maohao', 'phone', 'times', 'use')
    search_fields = ('name', 'DepartmenT', 'maohao', 'phone', 'times', 'use')
    list_filter = ['name', 'DepartmenT', 'maohao', 'phone', 'times', 'use']


admin.site.register(maohao_info, maohaoAdmin)




class registeredAdmin(admin.ModelAdmin):
    list_display = ('domain', 'ip', 'name', 'department', 'use', 'https', 'Review_status', 'RecordId', 'updatetime')
    search_fields = ('domain', 'ip', 'name', 'department', 'use', 'https', 'Review_status', 'RecordId', 'updatetime')


admin.site.register(registered, registeredAdmin)





class mail_listAdmin(admin.ModelAdmin):
    list_display = ('mail_address', 'mail_name')
    search_fields = ('mail_address', 'mail_name')


admin.site.register(mail_list, mail_listAdmin)

