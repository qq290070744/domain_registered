from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Count
import time, json, pymysql, collections, os, re
from app01.models import *
from django.http import JsonResponse
# Create your views here.
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from app01.aliyun import 阿里云api
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
import threading
from django.core import serializers


def acc_login(request):
    if request.method == "POST":
        print(request.POST)
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            return redirect(request.GET.get('next'))
        else:
            error = "error"
            return render(request, "login.html", {"login_error": error})

    return render(request, "login.html")


@login_required
def acc_logout(requrst):
    logout(requrst)
    return redirect("/")


# text = '''
# 申请人：{}
# 申请部门：{}
# 域名用途：{}
#
# 正式：{}
# 测试：beta-{}
# 开发：dev-{}
# 灰度：rel-{}
# 验收：check-{}
#
# 是否需要https：{}
# '''
text = '''
申请人：{}
申请部门：{}
域名用途：{}
正式域名：{}
解析到的IP地址:{}
是否需要https：{}
'''
to_mail = [
    # 'jiangwh@healthmall.cn',
    # 'sateam@healthmall.cn',
]  # 邮件发送给谁


@login_required
def index(request):
    maillist = mail_list.objects.all()
    for i in maillist:
        if i.mail_address not in to_mail:
            to_mail.append(i.mail_address)
    d1 = filed1.objects.all()
    d2 = filed2.objects.all()
    d3 = filed3.objects.all()
    print("用户正在访问主页")
    if request.POST:
        print(request.POST)
        data = request.POST

        mail = "{}-{}.{}.{}".format(data["domain"], data["domain1"], data["domain3"], data["domain4"])
        mail = mail.replace("无-", '')
        print(mail)
        mail_text = text.format(data["user"], data["department"], data["use"], mail, data['ip'], data["https"])
        send_mail('域名申请', mail_text, 'sa@healthmall.cn',
                  to_mail, fail_silently=False)  # 'sateam@healthmall.cn'

        b = registered(domain=mail, name=data["user"], department=data["department"], use=data["use"], ip=data['ip'],
                       https=data["https"], updatetime=time.strftime("%Y-%m-%d %H:%M:%S"), Review_status="未审核")
        b.save()
        mail_text = mail_text.replace("\n", "<br>")
        return render(request, 'index.html', {"ok": mail_text, "d1": d1, "d2": d2, "d3": d3}, )
    return render(request, 'index.html', {"d1": d1, "d2": d2, "d3": d3})


@login_required
def domain_info(request):
    apidic = {"Action": "DescribeDomains", "PageSize": "100"}
    res = 阿里云api.get_result(apidic)
    res = json.loads(res)
    domain_list = res.get('Domains').get('Domain')
    domain_info_list = []

    def exec_api(i):
        DomainName = i.get('DomainName')
        domain_Info = 阿里云api.get_result({"Action": "DescribeDomainWhoisInfo", "DomainName": DomainName})
        domain_Info = json.loads(domain_Info)
        domain_Info['DomainName'] = DomainName
        domain_info_list.append(domain_Info)
        # print(domain_info_list)

    if request.is_ajax():

        for i in domain_list:
            t = threading.Thread(target=exec_api, args=(i,))
            t.start()
            t.join()

        return JsonResponse(domain_info_list, safe=False)
    return render(request, 'domain_info.html')


def maohao_souji(request):
    DepartmenT = Department.objects.all()

    if request.POST:
        data = request.POST
        name = data.get('name')
        department = data.get('department')
        department_id=Department.objects.filter(department_name=department)
        departmentId=serializers.serialize("json",department_id)
        departmentId=json.loads(departmentId)
        departmentId=departmentId[0]["pk"]
        print(departmentId)
        maohao = data.get('maohao')
        phone = data.get('phone')
        times = data.get('time')
        use = data.get('use')
        b = maohao_info(name=name, DepartmenT_id=departmentId, maohao=maohao, phone=phone, times=times, use=use)
        b.save()
        return render(request, 'maohao.html', {"ok": "ok", "DepartmenT": DepartmenT})
    return render(request, 'maohao.html', {"DepartmenT": DepartmenT})


@login_required
def his(request):
    seach = request.GET.get('seach')
    data = registered.objects.all().order_by('-id')
    data = Seach(seach, data)
    if request.POST:
        print(request.POST)
        data_id = request.POST['_id']
        mail_select = request.POST["mail"]
        if (mail_select == 'ok'):
            mail_text = registered.objects.filter(id=data_id)
            for i in mail_text:
                mail_text = "域名：{}已被删除!".format(i.domain)

                send_mail('域名删除', mail_text, 'sa@healthmall.cn', to_mail,
                          fail_silently=False)  # "lixk@healthmall.cn",'sateam@healthmall.cn'

        d = registered(id=data_id)
        d.delete()

    if not seach:
        paginator = Paginator(data, 15)  # 每页显示15个
    else:
        paginator = Paginator(data, 100)  # 每页显示100个
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页面不是整数，请提供第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页面超出范围（例如9999），则提供最后一页的结果。
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'his.html', {'contacts': contacts, "页的序号": range(1, contacts.paginator.num_pages + 1)})
    # return render(request, 'his.html', {"data": data})


@staff_member_required
def Review(request):
    data = registered.objects.exclude(Review_status="审核通过").order_by('-id')
    try:
        if request.POST.get("_id") and request.POST.get("mail"):
            print(request.POST)
            data_id = request.POST['_id']
            mail_select = request.POST["mail"]
            ip = request.POST["ip"]

            mail_text = registered.objects.filter(id=data_id)
            for i in mail_text:
                # ip=i.ip
                mail_text = "域名：{} 已审核通过!".format(i.domain)

                RecordId = domain_api('AddDomainRecord', i.domain, i.https, ip)  # 调用阿里云域名api
                if RecordId:
                    if (mail_select == 'ok'):
                        send_mail('域名审核通过', mail_text, 'sa@healthmall.cn', to_mail, fail_silently=False)  # 发邮件
                    registered.objects.filter(id=data_id).update(Review_status='审核通过', RecordId=RecordId)  # 数据库记录
    except Exception:
        pass

    paginator = Paginator(data, 10)  # 每页显示10个
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页面不是整数，请提供第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页面超出范围（例如9999），则提供最后一页的结果。
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'review.html', {"contacts": contacts})


@staff_member_required
def DeleteDomainRecord(request):
    seach = request.GET.get('seach')
    # print(seach)
    data = registered.objects.filter(RecordId__isnull=False).order_by('-id')
    data = Seach(seach, data)
    if request.POST:
        print(request.POST)
        data_id = request.POST['_id']
        mail_select = request.POST["mail"]
        RecordId = request.POST["RecordId"]
        apidic = {"Action": "DeleteDomainRecord", "RecordId": RecordId}
        res = 阿里云api.get_result(apidic)
        res = json.loads(res)
        registered.objects.filter(RecordId=res.get('RecordId')).update(RecordId="解析记录已删除", Review_status='')
        if (mail_select == 'ok'):
            mail_text = registered.objects.filter(id=data_id)
            for i in mail_text:
                mail_text = "解析记录：{}已被删除!".format(i.domain)

                send_mail('解析记录删除', mail_text, 'sa@healthmall.cn', to_mail,
                          fail_silently=False)  # "lixk@healthmall.cn",'sateam@healthmall.cn'
    if not seach:
        paginator = Paginator(data, 15)  # 每页显示15个
    else:
        paginator = Paginator(data, 100)  # 每页显示100个
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页面不是整数，请提供第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页面超出范围（例如9999），则提供最后一页的结果。
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'his.html',
                  {"解析记录删除": "解析记录删除", 'contacts': contacts, "页的序号": range(1, contacts.paginator.num_pages + 1)})


def Seach(seach, data):
    search_keywords = seach
    if search_keywords:
        data = data.filter(Q(domain__icontains=search_keywords) | Q(ip__icontains=search_keywords) | Q(
            name__icontains=search_keywords) | Q(department__icontains=search_keywords) | Q(
            use__icontains=search_keywords) | Q(https__icontains=search_keywords) | Q(
            Review_status__icontains=search_keywords) | Q(RecordId__icontains=search_keywords))
    return data


def domain_api(Action, domain, https, ip):
    domain_split = domain.split('.')
    domain_split_3 = ''
    if len(domain_split) > 3:
        domain_split_3 = '.' + domain_split[-1]
    RR = domain.split('.')[0]
    reip = re.match('^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$', ip)
    if reip:
        Type = 'A'
    else:
        Type = 'CNAME'
        RR = RR.lower()  # 变小写
    dic = {"Action": Action, "DomainName": "{}.{}{}".format(domain_split[1], domain_split[2], domain_split_3),
           "RR": RR, "Type": Type, "Value": ip}
    res = 阿里云api.get_result(dic)
    res = json.loads(res)
    print(res.get('RecordId'))
    return res.get('RecordId')
