import re

from utils import rate_is_text_about_IT, purpose_words, nlp_ru, model, information_words, ignore_headers


def has_substring(string):
    for substring in purpose_words:
        index_start = string.lower().find(substring)
        if index_start >= 0:
            return True, index_start, index_start + len(substring), substring
    return False, -1, None, None


def make_purpose_task(phrase):
    contains, idx_start, idx_end, found_str = has_substring(phrase)
    if not contains:
        return

    s = nlp_ru(phrase).sentences[0].words

    collected = [x.id for x in s if x.start_char >= idx_start and x.end_char <= idx_end]
    if found_str == 'для':
        collected += [x.head for x in s if x.lemma == 'для']
    while True:
        append_elements = [x.id for x in s if
                           x.head in collected and x.id not in collected and x.start_char > idx_end and (
                                   x.feats is None or 'Case=Nom' not in x.feats)]
        if len(append_elements) == 0:
            break
        collected += append_elements
    if not collected:  # TODO обрабатывать не только найденное первое предложение
        return None
    mark_from = idx_end + 1
    mark_end = max(x.end_char for x in s if x.id in collected)
    return {
        'phrase': phrase,
        'task': phrase[0:mark_from] + '<<<' + phrase[mark_from:mark_end] + '>>>' + phrase[mark_end:],
        'word': found_str
    }
    # print(s)


def make_insert_term_task(definition, title):
    tire = '—'
    if tire in definition and tire not in title:
        to_replace_title = definition.split(tire)[0]
        term_task = definition.replace(to_replace_title, f'<<<{to_replace_title}>>>')
        definition_task = definition.replace(tire, f'{tire}<<<', 1) + '>>>'
    else:
        term_task = definition.replace(title, f'<<<{title}>>>')
        definition_task = definition.replace(title, f'{title}<<<') + '>>>'
    return {
        'term_task': term_task,
        'definition_task': definition_task
    }


def group_by_h2(children_tags):
    res_h2 = []
    last_meet_h2 = None
    for tag in children_tags:
        if tag.name == 'h2':  # обработка нового заголовка
            h2_text = tag.find('span', {'class': 'mw-headline'}).text
            last_meet_h2 = h2_text
        elif tag.name == 'div' and 'role' in tag and tag['role'] == 'navigation':
            continue
        else:  # обработка нормальных элементов
            # обработаем запись новой h2-группы. Если нет элементов, то и группа не появится
            if not last_meet_h2 or last_meet_h2.lower() in ignore_headers:  # если не тот заголовок
                continue
            elif len(res_h2) == 0 or res_h2[-1]['h2'] != last_meet_h2:
                res_h2.append({
                    'h2': last_meet_h2,
                    'children': []
                })
            # h2-группа на месте, можно дописывать
            res_h2[-1]['children'].append(tag)
    return [x for x in res_h2 if len(x['children'])]


def make_ul_li_task(soup):
    children_tmp = soup.find('div', {'class': 'mw-content-ltr mw-parser-output'}).findChildren(recursive=False)
    res = []
    children = group_by_h2(children_tmp)
    for group in children:
        for idx, child_tag in enumerate(group['children']):
            if child_tag.name in ['ol', 'ul']:
                if idx == 0:
                    res.append(f"{group['h2']}<<<{child_tag.text}>>>")
                else:
                    res.append(f"{group['children'][idx - 1].text}<<<{child_tag.text}>>>")
    # print(children_tmp)
    # children_names = [c.name for c in children_tmp]
    return res
