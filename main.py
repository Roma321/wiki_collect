import concurrent.futures
import json

import requests
from bs4 import BeautifulSoup

from collect_links import all_articles
from make_task import make_insert_term_task, make_purpose_task, make_ul_li_task
from string_utils import delete_inside_parentheses_and_brackets


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


# res = []
# res_p = []
# res_ul = []
# all_links = all_articles()
# for idx, link in enumerate(all_links):
#     try:
#         print(idx)
#         page = requests.get(link).text
#         page_soup = BeautifulSoup(page, 'html.parser')
#         title_on_page = page_soup.find('span', {'class': 'mw-page-title-main'}).text
#         first_p = page_soup.find('div', {'class': 'mw-content-ltr mw-parser-output'}).find('p')
#         title = first_p.find('b')
#         if title is None:
#             continue
#         title = delete_inside_parentheses_and_brackets(title.text)
#         definition = delete_inside_parentheses_and_brackets(first_p.text)
#         term_task = make_insert_term_task(definition, title)
#         purpose_task = make_purpose_task(definition)
#         ul_task = make_ul_li_task(page_soup)
#         res.append(term_task)
#         res_p.append(purpose_task)
#         res_ul.append({'task': ul_task, 'link': link})
#         # print('success', term_task, purpose_task)
#     except Exception as e:
#         print('error', e)
#
# with open('terms.json', 'w', encoding='utf-8') as f:
#     json.dump(res, f, ensure_ascii=False, indent=4)
#
# with open('res_p.json', 'w', encoding='utf-8') as f:
#     json.dump(res_p, f, ensure_ascii=False, indent=4)
#
# with open('uls.json', 'w', encoding='utf-8') as f:
#     json.dump(res_ul, f, ensure_ascii=False, indent=4)
all_links = all_articles()
results = []

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Submit the tasks to the executor
    futures = [executor.submit(process_link, idx, link) for idx, link in enumerate(all_links)]

    # Collect the results as they become available
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result is not None:
            results.append(result)

res = [task['term'] for task in results]
res_p = [task['purpose'] for task in results]
res_ul = [{'task': task['ul'], 'link': task['link']} for task in results]

with open('terms.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)

with open('res_p.json', 'w', encoding='utf-8') as f:
    json.dump(res_p, f, ensure_ascii=False, indent=4)

with open('uls.json', 'w', encoding='utf-8') as f:
    json.dump(res_ul, f, ensure_ascii=False, indent=4)
