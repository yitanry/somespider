import re
import requests
import selenium.webdriver as wd
import header_parser
# driver = wd.Chrome()
# driver.maximize_window()
# driver.get(r'https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0')
# html = driver.page_source
# with open('./tmp/hot_page.html', 'w', encoding='utf-8') as f:
#     f.write(html)
# print(driver.get_cookies())
# driver.close()
basic_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0'

with open('./tmp/header_2', 'r', encoding='utf-8') as f:
    cookies, headers = header_parser.header_parser(f.readlines())
# print(headers)
# print(cookies)
res = requests.get(basic_url, headers=headers, cookies=cookies)
with open('./tmp/all_pages.json', 'w', encoding='utf-8') as w:
    w.write(res.text)
print(res.text)
