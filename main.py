import json

import requests
from bs4 import BeautifulSoup

from collect_links import all_articles
from make_task import make_insert_term_task, make_purpose_task_from_phrase, make_ul_li_task, make_purpose_task_from_page
from string_utils import delete_inside_parentheses_and_brackets
from utils import parallel_map, first_p_by_link


def process_link(idx, link):
    try:
        page = requests.get(link).text
        page_soup = BeautifulSoup(page, 'html.parser')
        article = page_soup.find('div', {'class': 'mw-content-ltr mw-parser-output'})
        infobox_tables = article.find_all('table', {'class': 'infobox'})
        for table in infobox_tables:
            table.decompose()
        first_p = article.find('p', class_=lambda x: x != "mw-empty-elt" and x != 'wikidata-claim')
        title = first_p.find('b')
        if title is None:
            return None
        title = delete_inside_parentheses_and_brackets(title.text)
        definition = delete_inside_parentheses_and_brackets(first_p.text)
        term_task = make_insert_term_task(definition, title)
        purpose_task = make_purpose_task_from_page(page_soup)
        ul_task = make_ul_li_task(page_soup)
        return {'term': term_task, 'purpose': purpose_task, 'ul': ul_task, 'link': link}
    except Exception as e:
        print('error', idx, e)
        return None


# all_links = all_articles()


def make_corpus(links, directory=None, num_threads=5, step_info=100):
    raw_results = parallel_map(num_threads, links, process_link, step_info)
    results = [x for x in raw_results if x is not None]
    errors_count = len([x for x in raw_results if x is None])

    print(errors_count)
    res = [task['term'] for task in results]
    res_p = [task['purpose'] for task in results]
    res_ul = [{'task': task['ul'], 'link': task['link']} for task in results]
    with open(f'{f"{directory}/" if directory is not None else ""}terms.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
    with open(f'{f"{directory}/" if directory is not None else ""}res_p.json', 'w', encoding='utf-8') as f:
        json.dump(res_p, f, ensure_ascii=False, indent=4)
    with open(f'{f"{directory}/" if directory is not None else ""}uls.json', 'w', encoding='utf-8') as f:
        json.dump(res_ul, f, ensure_ascii=False, indent=4)

# make_corpus(all_links)
