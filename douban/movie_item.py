import re
import json
import urllib
import requests
import os
import time
import selenium.webdriver as wd
from selenium.webdriver.chrome.options import Options
from PIL import Image as im


class Douban(object):

    def __init__(self, url):
        """
        初始化item页信息
        :param url: 需要抓取的豆瓣电影页
        """
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--headless')
        self.target_url = url
        if not os.path.exists('./'):
            os.mkdir('./src')
        self.driver = wd.Chrome(chrome_options=chrome_options)
        self.driver.maximize_window()
        self.driver.get(url)
        # with open('./src/item_page.html', 'w', encoding='utf-8') as f:
            # f.write(self.driver.page_source)
        # self.driver.close()
        # with open('./src/item_page.html', 'r', encoding='utf-8') as f:
            # self.html = f.read()
        self.html = self.driver.page_source
        self.data = {}
        # self.basic_dir = os.path.abspath('./')
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

    def init_data(self):
        """
        初始化部分电影信息
        :return:
        """
        # 获取item名称
        _name_reg = re.compile(
            r'<span property="v:itemreviewed">(.*?)</span>', re.S)
        self.data['movie_name'] = re.findall(_name_reg, self.html)[0]

        # 获取item发布年份
        _released_year_reg = re.compile(
            r'<span class="year">\((.*?)\)</span>', re.S)
        self.data['released_year'] = re.findall(
            _released_year_reg, self.html)[0]

        # 获取item海报url
        _posters_url_reg = re.compile(
            r'<a class="nbgnbg" href="(.*?)" title="点击看更多海报">', re.S)
        self.data['posters'] = re.findall(_posters_url_reg, self.html)
        # 获取item主创姓名
        _main_team_reg = re.compile(r'<a.*?>(.*?)</a>', re.S)
        for line in self.html.split('\n'):
            if '<span class="pl">导演</span>' in line:
                self.data['director'] = re.findall(_main_team_reg, line)
            elif '<span class="pl">编剧</span>' in line:
                self.data['screenwriter'] = re.findall(_main_team_reg, line)
            elif '<span class="pl">主演</span>' in line:
                self.data['actor'] = re.findall(_main_team_reg, line)[:-1]

        # 获取item类型
        _type_reg = re.compile(r'<span property="v:genre">(.*?)</span>', re.S)
        self.data['type'] = re.findall(_type_reg, self.html)

        # 获取item发行地
        _state_reg = re.compile(
            r'<span class="pl">制片国家/地区:</span>(.*?)<br>', re.S)
        self.data['state'] = [item.strip()
                              for item in re.findall(_state_reg, self.html)]

        # 获取item发行时间
        _released_time_reg = re.compile(
            r'initialReleaseDate.*?>([\d]{4}-[\d]{2}-[\d]{2})\((.*?)\).*?>', re.S)
        self.data['released_time'] = [{item[-1]: item[0]}
                                      for item in re.findall(_released_time_reg, self.html)]

        # 获取item简介
        _summary_reg = re.compile(r'v:summary.*?>(.*?)<br>(.*?)</span>', re.S)
        self.data['summary'] = '\t' + '\n\t'.join([''.join(element) for element in [re.split(
            r'[\s]', item) for item in re.findall(_summary_reg, self.html)[0]]])

        # 获取item主创名
        _main_team_name_reg = re.compile(
            r'<li class="celebrity">.*?<div class="avatar".*?url\((.*?)\).*?<a href.*?class="name">(.*?)<.*?class="role".*?>(.*?)<',
            re.S)
        self.data['main_team_info'] = [{'name': item[1], 'role': ' '.join(item[-1].split(' ')[1:]) if len(
            item[-1].split(' ')) != 1 else item[-1], 'avatar': item[0]} for item in
                                       re.findall(_main_team_name_reg, self.html)]

        # 获取item剧照url
        # _poster_url_reg = re.compile(
        #     r'<div id="related-pic".*?添加.*?<a href="(.*?/all_photos)?">图片', re.S)
        # self.data['stills'] = re.findall(_poster_url_reg, self.html)
        self.data['stills'] = self.data['posters'][0][:-1] + 'S'

    def build_dir(self):
        """
        为电影创建目录结构
        .
        +-- movie_item.py
        +-- movie_name/
        |   +-- main_team/
        |   +-- posters/
        |   +-- stills/
        |   +-- movie_name_info.json

        :return:
        """
        # if not os.path.exists('./item_src'):
            # os.mkdir('./item_src')
        # self.basic_dir = os.path.abspath('./item_src')
        # os.chdir(self.basic_dir)
        # if ':' not in self.data['movie_name'] and '：' not in self.data['movie_name']:
            # _dir_name = self.data['movie_name']
        # else:
            # _dir_name = ''.join(self.data['movie_name'].split(':'))
        _dir_name = self.data['movie_name'].split('：')[0].split(':')[0].split('？')[0].split('?')[0]
        if not os.path.exists(f'./{_dir_name}'):
            os.mkdir(_dir_name)
        os.chdir(os.path.abspath(f'./{_dir_name}'))
        self.item_abs_path = os.path.abspath('./')
        for dir_name in ['./posters', './main_team', './stills']:
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
        # if not os.path.exists('./posters'):
        #     os.mkdir('./posters')
        # elif not os.path.exists('./main_team'):
        #     os.mkdir('./main_team')
        # elif not os.path.exists('./stills'):
        #     os.mkdir('./stills')

    def webp_2_png(self, bname, aname):
        """
        webp 转 jpg
        :param bname: 转换前文件名，可以包含路径
        :param aname: 转换后文件名，可以包含路径
        :return:
        """
        im.open(bname).save(aname)
        os.remove(bname)

    def download(self, type, name, url):
        """
        下载页面图片
        :param type: 图片分类
        :param name: 图片名
        :param url: 图片url
        :return:
        """
        res = requests.get(url, headers=self.header)
        if res.status_code == 200:
            with open(f'./{type}/{name}.webp', 'wb') as w:
                w.write(res.content)
            self.webp_2_png(f'./{type}/{name}.webp', f'./{type}/{name}.png')

    def get_element_page(self, url):
        """
        获取跳转页html
        :param url: 需要获取的跳转页url
        :return:
        """
        self.driver.get(url)
        return self.driver.page_source

    def download_poster(self):
        """
        下载电影海报（部分）
        :return:
        """
        _count = 0
        _poster_url = self.data['posters'][0]
        _poster_page = self.get_element_page(_poster_url)
        _poster_url_reg = re.compile(
            r'<li.*?<div class="cover".*?<a href.*?<img src="(.*?)">.*?class="prop".*?(\d+x\d+).*?</div>', re.S)
        self.data['poster_urls'] = [{'url': item[0], 'pixel': item[-1]}
                                    for item in re.findall(_poster_url_reg, _poster_page)]
        for item in self.data['poster_urls']:
            _count += 1
            self.download(
                'posters', f'poster-{str(_count)}-{item["pixel"]}', item['url'])

    def download_main_team_pic(self):
        """
        下载电影主创人员图片
        :return:
        """
        for item in self.data['main_team_info']:
            self.download('main_team', item['name'], item['avatar'])

    def download_stills(self):
        """
        下载电影剧照（部分）
        :return:
        """
        _count = 0
        _stills_url = self.data['stills']
        _stills_page = self.get_element_page(_stills_url)
        _stills_url_reg = re.compile(
            r'<li.*?<div class="cover".*?<a href.*?<img src="(.*?)">.*?class="prop".*?(\d+x\d+).*?</div>', re.S)
        self.data['stills_urls'] = [{'url': item[0], 'pixel': item[-1]}
                                    for item in re.findall(_stills_url_reg, _stills_page)]
        for item in self.data['stills_urls']:
            _count += 1
            self.download(
                'stills', f'stills-{str(_count)}-{item["pixel"]}', item['url'])

    def store_item_info(self):
        """
        保存电影信息
        :return:
        """
        with open(f'./{self.data["movie_name"]}.json', 'w', encoding='utf-8') as j:
            j.write(json.dumps(self.data))

    def run(self):
        """
        启动
        :return:
        """
        self.init_data()
        self.build_dir()
        self.download_poster()
        self.download_main_team_pic()
        self.download_stills()
        self.store_item_info()
        os.chdir('../../')
        self.driver.close()


if __name__ == '__main__':
    tmp = Douban(
        r'https://movie.douban.com/subject/27060077/?tag=%E7%83%AD%E9%97%A8&from=gaia_video')
    tmp.run()
    print(json.dumps(tmp.data, indent=4))

    # print(os.path.abspath('./'))
