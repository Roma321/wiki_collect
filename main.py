import json

import requests
from bs4 import BeautifulSoup

from collect_links import all_articles
from make_task import make_insert_term_task, make_purpose_task, make_ul_li_task
from string_utils import delete_inside_parentheses_and_brackets
from utils import parallel_map


def process_link(idx, link):
    print(idx)
    try:
        page = requests.get(link).text
        page_soup = BeautifulSoup(page, 'html.parser')
        first_p = page_soup.find('div', {'class': 'mw-content-ltr mw-parser-output'}).find('p')
        title = first_p.find('b')
        if title is None:
            return None
        title = delete_inside_parentheses_and_brackets(title.text)
        definition = delete_inside_parentheses_and_brackets(first_p.text)
        term_task = make_insert_term_task(definition, title)
        purpose_task = make_purpose_task(definition)
        ul_task = make_ul_li_task(page_soup)
        return {'term': term_task, 'purpose': purpose_task, 'ul': ul_task, 'link': link}
    except Exception as e:
        print('error', idx, e)
        return None


all_links = all_articles()
results = parallel_map(5, all_links, process_link, 100)

res = [task['term'] for task in results]
res_p = [task['purpose'] for task in results]
res_ul = [{'task': task['ul'], 'link': task['link']} for task in results]

with open('terms.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)

with open('res_p.json', 'w', encoding='utf-8') as f:
    json.dump(res_p, f, ensure_ascii=False, indent=4)

with open('uls.json', 'w', encoding='utf-8') as f:
    json.dump(res_ul, f, ensure_ascii=False, indent=4)
