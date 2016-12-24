#coding=utf-8

import time
from bs4 import BeautifulSoup
from userAgents import *
from proxiesList import proxy
import requests

print '此次爬虫使用的代理IP是{}'.format(proxy)

'''
-------------------------------------------------------------
方法1作用：获取某个贴吧的信息
参数说明："tieba_name"是打开某个贴吧后，浏览器地址栏中的"kw="之后的汉字
-------------------------------------------------------------
'''
def get_tieba_detail_info(tieba_name):
    start_url='http://tieba.baidu.com/f'
    host_url='http://tieba.baidu.com'
    payload={'ie':'utf-8','kw':str(tieba_name)}
    r=requests.get(start_url,params=payload,proxies=proxy,timeout=20)
    if r.status_code==200:
        time.sleep(2)
        bs=BeautifulSoup(r.text,'lxml')
        # 1、获取贴吧名字
        get_name=bs.find('title').text
        name=get_name.split('_')[0].split(' ')[-1]
        # 2、获取关注人数
        get_memNum=bs.select('span[class="card_menNum"]')[0]
        memNum=get_memNum.text
        # 3、获取帖子总数
        get_infoNum=bs.select('span[class="card_infoNum"]')[0]
        infoNum=get_infoNum.text
        # 4、获取本吧所在类别信息
        get_card_info=bs.select('div.card_info > ul > li > a')
        # 5、获取所在频道
        channel=get_card_info[0].text.encode('utf-8')
        # 6、获取所在目录
        dir_text=get_card_info[1].text.encode('utf-8')
        # 7、获取slogan
        get_slogan=bs.select('div.card_top.clearfix > p')
        slogan=get_slogan[0].text
        # 8、获取本吧详细信息链接——【待解决】
        get_det_link=bs.select("h4 > span > a")
        det_link=host_url+get_det_link[0].get('href')
        # 获得吧务团队、本吧会员、本吧会员的信息
        # get_bawu_detials_link(det_link


        print name
        print memNum
        print infoNum
        print channel
        print dir_text
        print slogan
        print det_link
    else:
        print "请求错误，请调试请求~"
        pass



'''
--------------------------------------------------------------------------
方法2说明：获取"本吧信息"中的详细信息页面中的三个模块的链接（吧务团队、吧务候选、本吧会员）
         其中"本吧详情"模块的链接就是传入的参数"detial_link"
参数说明：本参数是从方法1中的得到，是某贴吧主页的右侧"本吧信息"的"查看详情"的链接，所以本
        函数可以搭配方法1才能自动使用，否则需要手动获取"查看详情"的链接
--------------------------------------------------------------------------
'''
def get_bawu_detials_link(detial_link):
    # 获得贴吧的吧务信息——考虑整合到获取贴吧的详细信息函数中
    details_info_url='http://tieba.baidu.com/bawu2/platform/detailsInfo?word=%E4%B8%8A%E6%B5%B7%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8'
    host_url='http://tieba.baidu.com'
    r=requests.get(details_info_url,proxies=proxy,timeout=20)
    if r.status_code==200:
        time.sleep(2)
        bs=BeautifulSoup(r.text,'lxml')
        get_team_info_url=bs.select('div > p > a')
        # 获取吧务团队的链接
        team_info_url=host_url+get_team_info_url[1].get('href')
        # 获得吧务候选的链接
        candidate_info_url=host_url+get_team_info_url[2].get('href')
        # 获得本吧会员的链接
        member_info_url=host_url+get_team_info_url[3].get('href')

        print team_info_url
        print candidate_info_url
        print member_info_url
    else:
        print '请求错误，请调试请求！'
        pass


'''
-------------------------------------------------------------------------
方法3作用：获取某贴吧的吧务团队的所有人链接
         （已实现分类：吧主、小吧主、图片小编、视频小编、吧刊主编、吧刊小编）
参数说明："吧务团队"的链接，来源是由方法2获得。所以本方法需要搭配方法2才可以自动爬取信息，
        否则请自行获取"吧务团队"模块的链接。
-------------------------------------------------------------------------
'''

# 获得吧务团队信息-有错误，待修改
def get_bawu_member_link():
    team_info_url='http://tieba.baidu.com/bawu2/platform/listBawuTeamInfo?word=%C9%CF%BA%A3%B9%A4%B3%CC%BC%BC%CA%F5%B4%F3%D1%A7'
    host_url='http://tieba.baidu.com'
    r=requests.get(team_info_url,proxies=proxy,timeout=20)
    if r.status_code==200:
        time.sleep(2)
        bs=BeautifulSoup(r.text,'lxml')
        # 吧主的个人信息链接
        get_bazhu_link=bs.select('div.bawu_single_type.first_section > div.member_wrap.clearfix > span > a.user_name')
        bazhu_length=len(get_bazhu_link)
        # for i in range(0,bazhu_length):
        #     print   host_url+get_bazhu_link[i].get('href')

        #小吧主的个人信息——有问题！继承nth-child（2）解析错误，换解析方式？
        # get_xiaobazhu_link=bs.select('div:nth-child(2) > div.member_wrap.clearfix > span > a.user_name')
        get_xiaobazhu_link = bs.select('a.user_name')
        xiaobazhu_length=len(get_xiaobazhu_link)
        # for j in range(bazhu_length,xiaobazhu_length):
        #     print host_url+get_xiaobazhu_link[j].get('href')

        #图片小编的个人信息链接
        # get_tupianxiaobian_link=get_xiaobazhu_link
        # tupianxiaobian_link=get_tupianxiaobian_link
    else:
        print '请求错误，请修改请求！'
        pass


'''
-------------------------------------------------------------
方法4作用：获取某个贴吧，某一页的所有帖子信息（包括：标题、链接）
参数说明："tieba_name"是打开某个贴吧主页后，浏览器地址栏中"kw="后的汉字
        "page"是想要爬取的页码数
-------------------------------------------------------------
'''
def get_single_page_items_info(tieba_name,page):
    host_url='http://tieba.baidu.com'
    # pn=[pn for pn in range(0,6350,50)]
    payload={'ie':'utf-8','kw':str(tieba_name),'pn':str(page)}
    r=requests.get(host_url+'/f',params=payload,proxies=proxy,timeout=15)
    time.sleep(2)
    if r.status_code==200:
        bs=BeautifulSoup(r.text,'lxml')
        items=bs.select('div.threadlist_title.pull_left.j_th_tit > a')
        item_authors=bs.select('div.col2_right.j_threadlist_li_right > div.threadlist_lz.clearfix > div.threadlist_author.pull_right > span.tb_icon_author > span.frs-author-name-wrap > a')
        item_num=len(items)
        response_num=bs.select('div.col2_left.j_threadlist_li_left > span')
        # item_author_num=len(item_authors)
        for i in range(0,item_num-1):
            # 得到了帖子的标题
            print items[i].text
            # 回帖量
            print (int(response_num[i].text)+1)
            # 得到帖子的链接
            print host_url+'/'+items[i].get('href')
            # 帖子的楼主信息
            print item_authors[i].text
            # 楼主信息的链接
            print (host_url+item_authors[i].get('href'))
            print '\n'
    else:
        print "请求错误，请调试请求！"
        pass


'''
--------------------------------------------------------------
方法5作用：获取某个贴吧，某几页之间的所有帖子信息（包括：标题、链接）
参数说明："tieba_name"是打开某个贴吧主页后，浏览器地址栏中"kw="后的汉字
        "beginPage"是想要爬取的起始页码数
        "endPage"是想要爬取的结尾页码数
--------------------------------------------------------------
'''
def get_all_items_info(tieba_name,beginPage,endPage):
    for page in range(50*(beginPage-1),50*endPage,50):
        get_single_page_items_info(str(tieba_name),page)



'''
-------------------------------------------------------------
方法6作用:获取某一篇帖子某一页的所有的楼层评论、评论者所使用的设备信息、评论时间
参数说明："item_link"帖子的链接
        "page"页码数
-------------------------------------------------------------
'''
# 获取每一篇帖子的某一页详细信息以及楼层评论
def get_single_judgement_info(item_link,page):
    payload={'pn':str(page)}
    r=requests.get(item_link,proxies=proxy,timeout=15,params=payload)
    time.sleep(2)
    if r.status_code==200:
        bs=BeautifulSoup(r.text,'lxml')
        # 得到回复内容
        contents=bs.select('div[id*="post_content_"]')
        contents_num=len(contents)
        # 得到发送评论的设备类型-----待修改
        # devices=bs.select('ul.p_mtail > li:nth-child(2) > a')
        # devices=bs.select('a[class="p_tail_wap"]')
        # print len(devices)
        # datas=bs.select('ul.p_tail > li:nth-child(2) > span')

        for i in range(0,contents_num,1):
            print contents[i].text.strip()
            # print devices[i].text
            print '\n'
    else:
        print "请求错误，请调试请求！"
        pass



'''
--------------------------------------------------------------------
方法7作用:获取某一篇帖子某几页之间的所有的楼层评论、评论者所使用的设备信息、评论时间
参数说明："beginPage"起始页码
        "endPage"结尾页码
--------------------------------------------------------------------
'''

# 获取某个帖子某页之前的所有楼层评论
def get_all_judgement_info(item_link,beginPage,endPage):
    for page in range(beginPage,endPage+1,1):
        get_single_judgement_info(item_link,page)

# item_link='http://tieba.baidu.com/p/4372736094'
# beginPage=1
# endPage=2
# get_all_judgement_info(item_link,beginPage,endPage)


# 获取用户个人信息页的信息




