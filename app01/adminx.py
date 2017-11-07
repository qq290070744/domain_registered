#!/usr/bin/env python
# coding:utf-8
import xadmin
from .models import *


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

xadmin.site.register(Department)
xadmin.site.register(filed1)
xadmin.site.register(filed2)
xadmin.site.register(filed3)


class maohaoxAdmin(object):
    list_display = ('name', 'DepartmenT', 'maohao', 'phone', 'times', 'use')
    # search_fields = ('name', 'DepartmenT', 'maohao', 'phone', 'times', 'use')
    search_fields = ('name', 'DepartmenT__department_name', 'maohao', 'phone', 'times', 'use')
    list_filter = ['name', 'DepartmenT', 'maohao', 'phone', 'times', 'use']


xadmin.site.register(maohao_info, maohaoxAdmin)


class registeredAdmin(object):
    list_display = ('domain', 'ip', 'name', 'department', 'use', 'https', 'colored_status', 'RecordId', 'updatetime')
    search_fields = ('domain', 'ip', 'name', 'department', 'use', 'https', 'Review_status', 'RecordId')
    list_filter = ('domain', 'ip', 'name', 'department', 'use', 'https', 'Review_status', 'RecordId', 'updatetime')


xadmin.site.register(registered, registeredAdmin)


class mail_listAdmin(object):
    list_display = ('mail_address', 'mail_name')
    search_fields = ('mail_address', 'mail_name')
    list_filter = ('mail_address', 'mail_name')


xadmin.site.register(mail_list, mail_listAdmin)

from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)
