import time
import string
import urllib.request
from selenium import webdriver
import os
import urllib.request
import re


def get_html(url, scrape_option, headers={}):
    if scrape_option == 'urllib':
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
            the_page = (str(the_page))
        except:
            return []
    else:
        try:
            option = webdriver.ChromeOptions()
            option.add_argument(' — incognito')
            option.add_argument('--no - sandbox')
            option.add_argument('--window - size = 1420, 1080')
            option.add_argument('--headless')
            option.add_argument('--disable - gpu')
            driver1 = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver',
                                       options=option)
            driver1.get(url)
            time.sleep(1)
            the_page = str(driver1.page_source)
            # print(the_page)
            time.sleep(2)
        except:
            return []
    return parse_html_string(the_page)


def parse_html_string(html):
    result = []
    line = ""
    for i in html:
        if i == '<':
            if len(line) != 0:
                result.append(line)
            line = "<"
        elif i == '>':
            line += '>'
            result.append(line)
            line = ""
        else:
            line += i
    result.append(line)
    return result


def parse_scraped_html(html):
    raw_html = []
    for j in range(len(html)):
        i = html[j]
        i = i.replace('\\n', '')
        i = i.replace('\\t', '')
        i = i.replace('\\r', '')
        i = i.replace('&nbsp;', '')
        while '  ' in i:
            i = i.replace('  ', ' ')
        if len(i) == 0 or i == ';':
            i = ' '
        if i != ' ' and i[0] != '<' and 0 < j < len(html) - 1 and (
                html[j + 1][:2] != '</' or html[j - 1][:2] == '</' or html[j - 1][:3] == '<br'):
            a = i.strip()
            if a in string.punctuation:
                continue
            raw_html.append('<no_tag>')
            raw_html.append(i)
            raw_html.append('</no_tag>')
        else:
            raw_html.append(i)
    return raw_html


def get_links_on_google(query, forbidden=[]):
    possibleURLs = []
    url = 'https://www.google.com/search?q=' + query.replace(' ', '+').replace('/', "%2F").replace('–', '')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.google.com/'})
    with urllib.request.urlopen(req) as response:
        r = response.read()
    plaintext = r.decode('utf8')
    links = re.findall("href=[\"\'](.*?)[\"\']", plaintext)
    for i in links:
        k = '/url?q=http'
        flag = True
        for j in forbidden:
            if j in i:
                flag = False
        if len(i) > len(k) and i[:len(k)] == k and flag:
            link = i[7:].split('&amp')[0]
            link = urllib.parse.unquote(link)
            possibleURLs.append(link)
    return possibleURLs


# a = get_html('https://cs.illinois.edu/about/people/all-faculty', 's')
# print(a)