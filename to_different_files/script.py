import json
import uuid
import re

from string_utils import delete_inside_parentheses_and_brackets


def split_definitions():
    with open('/home/roman/projects/my/wiki_collect/corpus-3/terms.json', 'r') as f:
        j = json.load(f)

        for item in j:
            task = item['definition_task'].replace('\n', '')
            d = {
                'task': task,
                'correct': [f'{x}'.strip() for x in re.findall(r'<<<(.+?)>>>', task)],
                'wrong': [],
                'meta': {
                    'type': 'definition'
                }
            }

            with open(f'../splitted/{uuid.uuid4()}.json', 'w') as file:
                json.dump(d, file, ensure_ascii=False, indent=4)


# split_definitions()


def split_uls():
    with open('/home/roman/projects/my/wiki_collect/corpus-3/uls.json', 'r') as f:
        j = json.load(f)

        for item in j:
            for task in item['task']:
                task = delete_inside_parentheses_and_brackets(task)
                correct_list = re.findall(r'<<<(.+?)>>>', task, re.DOTALL)

                correct_list = [x.strip() for x in correct_list if x.strip()]

                correct_answers = [re.split(r'\n+', x) for x in correct_list]
                correct_answers = [x for x in correct_answers if x]
                d = {
                    'task': task,
                    'correct': correct_answers,
                    'wrong': [],
                    'meta': {
                        'type': 'ul',
                        'link': item['link']
                    }
                }
            with open(f'../splitted/{uuid.uuid4()}.json', 'w') as file:
                json.dump(d, file, ensure_ascii=False, indent=4)


# split_uls()

def split_res_p():
    with open('/home/roman/projects/my/wiki_collect/corpus-3/res_p.json', 'r') as f:
        j = json.load(f)

        for item in j:
            for h2_list in item:
                for h2 in h2_list:
                    for task in h2['tasks']:
                        task = delete_inside_parentheses_and_brackets(task)
                        correct_list = re.findall(r'<<<(.+?)>>>', task, re.DOTALL)

                        correct_list = [x.strip() for x in correct_list if x.strip()]

                        correct_answers = [re.split(r'\n+', x) for x in correct_list]
                        correct_answers = [x for x in correct_answers if x]
                        d = {
                            'task': task,
                            'correct': correct_answers,
                            'wrong': [],
                            'meta': {
                                'type': 'ul',
                                'link': item['link']
                            }
                        }
            with open(f'../splitted/{uuid.uuid4()}.json', 'w') as file:
                json.dump(d, file, ensure_ascii=False, indent=4)
