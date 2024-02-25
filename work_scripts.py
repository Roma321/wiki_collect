import json

import requests
from bs4 import BeautifulSoup

from string_utils import delete_inside_parentheses_and_brackets
from utils import rate_is_text_about_IT, parallel_map


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
        page = requests.get(link_dict['link']).text
        page_soup = BeautifulSoup(page, 'html.parser')
        first_p = page_soup.find('div', {'class': 'mw-content-ltr mw-parser-output'}).find('p')
        definition = delete_inside_parentheses_and_brackets(first_p.text)
        link_dict['about_IT'] = rate_is_text_about_IT(definition)
        return link_dict
    except:
        link_dict['about_IT'] = None
        print('ERROR ON', link_dict)
        return link_dict


def step_2():
    with open('links-8-with-rates.txt', 'r') as file:
        j = json.load(file)
    r = parallel_map(40, j, rate_is_link_about_IT, 40)
    # print(r)
    with open('links-8-with-rates-extended.json', 'w') as file:
        json.dump(r, file, ensure_ascii=False, indent=4)


step_2()
