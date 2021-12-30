from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import json
import random
import sys
from get_background import get_experience, get_education

sys.path.insert(1, '../helper')

from get_html import parse_html_string, get_links_on_google


# name_list: a list of names
# university: university of faculty members
# linkedin_email: email address used to log in a linkedin account
# linkedin_password: password used to log in a linkedin account
# this function first log in with linkedin_email and linkedin_password so we can get access to full profiles on linkedin
#
# return: {
#   faculty1: {'education': [...], 'experience': [...]},
#   faculty2: {'education': [...], 'experience': [...]},
#   ...
# }
def get_background_on_linkedin(name_list, university, linkedin_email, linkedin_password):
    option = webdriver.ChromeOptions()

    option.add_argument(' — incognito')
    option.add_argument('--no - sandbox')
    option.add_argument('--window - size = 1420, 1080')
    option.add_argument('--headless')
    option.add_argument('--disable - gpu')

    # option.add_argument('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45')
    option.add_argument('Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
    driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver', chrome_options=option)
    driver.get('https://www.linkedin.com/')
    time.sleep(1)
    inputElement = driver.find_element_by_id('session_key')
    for i in linkedin_email:
        inputElement.send_keys(i)
        time.sleep(random.uniform(0.2, 0.5))
    time.sleep(2)
    inputElement = driver.find_element_by_id('session_password')
    for i in linkedin_password:
        inputElement.send_keys(i)
        time.sleep(random.uniform(0.2, 0.5))
    time.sleep(2)
    submit_button = driver.find_elements_by_xpath('/html/body/main/section[1]/div/div/form/button')[0]
    submit_button.click()
    time.sleep(3)

    count = 0
    res = {}
    for name in name_list:
        count += 1
        print(name)
        time.sleep(1)
        try:
            url = get_links_on_google('{} uiuc linkedin'.format(name))[0]
        except:
            res[name] = {'status': 'fail', 'education': [], 'experience': []}
            print('fail to get url for {}'.format(name))
            print()
            continue

        print(url)
        if 'https://www.linkedin.com/in/' not in url:
            res[name] = {'status': 'fail', 'education': [], 'experience': []}
            print('cannot find linkedin page for {}'.format(name))
            print()
            continue

        driver.get(url)
        time.sleep(random.randint(60, 120))
        html_string = str(driver.page_source)
        html = parse_html_string(html_string)

        education = get_education(html)
        print('Education:')
        print(education)
        experience = get_experience(html)
        print('Experience:')
        print(experience)

        res[name] = {'status': 'success', 'education': education, 'experience': experience}

        time.sleep(3)
        print()
        print()
        if count % 23 == 0:
            time.sleep(random.randint(300, 600))
    driver.quit()
    return res


# example
l = '''
Tarek Abdelzaher
Sarita V. Adve
Vikram Adve
Gul A. Agha
Abdussalam Alawini
'''

# before running this function, please go to LinkedIn and sign in with the following account
l = l.split('\n')[1:-1]
get_background_on_linkedin(l, 'uiuc', 'abudua732@gmail.com', '987acsdujhlcasd')

