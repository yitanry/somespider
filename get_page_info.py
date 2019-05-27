import re
import json
import requests
import os
import selenium.webdriver as wd
import header_parser
import movie_item
# driver = wd.Chrome()
# driver.maximize_window()
# driver.get(r'https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0')
# html = driver.page_source
# with open('./tmp/hot_page.html', 'w', encoding='utf-8') as f:
#     f.write(html)
# print(driver.get_cookies())
# driver.close()
basic_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start='
all_page_info = []
with open('./tmp/header_2', 'r', encoding='utf-8') as f:
    cookies, headers = header_parser.header_parser(f.readlines())
# print(headers)
# print(cookies)

for num in range(0, 321, 20):
    res = requests.get(basic_url + str(num), headers=headers, cookies=cookies)
    if res.status_code == 200:
        # with open('./tmp/all_pages.json', 'w', encoding='utf-8') as w:
            # w.write(res.text)
        data = json.loads(res.text)['subjects']
        for item in data:
            os.chdir('./item_src')
            tmp = movie_item.Douban(item['url'])
            tmp.run()