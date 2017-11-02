"""domain_registered URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views as app01

urlpatterns = [
    url(r"^$", app01.index),
    url(r"^maohao", app01.maohao_souji),
    # url(r"^已经录入过信息查看", app01.maohao_souji),
    url(r"^accounts/login/$", app01.acc_login),
    url(r"^accounts/logout/$", app01.acc_logout),
    url(r"^his", app01.his),
    url(r'^admin/', admin.site.urls),
    url(r"^Review", app01.Review),
    url(r"^DeleteDomainRecord", app01.DeleteDomainRecord),
    url(r"^domainInfo", app01.domain_info),
]
