# -*- coding: utf-8 -*-
import os
import json
import urllib.request
from get_data_from_multiple_lists import view_html_structure
from scrape_inst_names import InstitutionScraper

import re
import urllib.parse
import argparse

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

    res_data = {}
    res_url = ''

    for url in possibleURLs:
        for option in ['urllib', 'urllibs']:
            try:
                r = view_html_structure(url, option)
            except:
                continue

            if len(r) > 1:
                return r, url

    return res_data, res_url

def save_and_cleanup(department, university, res_data):
    with open('./results/{}-{}-faculty-info.json'.format(university, department), 'w+') as fp:
        fp.write(json.dumps(res_data, indent = 4))

    # removing intermediate txt files
    os.remove('./html_structure.txt')
    os.remove('./raw_html.txt')


def parse_args():
    parser = argparse.ArgumentParser(description="Run baselines.")

    parser.add_argument('--url', type=str, help='The USAToday url for instituions.')
    parser.add_argument('--raw_html', type=str, help='The raw html of the USAToday page for instituions.')
    parser.add_argument('--department', type=str,
                        help='Department name within the university.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    url = args.url
    raw_html = args.raw_html
    department = args.department
    universities = []

    if((url == None and raw_html != None) or (url != None and raw_html == None)):
        scraper = InstitutionScraper()
        scraper.scrape(url, raw_html, department)

        with open('./results/top_{}_univs.csv'.format(department)) as fp:
            for line in fp:
                universities.append(line.strip().split(',')[1].strip('\''))
    

    for university in set(universities):
        print('Fecthing information for department = {} of university = {}'.format(department, university))

        data, url = find(university, department)
        save_and_cleanup(department, university, data)
