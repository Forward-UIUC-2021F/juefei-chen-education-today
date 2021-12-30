from get_html import get_html, parse_scraped_html, parse_html_string
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import json
import random


class Node:
    def __init__(self, parent, tag, text):
        self.parent = parent
        self.tag = tag
        self.text = text
        self.children = []


def get_experience(html):
    res = []
    tag_stack = []
    education_area = False
    cur_education = []
    root = Node(None, '', '')
    for line in html:
        if 'pv-entity__position-group-pager pv-profile-section__list-item ember-view' in line:
            education_area = True
        if education_area:
            if line[:4] == '<img' or line[:3] == '<br' or line[:2] == '<!':
                continue
            if len(line) > 2 and line[:2] == '</':
                tag_stack.pop()
                if not tag_stack:
                    res.append(cur_education)
                    cur_education = []
                    education_area = False
            elif len(line) > 2 and line[:1] == '<' and line[1] != '!':
                if 'visually-hidden' in line:
                    tag_stack.append('<span class="visually-hidden">')
                else:
                    tag_stack.append(line.split()[0] + '>')
            else:
                tmp = line.replace('\n', '').replace(' ', '')
                if not tmp or line[:2] == '<!' or 'visually-hiddenssss' in tag_stack[-1]:
                    continue
                print(line.strip(), len(tag_stack))
                cur_education.append(line.strip())
    return res


def get_education(html):
    res = []
    tag_stack = []
    education_area = False
    cur_education = []
    for line in html:
        if 'pv-profile-section__list-item pv-education-entity pv-profile-section__card-item ember-view' in line:
            education_area = True
        if education_area:
            if line[:4] == '<img' or line[:3] == '<br' or line[:2] == '<!':
                continue
            if len(line) > 2 and line[:2] == '</':
                tag_stack.pop()
                if not tag_stack:
                    res.append(cur_education)
                    cur_education = []
                    education_area = False
            elif len(line) > 2 and line[:1] == '<' and line[1] != '!':
                if 'visually-hidden' in line:
                    tag_stack.append('<span class="visually-hidden">')
                else:
                    tag_stack.append(line.split()[0] + '>')
            else:
                tmp = line.replace('\n', '').replace(' ', '')
                if not tmp or line[:2] == '<!' or 'visually-hiddensss' in tag_stack[-1]:
                    continue
                cur_education.append(line.strip())
    return res


def get_education_background_on_linkedin(urls):
    option = webdriver.ChromeOptions()

    option.add_argument(' — incognito')
    option.add_argument('--no - sandbox')
    option.add_argument('--window - size = 1420, 1080')
    option.add_argument('--headless')
    option.add_argument('--disable - gpu')

    option.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54')
    driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver', chrome_options=option)
    driver.get('https://www.linkedin.com/')
    time.sleep(1)
    inputElement = driver.find_element_by_id('session_key')
    inputElement.send_keys('1787925970@qq.com')
    time.sleep(2)
    inputElement = driver.find_element_by_id('session_password')
    inputElement.send_keys('qwemnbzxcpoi')
    time.sleep(2)
    submit_button = driver.find_elements_by_xpath('/html/body/main/section[1]/div/div/form/button')[0]
    submit_button.click()
    time.sleep(3)

    res = []
    count = 0
    for url in urls:
        count += 1
        print(url)
        driver.get(url)
        time.sleep(3)
        html_string = str(driver.page_source)
        t = parse_html_string(html_string)

        f = get_education(t)
        for i in f:
            print(i)
        f = get_experience(t)
        for i in f:
            print(i)

        r = []
        for i in range(len(t)):
            if t[i] == '<h3 class="pv-entity__school-name t-16 t-black t-bold">':
                r.append(t[i + 1])
                print(url, t[i + 1])

        time.sleep(random.randint(10, 15))
        # time.sleep(60)
        print()
        res.append(r)
        if count % 23 == 0:
            time.sleep(random.randint(300, 600))
    driver.quit()
    return res


urls = [
    'https://www.linkedin.com/in/juefei-chen-b9413b188/',
    'https://www.linkedin.com/in/kcchang/'
]
get_education_background_on_linkedin(urls)


# f = open('linkedin_urls.json')
# t = json.load(f)
# urls = []
# for i, j in t:
#     urls.append(j)
# r = get_education_background_on_linkedin(urls)
# res = []
# for i in range(len(t)):
#     res.append([t[i][0], t[i][1], {'education': r[i]}])
# with open('education_background/uiuc_cs.json', 'w') as outfile:
#     json.dump(res, outfile, indent=4)
