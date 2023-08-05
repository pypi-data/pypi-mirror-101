# -*- coding: utf8 -*-

import os
import re
import sys
import traceback
import urllib.request
import json
from pyquery import PyQuery
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)
from util.pub_fun import Pub_fun



class BaiduPcExtractor:
    def __init__(self):
        super().__init__()
        self.pub_fun = Pub_fun()

    def baidu_pc_extractor(self, html ,page, spidertype=1):
        """
        百度pc端解析器
        :param html:
        :param page: 第几页
        :param spidertype: 1不抓真实url 2:获取真实url
        :return: {
            'html_status' : -1(页面dom异常或有验证)  1：页面正常，
            'data_list' : [
                {
                    "rank": 1,
                    "title": title,
                    "show_url": show_url,
                    "real_url": real_url,
                    "desc": desc,
                    "sub_rank_data": [
                        "sub_rank": 1,"show_url": show_url, "title": title, "real_url": real_url,
                        "sub_rank": 2,"show_url": show_url, "title": title, "real_url": real_url,
                        "sub_rank": 3,"show_url": show_url, "title": title, "real_url": real_url,
                    ]
                }
            ]
        }
        """

        print('开始解析 百度pc端 列表页')
        result = {}
        result['html_status'] = self.check_html_dom(html)
        result['data_list'] = self.get_data_list(result, html, page, spidertype)

        return result

    def check_html_dom(self, html):
        """
        判断pc端dom元素是否异常
        :return:  正常返回1  异常返回-1
        """
        try:
            if html.find("</html>") < 0 or html.find('id="wrap"') >= 0 or (
                    "<title>百度App</title>" in html and "拦截通用" in html) or (
                    "<title>百度安全验证</title>" in html and "百度安全验证" in html) or html.find('页面不存在_百度搜索') >= 0 or html.find(
                'id="container"') < 0 or html.find('id="content_left"') < 0 or html.find('<title>') < 0:
                return -1
            else:
                return 1
        except Exception:
            print(traceback.format_exc())
            html_status = -1
        return html_status

    def get_data_list(self, result, html, page, spidertype):
        """
        获取百度列表数据
        :param result:
        :param html:
        :return:
        """
        data_list = []
        if result['html_status'] != 1:
            return data_list
        try:
            query = PyQuery(html, parser='html')
            containers = query('#content_left>.c-container')
            if len(containers) == 0:
                return data_list

            increase_rank = self.get_page_start_rank(page)
            for container in containers.items():
                item_rank_data = {}
                increase_rank += 1 # 递增排名(参考)
                # 1: 普通格式 class参考result c-container new-pmd "tpl": 'se_com_default',
                if container.has_class('result'):
                    item_rank_data = self.get_normal_rank_data(container, increase_rank, spidertype)
                # 2: 最新相关信息 class参考result-op c-container new-pmd xpath-log tpl="sp_realtime_bigpic5"
                if container.has_class('result-op') and container.attr('tpl') == 'sp_realtime_bigpic5':
                    item_rank_data = self.get_latest_news_rank_data(container, increase_rank, spidertype)
                # 3: 百度百科 class参考 result-op c-container new-pmd             tpl="bk_polysemy"
                if container.has_class('result-op') and container.attr('tpl') == 'bk_polysemy':
                    item_rank_data = self.get_baike_rank_data(container, increase_rank, spidertype)
                # 4: 百度视频 class参考 result-op c-container new-pmd xpath-log   tpl="short_video_pc"
                if container.has_class('result-op') and container.attr('tpl') == 'short_video_pc':
                    item_rank_data = self.get_video_rank_data(container, increase_rank, spidertype)
                # 5: 百度图片 class参考 result-op c-container new-pmd xpath-log   tpl="img_address"
                if container.has_class('result-op') and container.attr('tpl') == 'img_address':
                    item_rank_data = self.get_img_rank_data(container, increase_rank, spidertype)
                # 6: 百度贴吧 class参考 result-op c-container new-pmd xpath-log   tpl="tieba_general"   # 带图贴吧多条
                if container.has_class('result-op') and container.attr('tpl') == 'tieba_general':
                    item_rank_data = self.get_tieba_rank_data(container, increase_rank, spidertype)
                # 7: 其他人也在搜 class参考 result-op c-container new-pmd         tpl="recommend_list"
                if container.has_class('result-op') and container.attr('tpl') == 'recommend_list':
                    item_rank_data = self.get_recommend_rank_data(container, increase_rank, spidertype)
                # 品牌官网 ， 快手-W[01024]港股实时行情 - 富途牛牛
                print(item_rank_data)
                if len(item_rank_data) == 0:
                    continue
                data_list.append(item_rank_data)
            return data_list
        except Exception:
            print(traceback.format_exc())
            return data_list

    def get_normal_rank_data(self, container, increase_rank, spidertype):
        """
        获取常规模式百度列表单条数据内容
        :return:
        """
        try:
            rank_data = {
                "rank": self.get_item_rank(container, increase_rank),
                "title": self.get_item_title(container),
                'desc': self.get_normal_item_desc(container),
                'show_url': self.get_normal_item_show_url(container),
                'baidu_url': self.get_item_baidu_url(container),
                "sub_rank_data": [],
                "tpl": 'se_com_default',
            }
            real_url = self.get_normal_item_real_url(rank_data['show_url'], rank_data['baidu_url'], spidertype)
            domain = self.get_item_domain(rank_data['show_url'], real_url)
            rank_data['real_url'] = real_url
            rank_data['domain'] = domain

            return rank_data
        except Exception:
            print(traceback.format_exc())
            return []

    def get_baike_rank_data(self, container, increase_rank, spidertype):
        """
        百度百科
        :return:
        """
        try:
            rank_data = {
                "rank": self.get_item_rank(container, increase_rank),
                "title": self.get_item_title(container),
                'desc': container('.op-bk-polysemy-piccontent').text(),
                'show_url': self.get_normal_item_show_url(container),
                'baidu_url': self.get_item_baidu_url(container),
                "sub_rank_data": [],
                "tpl": "bk_polysemy"
            }
            real_url = self.get_normal_item_real_url(rank_data['show_url'], rank_data['baidu_url'], spidertype)
            domain = self.get_item_domain(rank_data['show_url'], real_url)
            rank_data['real_url'] = real_url
            rank_data['domain'] = domain

            return rank_data
        except Exception:
            print(traceback.format_exc())
            return []

    def get_latest_news_rank_data(self, container, increase_rank, spidertype):
        """
        获取最新相关信息
        :return:
        """
        try:
            rank_data = {
                "rank": self.get_item_rank(container, increase_rank),
                "title": self.get_item_title(container),
                'desc': '',
                'show_url': '',
                'real_url': '',
                'domain': '',
                'baidu_url': self.get_item_baidu_url(container),
                "sub_rank_data": self.get_news_item(container, spidertype),
                "tpl": "sp_realtime_bigpic5"
            }
            return rank_data
        except Exception:
            print(traceback.format_exc())
            return []

    def get_video_rank_data(self, container, increase_rank, spidertype):
        """
        获取百度视频
        :return:
        """
        try:
            rank_data = {
                "rank": self.get_item_rank(container, increase_rank),
                "title": self.get_item_title(container),
                'desc': '',
                'show_url': '',
                'real_url': '',
                'domain': '',
                'baidu_url': self.get_item_baidu_url(container),
                "sub_rank_data": self.get_video_item(container, spidertype),
                "tpl": "short_video_pc"
            }
            return rank_data
        except Exception:
            print(traceback.format_exc())
            return []

    def get_img_rank_data(self, container, increase_rank, spidertype):
        """
        获取百度图片
        :return:
        """
        try:
            rank_data = {
                "rank": self.get_item_rank(container, increase_rank),
                "title": self.get_item_title(container),
                'desc': '',
                'show_url': self.get_normal_item_show_url(container),
                'real_url': '',
                'baidu_url': self.get_item_baidu_url(container),
                "sub_rank_data": self.get_img_item(container, spidertype),
                "tpl": "img_address"
            }
            domain = self.get_item_domain(rank_data['show_url'], rank_data['show_url'])
            rank_data['domain'] = domain
            return rank_data
        except Exception:
            print(traceback.format_exc())
            return []

    def get_tieba_rank_data(self, container, increase_rank, spidertype):
        """
        获取百度贴吧
        :return:
        """
        try:
            rank_data = {
                "rank": self.get_item_rank(container, increase_rank),
                "title": self.get_item_title(container),
                'desc': '',
                'show_url': container('.c-showurl .c-showurl').text(),
                'baidu_url': self.get_item_baidu_url(container),
                "sub_rank_data": self.get_tieba_item(container, spidertype),
                "tpl": "tieba_general"
            }
            real_url = self.get_normal_item_real_url(rank_data['show_url'], rank_data['baidu_url'], spidertype)
            domain = self.get_item_domain(rank_data['show_url'], real_url)
            rank_data['real_url'] = real_url
            rank_data['domain'] = domain
            return rank_data
        except Exception:
            print(traceback.format_exc())
            return []

    def get_recommend_rank_data(self, container, increase_rank, spidertype):
        """
        其他人还在搜
        :return:
        """
        try:
            rank_data = {
                "rank": self.get_item_rank(container, increase_rank),
                "title": container('.c-font-medium:first').text(),
                'desc': '',
                'show_url': '',
                'baidu_url': '',
                "sub_rank_data": self.get_recommend_item(container, spidertype),
                "tpl": "recommend_list"
            }
            real_url = self.get_normal_item_real_url(rank_data['show_url'], rank_data['baidu_url'], spidertype)
            domain = self.get_item_domain(rank_data['show_url'], real_url)
            rank_data['real_url'] = real_url
            rank_data['domain'] = domain
            return rank_data
        except Exception:
            print(traceback.format_exc())
            return []

    def get_news_item(self, container, spidertype):
        '''
        最新消息
        "sub_rank_data": [
            "sub_rank": 1,"show_url": show_url, "title": title, "real_url": real_url,
        ]
        :param container:
        :return:
        '''
        try:
            sub_rank_data = []
            c_rows = container('.c-row')
            if len(c_rows) == 0:
                return []
            sub_index = 1
            for c_row in c_rows.items():
                if c_row.has_class('c-color-text'): # top1的描述
                    continue
                item = {
                    "rank": sub_index,
                    "title": c_row('a').text(),
                    'desc': '',
                    'show_url': c_row('.op_sp_realtime_bigpic5_left').text(),
                    'baidu_url': c_row('a').attr('href'),
                }
                item['real_url'] = self.get_normal_item_real_url(item['show_url'], item['baidu_url'], spidertype)
                item['domain'] = self.get_item_domain(item['show_url'], item['real_url'])
                sub_index += 1
                sub_rank_data.append(item)
            return sub_rank_data
        except Exception:
            print(traceback.format_exc())
            return []

    def get_tieba_item(self, container, spidertype):
        '''
        贴吧
        "sub_rank_data": [
            "sub_rank": 1,"show_url": show_url, "title": title, "real_url": real_url,
        ]
        :param container:
        :return:
        '''
        try:
            sub_rank_data = []
            c_rows = container('.c-container > .c-row')
            if len(c_rows) == 0:
                return []
            sub_index = 1
            for c_row in c_rows.items():
                if c_row.has_class('c-gap-top-small'): # top1的描述
                    continue
                item = {
                    "rank": sub_index,
                    "title": c_row('a').text(),
                    'desc': '',
                    'show_url': '',
                    'baidu_url': c_row('a').attr('href'),
                }
                item['real_url'] = self.get_normal_item_real_url(item['show_url'], item['baidu_url'], spidertype)
                item['domain'] = self.get_item_domain(item['show_url'], item['real_url'])
                sub_index += 1
                sub_rank_data.append(item)
            return sub_rank_data
        except Exception:
            print(traceback.format_exc())
            return []

    def get_recommend_item(self, container, spidertype):
        '''
        其他人还在搜
        "sub_rank_data": [
            "sub_rank": 1,"show_url": show_url, "title": title, "real_url": real_url,
        ]
        :param container:
        :return:
        '''
        try:
            sub_rank_data = []
            c_rows = container('.c-gap-top-xsmall')
            if len(c_rows) == 0:
                return []
            sub_index = 1
            for c_row in c_rows.items():
                item = {
                    "rank": sub_index,
                    "title": c_row('a').text(),
                    'desc': '',
                    'show_url': '',
                    'baidu_url': 'https://www.baidu.com' + c_row('a').attr('href'),
                }
                item['real_url'] = self.get_normal_item_real_url(item['show_url'], item['baidu_url'], spidertype)
                item['domain'] = self.get_item_domain(item['show_url'], item['real_url'])
                sub_index += 1
                sub_rank_data.append(item)
            return sub_rank_data
        except Exception:
            print(traceback.format_exc())
            return []

    def get_video_item(self, container, spidertype):
        '''
        百度视频
        "sub_rank_data": [
            "sub_rank": 1,"show_url": show_url, "title": title, "real_url": real_url,
        ]
        :param container:
        :return:
        '''
        try:
            sub_rank_data = []
            c_rows = container('.c-span3')
            if len(c_rows) == 0:
                return []
            sub_index = 1
            for c_row in c_rows.items():
                item = {
                    "rank": sub_index,
                    "title": c_row('.op-short-video-pc-title-new').text(),
                    'desc': '',
                    'show_url': c_row('.op-short-video-pc-clamp1').text(),
                    'baidu_url': '',
                    'real_url': c_row('a:first').attr('href'),
                }
                item['domain'] = self.get_item_domain(item['show_url'], item['real_url'])
                sub_index += 1
                sub_rank_data.append(item)
            return sub_rank_data
        except Exception:
            print(traceback.format_exc())
            return []

    def get_img_item(self, container, spidertype):
        '''
        百度图片
        "sub_rank_data": [
            "sub_rank": 1,"show_url": show_url, "title": title, "real_url": real_url,
        ]
        :param container:
        :return:
        '''
        try:
            sub_rank_data = []
            c_rows = container('.op-img-address-link-type')
            if len(c_rows) == 0:
                return []
            sub_index = 1
            for c_row in c_rows.items():
                item = {
                    "rank": sub_index,
                    'baidu_url': c_row.attr('href'),
                    'src': c_row('img').attr('src'),
                    "title": '',
                    'desc': '',
                    'show_url': '',
                    'real_url': '',
                    'domain': '',
                }
                sub_index += 1
                sub_rank_data.append(item)
            return sub_rank_data
        except Exception:
            print(traceback.format_exc())
            return []


    def get_item_title(self, container):
        """
        解析标题
        :param container:
        :return:
        """
        title = ''
        try:
            title = container('h3 a').text()
        except Exception:
            print(traceback.format_exc())
        return title

    def get_item_domain(self, show_url, real_url):
        """
        根据url获取domain
        :param container:
        :return:
        """
        domain = ''
        try:
            domain = self.pub_fun.get_top_domain(real_url)
            if domain == '':
                domain = self.pub_fun.get_top_domain(show_url)
        except Exception:
            print(traceback.format_exc())
        return domain

    def get_normal_item_desc(self, container):
        """
        解析描述
        :param container:
        :return:
        """
        desc = ''
        try:
            desc = container('.c-abstract').text()
        except Exception:
            print(traceback.format_exc())
        return desc

    def get_item_baidu_url(self, container):
        """
        解析baidu_url
        :param container:
        :return:
        """
        baidu_url = ''
        try:
            baidu_url = container('h3 a').attr('href')
        except Exception:
            print(traceback.format_exc())
        return baidu_url

    def get_normal_item_show_url(self, container):
        """
        解析show_url
        :param container:
        :return:
        """
        show_url = ''
        try:
            if container('.c-showurl style').text() != '':
                # 中文
                container.remove('style')
            show_url = container('.c-showurl').text()
        except Exception:
            print(traceback.format_exc())
        return show_url

    def get_normal_item_real_url(self, show_url, baidu_url, spidertype):
        """
        解析real_url   如果显示url是中文 || spidertype==2
        :return:
        """
        real_url = ''
        try:
            if not self.pub_fun.is_valid_domain(show_url) or spidertype == 2:
                real_url = self.findReal_Address_improve(baidu_url)
        except Exception:
            print(traceback.format_exc())
        return real_url


    def findReal_Address_improve(self,baidu_url, cur_time=6):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                }
            request = urllib.request.Request(url=baidu_url,headers=headers)
            response = urllib.request.urlopen(request,timeout=cur_time)
            real_url = response.url
            return real_url
        except:
            return ""


    def get_item_rank(self, container, increase_rank):
        """
        解析排名
        :param container:
        :return:
        """
        try:
            rank = container.attr('id')
        except Exception:
            print(traceback.format_exc())
            rank = increase_rank
        return rank

    def get_page_start_rank(self, page):
        """
        根据初始页码计算第一条排名
        :param page:
        :return:
        """
        try:
            limit = 10
            return (page - 1) * limit
        except Exception:
            return 0


if __name__ == '__main__':

    b = BaiduPcExtractor()
    file_path = 'test_pc.html'.format(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    content = open(file_path, 'r', encoding='utf-8')
    html = content.read()
    content.close()

    l_s = b.baidu_pc_extractor(html,spidertype=2,  page=1)