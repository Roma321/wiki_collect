import json
from os import listdir
from os.path import isfile, join

import requests
from bs4 import BeautifulSoup

from main import make_corpus
from make_task import make_purpose_task_from_page
from string_utils import delete_inside_parentheses_and_brackets
from utils import first_p_by_link, nlp_ru, nlp_ru_tokenize


#
# import requests
# from bs4 import BeautifulSoup
#
# from string_utils import delete_inside_parentheses_and_brackets
# from utils import rate_is_text_about_IT, parallel_map
# import re
#
#
# def step_1():
#     # Load initial JSON data from the file
#     with open('links-8-with-rates.txt', 'r') as file:
#         j = json.load(file)
#
#     # Sort the data based on 'references' in descending order
#     sorted_data = sorted(j, key=lambda x: x['references'], reverse=True)
#
#     # Write the sorted data back to the file
#     with open('links-8-with-rates.txt', 'w') as file:
#         json.dump(sorted_data, file, ensure_ascii=False, indent=4)
#
#
# def rate_is_link_about_IT(idx, link_dict):
#     try:
#         definition = first_p_by_link(link_dict['link'])
#         link_dict['about_IT'] = rate_is_text_about_IT(definition)
#         return link_dict
#     except:
#         link_dict['about_IT'] = None
#         print('ERROR ON', link_dict)
#         return link_dict
#
#


#
#
# def step_2():
#     with open('links-8-with-rates.txt', 'r') as file:
#         j = json.load(file)
#     r = parallel_map(40, j, rate_is_link_about_IT, 40)
#     # print(r)
#     with open('links-8-with-rates-extended.json', 'w') as file:
#         json.dump(r, file, ensure_ascii=False, indent=4)
#
#
# def has_russian_letters(string):
#     russian_letters_pattern = re.compile(r'[а-яА-Я]')
#     return bool(russian_letters_pattern.search(string))
#
#
# def is_not_computer_game(link):
#     text = first_p_by_link(link).lower()
#     return 'видеоигр' not in text and not re.search(r'компьютерн.{1,20}игр', text)
#
#
# def set_work_group(idx, link_dict):
#     try:
#         if link_dict['about_IT'] is None or not is_not_computer_game(link_dict['link']):
#             link_dict['group'] = 0
#             return link_dict
#         group = 0  # побитово: 4 на ссылки, 2 на информатичность, 1 на русские буквы
#         if link_dict['references'] > 60:
#             group += 4
#         if link_dict['about_IT'] > 0.1:
#             group += 2
#         if has_russian_letters(link_dict['link']):
#             group += 1
#         link_dict['group'] = group
#         return link_dict
#
#     except:
#         link_dict['group'] = None
#         print('ERROR ON', link_dict)
#     return link_dict
#
#
# def step_3():
#     with open('links-8-with-rates-extended.json', 'r') as file:
#         j = json.load(file)
#
#     with_work_group = parallel_map(40, j, set_work_group, 40)
#     with open('links-8-with-work-group.json', 'w') as file:
#         json.dump(with_work_group, file, ensure_ascii=False, indent=4)


# def step_4():
#     with open('links-8-with-work-group.json', 'r') as file:
#         j = json.load(file)
#
#     j = [x for x in j if x['group'] == 7]
#     for x in j:
#         x['take'] = ""
#     for i in range(len(j) // 40 + 1):
#         start = i * 40
#         end = min((i + 1) * 40, len(j))
#         block = j[start:end]
#         with open(f'markup/{start}_{end - 1}.json', 'w') as file:
#             json.dump(block, file, ensure_ascii=False, indent=4)


# step_4()


def get_good_links(amount):
    files = [x for x in listdir('markup') if x.endswith('.json')]
    files = sorted(files, key=lambda x: int(x.split('_')[0]))[:amount // 40 + 1]
    print(files)
    articles = []
    for file in files:
        with open(f'markup/{file}', 'r') as file_data:
            j = json.load(file_data)[-40:]
            articles += [x for x in j if x['take'] == '1']

    return articles[:amount]


# step_6()


def step_7():
    with open('corpus-1/links.json', 'r') as file:
        j = json.load(file)
    make_corpus([x['link'] for x in j], directory='corpus-1', step_info=5)


def step_8():
    with open('corpus-1/links.json', 'r') as file:
        j = json.load(file)
    make_corpus([x['link'] for x in j], directory='corpus-2', step_info=5)


def step_9():
    all_links = get_good_links(2000)
    print(all_links)
    make_corpus([x['link'] for x in all_links], directory='corpus-3', step_info=5)


# step_7()

step_9()
