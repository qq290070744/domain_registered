# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-02 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0010_mail_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='maohao_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100, null=True, verbose_name='申请部门')),
                ('maohao', models.CharField(max_length=100, verbose_name='猫号')),
                ('phone', models.CharField(max_length=100)),
                ('times', models.CharField(max_length=100)),
                ('use', models.CharField(max_length=100, null=True, verbose_name='域名使用情况说明用途')),
            ],
        ),
        migrations.AlterField(
            model_name='registered',
            name='updatetime',
            field=models.DateTimeField(auto_now=True, verbose_name='最新修改时间'),
        ),
    ]