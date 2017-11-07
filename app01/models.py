from django.db import models
from django.contrib.auth.models import User
import datetime, time
from django.utils.html import format_html


# Create your models here.
class registered(models.Model):
    domain = models.CharField('域名', max_length=100)
    ip = models.CharField('要解析到的IP地址', max_length=30, null=True)
    name = models.CharField('申请人', max_length=30, null=True)
    department = models.CharField('申请部门', max_length=100, null=True)
    use = models.CharField('域名用途', max_length=100, null=True)
    https = models.CharField('是否需要https', max_length=100, null=True)
    Review_status = models.CharField('审核状态', max_length=100, null=True)
    RecordId = models.CharField('解析记录的ID', max_length=100, null=True)
    updatetime = models.DateTimeField('最新修改时间', auto_now=True)

    def colored_status(self):
        """
        在前端给状态字段根据不同状态添加不同的背景色
        Django 1.7之后需要format_html将字符串渲染一下
        用该函数名（colored_status）替换在model Admin中list_display中的status即可。
        :return:
        """
        global format_td
        if self.Review_status == "审核通过":
            format_td = format_html('<span style="background-color:yellowgreen;color:white">审核通过</span>')
        else:
            format_td = format_html('<span style="background-color:pink;color:red">未审核</span>')
        return format_td

    colored_status.short_description = "审核状态"

    class Meta:  # 这个是用来在admin页面上展示的，因为默认显示的是表名，加上这个就变成中文啦
        verbose_name = '域名信息表'
        verbose_name_plural = "域名信息表"

    def __str__(self):
        return self.name


class Department(models.Model):
    department_name = models.CharField('申请部门', max_length=100)

    class Meta:  # 这个是用来在admin页面上展示的，因为默认显示的是表名，加上这个就变成中文啦
        verbose_name = '猫号部门信息表'
        verbose_name_plural = "猫号部门信息表"

    def __str__(self):
        return self.department_name


class maohao_info(models.Model):
    name = models.CharField('姓名', max_length=100)
    # department = models.CharField('申请部门', max_length=100, null=True)
    DepartmenT = models.ForeignKey(Department, null=True, verbose_name=u"申请部门")
    maohao = models.CharField('猫号', max_length=100)
    phone = models.CharField('注册手机号', max_length=100)
    times = models.CharField('注册时间', max_length=100)
    use = models.CharField('使用情况说明用途', max_length=100, null=True)

    class Meta:  # 这个是用来在admin页面上展示的，因为默认显示的是表名，加上这个就变成中文啦
        verbose_name = '猫号信息表'
        verbose_name_plural = "猫号信息表"

    def __str__(self):
        return self.name


class userpro(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(u'姓名', max_length=30)

    def __unicode__(self):
        return self.name


class domain_filed(models.Model):
    filed1 = models.CharField(max_length=100, null=True)
    filed2 = models.CharField(max_length=100, null=True)
    filed3 = models.CharField(max_length=100, null=True)


class filed1(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:  # 这个是用来在admin页面上展示的，因为默认显示的是表名，加上这个就变成中文啦
        verbose_name = '域名字段1表'
        verbose_name_plural = "域名字段1表"

    def __str__(self):
        return self.name


class filed2(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:  # 这个是用来在admin页面上展示的，因为默认显示的是表名，加上这个就变成中文啦
        verbose_name = '域名字段2表'
        verbose_name_plural = "域名字段2表"

    def __str__(self):
        return self.name


class filed3(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:  # 这个是用来在admin页面上展示的，因为默认显示的是表名，加上这个就变成中文啦
        verbose_name = '域名字段3表'
        verbose_name_plural = "域名字段3表"

    def __str__(self):
        return self.name


class mail_list(models.Model):
    mail_address = models.CharField('邮件地址', max_length=100, unique=True)
    mail_name = models.CharField('姓名', max_length=100)

    class Meta:  # 这个是用来在admin页面上展示的，因为默认显示的是表名，加上这个就变成中文啦
        verbose_name = '邮件接收人表'
        verbose_name_plural = "邮件接收人表"

    def __str__(self):
        return self.mail_name


class EmailVerifyRecord(models.Model):
    email_choices = (
        ('register', u'注册'),
        ('forget', u'找回密码'),
    )
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices=email_choices, max_length=10, verbose_name=u'验证码类型')
    send_time = models.DateTimeField(verbose_name=u'发送时间')
