import time
import string
import urllib.request
from selenium import webdriver
import os
import json
import sys

sys.path.insert(1, '../helper')

from get_html import get_html, parse_scraped_html, parse_html_string, get_links_on_google

# extract information on orcid
def get_info(url):
    option = webdriver.ChromeOptions()

    option.add_argument(' — incognito')
    option.add_argument('--no - sandbox')
    option.add_argument('--window - size = 1420, 1080')
    option.add_argument('--headless')
    option.add_argument('--disable - gpu')

    option.add_argument('Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
    driver = webdriver.Chrome(executable_path=os.getcwd() + '/../chromedriver', chrome_options=option)

    driver.get(url)
    time.sleep(2)
    html_string = str(driver.page_source)
    html = parse_html_string(html_string)

    res = []
    tag_stack = []
    target_region = False
    cur_background = []
    cur_info = ''
    add_text = False
    for line in html:
        line = ' '.join(line.split())
        if len(line) == 0 or line[:2] == '<!':
            continue
        if line[:11] == '<app-panel ':
            tag_stack.append('<app-panel>')
            target_region = True
            add_text = True
            continue
        if not target_region:
            continue
        if line[0] == '<' and line[:2] != '</':
            tag_stack.append(line)
        if line[0] != '<' and add_text:
            if line == 'Show more detail':
                add_text = False
                continue
            if tag_stack and 'class="type"' in tag_stack[-1] and not cur_info:
                cur_background.append({'type': line})
            else:
                cur_info += line + ' '
        if line[:2] == '</':
            if cur_info:
                cur_background.append(cur_info[:-1])
                cur_info = ''
            tag_stack.pop()
            if not tag_stack:
                res.append(cur_background.copy())
                cur_background = []
                target_region = False

    for i in res:
        print(i)
    with open('data.json', 'w') as outfile:
        json.dump(res, outfile, indent=4, ensure_ascii=False)
    return res


# get faculty's background on orcid
# see return format in data.json
def get_background_on_orcid(name):
    urls = get_links_on_google(name + ' orcid')
    for url in urls:
        if 'https://orcid.org/' in url:
            return get_info(url)


# get_info('https://orcid.org/0000-0002-9241-2357')
# get_info('https://orcid.org/0000-0002-4237-5412')
# get_info('https://orcid.org/0000-0003-1106-7190')

# example
get_background_on_orcid('Abdussalam Alawini')
