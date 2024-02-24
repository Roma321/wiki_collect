import concurrent.futures
import json

import urllib.parse

import requests
from bs4 import BeautifulSoup

w1 = 'https://ru.wikipedia.org/wiki/Категория:Информационные_технологии'
w2 = 'https://ru.wikipedia.org/wiki/Категория:Информатика'
w3 = 'https://ru.wikipedia.org/wiki/Категория:Программирование'
MAX_DEPTH = 1


def inner_all_articles(base_link, depth):
    if depth == MAX_DEPTH:
        return []
    r = requests.get(base_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    all_groups = soup.find_all('div', {'class': 'mw-category-group'})
    groups = [g for g in all_groups if len(g.find_all('span', {'class': 'CategoryTreeBullet'})) == 0 and len(
        g.find_all('span', {'class': 'CategoryTreeEmptyBullet'})) == 0]
    groups = [x.find_all('a') for x in groups]
    flat_list = [
        x
        for xs in groups
        for x in xs
    ]
    links = [f'https://ru.wikipedia.org{x["href"]}' for x in flat_list]

    categories = [g.find_all('div', {'class': 'CategoryTreeItem'}) for g in all_groups if
                  len(g.find_all('span', {'class': 'CategoryTreeBullet'})) != 0 or len(
                      g.find_all('span', {'class': 'CategoryTreeEmptyBullet'})) != 0]
    categories = [
        f"https://ru.wikipedia.org/{x.find('a', href=True)['href']}"
        for xs in categories
        for x in xs
    ]
    links_from_categories = [inner_all_articles(c, depth + 1) for c in categories]
    links_from_categories = [
        x
        for xs in links_from_categories
        for x in xs
    ]
    return links + links_from_categories


def all_articles():
    links_inf_techs = inner_all_articles(w1, 0)
    links_inf = inner_all_articles(w2, 0)
    links_prog = inner_all_articles(w3, 0)
    links = [urllib.parse.unquote(x) for x in list(set(links_inf_techs + links_inf + links_prog))]
    return links


count_processed = 0


def process_link(link):
    global count_processed
    count_processed += 1
    if count_processed % 100 == 0:
        print(count_processed)
    references = rate_link(link)
    return {
        'references': references,
        'link': urllib.parse.unquote(link)
    }


def rate_link(link):
    link_title = link.replace('https://ru.wikipedia.org/wiki/', '')
    refs_count = \
        requests.get(
            f'https://linkcount.toolforge.org/api/?project=ru.wikipedia.org&page={link_title}&namespaces=').json()[
            'wikilinks']['all']
    return refs_count


def rate_links(links, save_path=None):
    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []

        for link in links:
            futures.append(executor.submit(process_link, link))

        try:
            for future in concurrent.futures.as_completed(futures):
                try:
                    res.append(future.result())
                except:
                    print('(((')
        except:
            print('very (((')
    if save_path is not None:
        with open('links-8-with-rates.txt', 'w') as f:
            json.dump(res, f, ensure_ascii=False, indent=4)
    return res
