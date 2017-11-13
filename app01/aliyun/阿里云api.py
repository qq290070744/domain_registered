#!/usr/bin/env python
# coding:utf-8
# 调用get_result()函数，并以字典形式传入<请求参数>，<公共请求参数>在函数中已经配置好重复传入会覆盖函数中的设置，返回信息为json
# 调用make_url(url,userdict)函数，并以字典形式传入<请求参数>以字符串传入阿里云api的网址，<公共请求参数>在函数中已经配置好重复传入会覆盖函数中的设置，返回信息为组合好的url
# 调用sign(accessKeySecret, parameters)函数，并以字典形式传入<全部请求参数>以字符串传入阿里云AccessKeySecret，返回信息为计算好的Signature
# 没有特殊需求的话可以直接使用2部分的函数来实现功能。（记得填写AccessKeyId和AccessKeySecret）
import urllib, json
from hashlib import sha1
import base64
import hmac
import time
import datetime
import random
from urllib import request

try:
    import httplib
except ImportError:
    import http.client as httplib
#######################################
AccessKeyId = '8TeO39wwohu7qENg'  # "你的AccessKeyId"
AccessKeySecret = 'wg8K6ZwDc1hiCqxXYKmSVkjRMYngKh'  # "你的AccessKeySecret "

URL = 'http://dns.aliyuncs.com/?'


#######################################
def sign(accessKeySecret, parameters):
    # ===========================================================================
    # '''签名方法
    # @param secret: 签名需要的密钥
    # @param parameters: 支持字典和string两种
    # '''
    # ===========================================================================
    # 如果parameters 是字典类的话
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

    canonicalizedQueryString = ''
    for (k, v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)

    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])

    h = hmac.new(accessKeySecret + b"&", stringToSign.encode('utf8'), sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature


def percent_encode(encodeStr):
    encodeStr = str(encodeStr)
    res = urllib.parse.quote(encodeStr, '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


# Create By Maple 2016.3.2
def make_url(url, userdict):
    # ------------------------------------------------------------------------------
    now = datetime.datetime.utcnow()
    otherStyleTime = now.strftime("%Y-%m-%dT%H:%M:%SZ")  # 2015-01-09T12:00:00Z
    randomint = random.randint(11111111111111, 99999999999999)
    # ------------------------------------------------------------------------------
    dict = {
        "Format": "json",
        "AccessKeyId": AccessKeyId,
        "SignatureMethod": "HMAC-SHA1",
        "SignatureNonce": str(randomint),
        "SignatureVersion": "1.0",
        "Version": "2015-01-09",
        "Timestamp": otherStyleTime,
        "DomainName": "casxt.com",
        "RRKeyWord": "test"}
    dict.update(userdict)
    Signature = percent_encode(sign(AccessKeySecret.encode("utf-8"), dict).decode("utf-8"))
    for k, v in dict.items():
        url = url + "&" + k + "=" + v
    url = url + "&Signature=" + Signature
    return (url)


def get_result(userdict):
    print(userdict)
    url = make_url(URL, userdict)
    with request.urlopen(url) as result:
        if result.status == 400:
            return ("{" + result.reason + "}")
        res = result.read().decode("utf-8")
        return (res)


if __name__ == "__main__":
    dic={"Action":"DescribeDomainRecords","DomainName":"jwmmma.com","RRKeyWord":"jwm"}
    # dic = {"Action": "DeleteDomainRecord", "RecordId": "3519119366461440"}
    # dic = {"Action": "DescribeDomainWhoisInfo", "DomainName": "jwmmma.com"}
    # dic = {"Action": "DescribeDomains", "PageSize": "100"}
    # dic={"Action":"DescribeDomainRecords","DomainName":"cuea.org.cn"}
    # dic={"Action":"AddDomainRecord","DomainName":"cuea.org.cn","RR":"@","Type":"A","Value":"121.201.28.13"}
    # dic={"Action":"AddDomainRecord","DomainName":"daxepay.cn","RR":"jwmtest1","Type":"CNAME","Value":"jwm.jwmmma.com"}
    res = json.loads(get_result(dic))
    print(res)
    # print(res.get('Domains').get('Domain'))
    # for i in res.get('Domains').get('Domain'):
    #     print(i.get('DomainName'))

