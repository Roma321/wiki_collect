import json
from os import listdir

from utils import first_p_by_link


def markup_helper():
    with open('markup/progress-info', 'r') as file_progress:
        progress = int(file_progress.read())
    files = [x for x in listdir('markup') if x.endswith('.json') and int(x.split('_')[0]) >= progress]
    files = sorted(files, key=lambda x: int(x.split('_')[0]))
    res_data = []
    for file in files:
        with open(f'markup/{file}', 'r') as file_data:
            j = json.load(file_data)
        for idx, link in enumerate(j):
            print(f'{idx + 1}/{len(j)}')
            ans = ''
            print(link['link'])
            while ans not in ['1', '2', '3', 'exit']:
                print('1 - берём\n2 - возможно\n3 - нет\n4 - показать первый абзац\n5 - показать все данные')
                ans = input('> ')
                if ans in ['1', '2', '3']:
                    link['take'] = ans
                if ans == '4':
                    print(first_p_by_link(link['link']))
                if ans == '5':
                    print(link)
            res_data.append(link)
            print('OK')

        with open('markup/progress-info', 'w') as file_progress:
            file_progress.write(file.split('_')[1].replace('.json', ''))
        with open(f'markup/{file}', 'w') as file_save_data:
            json.dump(res_data, file_save_data, ensure_ascii=False, indent=4)
        res_data = []
        print('Файл размечен и сохранён. 1 чтобы завершить')
        ans = input('> ')
        if ans == '1':
            exit(0)