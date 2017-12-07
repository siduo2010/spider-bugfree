#-*- coding: UTF-8 -*-
import urllib
import http.cookiejar
from getpass import getpass
from bs4 import BeautifulSoup

def URL_login(user_name, user_password, BugID):
    filename = 'cookie_Bugfree.txt'
    # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = http.cookiejar.MozillaCookieJar(filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    user_agent = r'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'
    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

    postdata = urllib.parse.urlencode({
        "LoginForm[username]": user_name,
        "LoginForm[password]": user_password,
        "LoginForm[language]": "zh_cn",
        "LoginForm[rememberMe]": "0"}).encode()

    # 登录URL
    loginUrl = 'http://10.9.51.183:8888/bugfree/index.php/site/login'
    # 模拟登录，并把cookie保存到变量
    request = urllib.request.Request(loginUrl, postdata, headers)
    result = opener.open(request).read()
    result_soup = BeautifulSoup(result, 'html.parser').text
    # 保存cookie到cookie.txt中
    cookie.save(ignore_discard=True, ignore_expires=True)
    if result_soup.find('用户名和密码不匹配') != -1:
        request_result = '0'
    else:
        request_result = '1'

    # 利用cookie请求访问另一个网址
    gradeUrl = 'http://10.9.51.183:8888/bugfree/index.php/bug/' + BugID
    # 请求访问查询网址, 'utf-8'
    result = opener.open(gradeUrl).read()
    return result

    return result

def bs4_paraser(html):
    all_value = []
    value = {}
    soup = BeautifulSoup(html, 'html.parser')
    # 获取的部分
    try:
        id_html = soup.find('span', attrs={'id': 'span_info_id'}).string  # , limit=1

        title = soup.find('input', attrs={'id': 'BugInfoView_title'})['value']

        name = soup.find('input', attrs={'id': 'BugInfoView_mail_to'})['value']

        print('Bugfree ID:' + id_html)
        print('Bugfree Title:' + title)
        print('Bugfree name:' + name)
    except:
        print('systerm failed!')

