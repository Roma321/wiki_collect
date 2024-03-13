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
# def step_5():
#     with open('markup/progress-info', 'r') as file_progress:
#         progress = int(file_progress.read())
#     files = [x for x in listdir('markup') if x.endswith('.json') and int(x.split('_')[0]) >= progress]
#     files = sorted(files, key=lambda x: int(x.split('_')[0]))
#     res_data = []
#     for file in files:
#         with open(f'markup/{file}', 'r') as file_data:
#             j = json.load(file_data)
#         for idx, link in enumerate(j):
#             print(f'{idx + 1}/{len(j)}')
#             ans = ''
#             print(link['link'])
#             while ans not in ['1', '2', '3', 'exit']:
#                 print('1 - берём\n2 - возможно\n3 - нет\n4 - показать первый абзац\n5 - показать все данные')
#                 ans = input('> ')
#                 if ans in ['1', '2', '3']:
#                     link['take'] = ans
#                 if ans == '4':
#                     print(first_p_by_link(link['link']))
#                 if ans == '5':
#                     print(link)
#             res_data.append(link)
#             print('OK')
#
#         with open('markup/progress-info', 'w') as file_progress:
#             file_progress.write(file.split('_')[1].replace('.json', ''))
#         with open(f'markup/{file}', 'w') as file_save_data:
#             json.dump(res_data, file_save_data, ensure_ascii=False, indent=4)
#         res_data = []
#         print('Файл размечен и сохранён. 1 чтобы завершить')
#         ans = input('> ')
#         if ans == '1':
#             exit(0)


# def step_6():
#     files = [x for x in listdir('markup') if x.endswith('.json')]
#     files = sorted(files, key=lambda x: int(x.split('_')[0]))[:3]
#     print(files)
#     articles = []
#     for file in files:
#         with open(f'markup/{file}', 'r') as file_data:
#             j = json.load(file_data)[-40:]
#             articles += [x for x in j if x['take'] == '1']
#     with open('corpus-1/links.json', 'w') as file:
#         json.dump(articles, file, ensure_ascii=False, indent=4)
#     print(len(articles))


# step_6()


def step_7():
    with open('corpus-1/links.json', 'r') as file:
        j = json.load(file)
    make_corpus([x['link'] for x in j], directory='corpus-1', step_info=5)


def step_8():
    with open('corpus-1/links.json', 'r') as file:
        j = json.load(file)
    make_corpus([x['link'] for x in j], directory='corpus-2', step_info=5)


# step_7()

# text = '''Форк (fork с англ. — «развилка, вилка») или ответвление — использование кода программного проекта в качестве старта для другого, при этом основной проект может как продолжать существование, так и прекратить его.
#
# Ответвлённый проект или форк может поддерживать и обмениваться частью содержимого с основным проектом, а может и приобрести абсолютно другие свойства, перестав иметь с базовым проектом что-то общее. Пример: разделение проекта X Window System на XFree86 и X.Org, разделение проекта OpenOffice.org на LibreOffice и Apache OpenOffice. Разделения были и среди несвободного программного обеспечения. Пример: Windows NT, которая по мере развития разделилась на две ветви: Windows 2000 и Windows Server.'''
# a = nlp_ru_tokenize(text)
#
# print(a.sentences)
# print(len(a.sentences))
# make_purpose_task_from_page()

# step_7()
step_8()