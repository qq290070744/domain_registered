from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return self.name


class Department(models.Model):
    department_name = models.CharField('申请部门', max_length=100)

    def __str__(self):
        return self.department_name


class maohao_info(models.Model):
    name = models.CharField(max_length=100)
    # department = models.CharField('申请部门', max_length=100, null=True)
    DepartmenT = models.ForeignKey(Department,null=True)
    maohao = models.CharField('猫号', max_length=100)
    phone = models.CharField(max_length=100)
    times = models.CharField(max_length=100)
    use = models.CharField('使用情况说明用途', max_length=100, null=True)

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

    def __str__(self):
        return self.name


class filed2(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class filed3(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class mail_list(models.Model):
    mail_address = models.CharField('邮件地址', max_length=100, unique=True)
    mail_name = models.CharField('姓名', max_length=100)

    def __str__(self):
        return self.mail_name
