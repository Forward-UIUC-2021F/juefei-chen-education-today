import time
from selenium import webdriver
import json
import urllib.request
from urllib.request import urlopen
from get_data_from_multiple_lists import view_html_structure
from datetime import datetime
import sys
import re
import urllib.parse
import pickle

forbidden = ['google', 'wiki', 'news', 'instagram', 'twitter', 'linkedin', 'criminal', 'course', 'facebook']


def find(university, department):
    possibleURLs = []
    query = university + ' ' + department
    url = 'https://www.google.com/search?q=' + query.replace(' ', '+').replace('/', "%2F").replace('–', '') + '+faculty'
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

    # for i in possibleURLs:
    #     print(i)

    res_data = {}
    res_url = ''
    res_num = 0

    for url in possibleURLs:
        for option in ['urllib', 'urllibs']:
            # print(option, url)
            try:
                r = view_html_structure(url, option)
            except:
                continue

            if len(r) > 1:
                return r, url
    return res_data, res_url

university = 'uiuc'
department = 'cs'
data, url = find(university, department)
print(data, url)
