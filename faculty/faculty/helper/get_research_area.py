from get_html import get_html, parse_scraped_html


def get_research_area_from_google_scholar(name):
    query = name.replace(' ', '+').replace('/', "%2F").replace('–', '')
    url = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors={}&btnG='.format(query)
    headers = {'User-Agent': 'Mozilla/5.0',
               'Referer': 'https://scholar.google.com/citations?hl=en&view_op=search_authors'}
    html = get_html(url, 'urllib', headers)
    raw_html = parse_scraped_html(html)
    target = '<a class="gs_ai_one_int"'
    target_len = len(target)
    res = []
    for i in range(len(raw_html)):
        if len(raw_html[i]) > target_len and raw_html[i][:target_len] == target:
            res.append(raw_html[i + 1])
    for i in res:
        print(i)

get_research_area_from_google_scholar('kevin chang') 