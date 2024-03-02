import json

import requests
from bs4 import BeautifulSoup

from string_utils import delete_inside_parentheses_and_brackets
from utils import rate_is_text_about_IT, parallel_map
import re


def step_1():
    # Load initial JSON data from the file
    with open('links-8-with-rates.txt', 'r') as file:
        j = json.load(file)

    # Sort the data based on 'references' in descending order
    sorted_data = sorted(j, key=lambda x: x['references'], reverse=True)

    # Write the sorted data back to the file
    with open('links-8-with-rates.txt', 'w') as file:
        json.dump(sorted_data, file, ensure_ascii=False, indent=4)


def rate_is_link_about_IT(idx, link_dict):
    try:
        definition = first_p_by_link(link_dict['link'])
        link_dict['about_IT'] = rate_is_text_about_IT(definition)
        return link_dict
    except:
        link_dict['about_IT'] = None
        print('ERROR ON', link_dict)
        return link_dict


def first_p_by_link(link):
    page = requests.get(link).text
    page_soup = BeautifulSoup(page, 'html.parser')
    article = page_soup.find('div', {'class': 'mw-content-ltr mw-parser-output'})
    infobox_tables = article.find_all('table', {'class': 'infobox'})
    for table in infobox_tables:
        table.decompose()
    first_p = article.find('p', class_=lambda x: x != "mw-empty-elt" and x != 'wikidata-claim')
    definition = delete_inside_parentheses_and_brackets(first_p.text)
    return definition


def step_2():
    with open('links-8-with-rates.txt', 'r') as file:
        j = json.load(file)
    r = parallel_map(40, j, rate_is_link_about_IT, 40)
    # print(r)
    with open('links-8-with-rates-extended.json', 'w') as file:
        json.dump(r, file, ensure_ascii=False, indent=4)


def has_russian_letters(string):
    russian_letters_pattern = re.compile(r'[а-яА-Я]')
    return bool(russian_letters_pattern.search(string))


def is_not_computer_game(link):
    text = first_p_by_link(link).lower()
    print('text', text, 'видеоигр' not in text and not re.search(r'компьютерн.{1,20}игр', text))
    return 'видеоигр' not in text and not re.search(r'компьютерн.{1,20}игр', text)


def step_3():
    with open('links-8-with-rates-extended.json', 'r') as file:
        j = json.load(file)
    j_not_none = [x for x in j if x['about_IT'] is not None]
    # j_none = [x for x in j if x['about_IT'] is None]
    sorted_data = sorted(j_not_none, key=lambda x: x['about_IT'], reverse=True)
    # sorted_data = [x for x in sorted_data[:20] if is_not_computer_game(x['link'])]
    with open('it-first.json', 'w') as file:
        json.dump(sorted_data, file, ensure_ascii=False, indent=4)


#
#
# # step_3()
#
# l = 'https://ru.wikipedia.org/wiki/Need_for_Speed:_Undercover'
# a = first_p_by_link(l).lower()
# print(a)

# step_2()
step_3()