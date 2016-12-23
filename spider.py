#coding=utf-8

import time
from bs4 import BeautifulSoup
from userAgents import *
from proxiesList import proxy
import requests

# print bs
print '使用代理IP={}'.format(proxy)


# 获取某个贴吧的信息
def get_tieba_detail_info(tieba_name):
    start_url='http://tieba.baidu.com/f'
    payload={'ie':'utf-8','kw':str(tieba_name)}
    r=requests.get(start_url,params=payload,proxies=proxy,timeout=15)
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
        get_det_link=bs.select("div > h4 > span > a")
        det_link=get_det_link[0].get('href')

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

# http://tieba.baidu.com/f?ie=utf-8&kw=%E4%B8%8A%E6%B5%B7%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6
# &pn=50,100,150....
# b = [i for i in range(1,11)]
# 获取每一页的所有帖子信息：标题、链接、
def get_single_page_items_info(tieba_name,pages):
    host_url='http://tieba.baidu.com'
    # pn=[pn for pn in range(0,6350,50)]
    payload={'ie':'utf-8','kw':str(tieba_name),'pn':str(50*(pages-1))}
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


# 获得某个贴吧某页之前的全部帖子
def get_all_items_info(tieba_name,endPage):
    for page in range(0,50*endPage,50):
        get_single_page_items_info(str(tieba_name),page)

# tieba_name='上海工程技术大学'
# endPage=2
# get_all_items_info(tieba_name,endPage)


# 获取每一篇帖子的某一页详细信息以及楼层评论
def get_single_judgement_info(item_link,endPage):
    payload={'pn':str(endPage)}
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


# item_link='http://tieba.baidu.com/p/4868331742'
# endPage=1
# get_single_judgement_info(item_link,endPage)


# 获取某个帖子某页之前的所有楼层评论
def get_all_judgement_info(item_link,endPage):
    for i in range(1,endPage,1):
        get_single_judgement_info(item_link,endPage)

# item_link='http://tieba.baidu.com/p/4372736094'
# endPage=2
# get_all_judgement_info(item_link,endPage)

