import re
import stanza
from gensim.models import KeyedVectors

stanza.download('ru')
nlp_ru = stanza.Pipeline('ru')
model = KeyedVectors.load_word2vec_format('word_vectors.w2v')
purpose_words = ['в качестве', 'с целью', 'для того чтобы', 'для того, чтобы', 'чтобы', 'применяются', 'применяется',
                 'используется', 'используются', 'используют', 'нацеленный на', 'нацеленная на', 'нацеленные на', 'для']
information_words = ['компьютер', 'информация', 'алгоритм', 'интернет', 'технология', 'linux', 'процессор', 'программа',
                     'информатика', 'пароль']
ignore_headers = ['история', 'литература', 'см. также', 'ссылки', 'примечания']


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
        'task': phrase[0:mark_from] + '***' + phrase[mark_from:mark_end] + '***' + phrase[mark_end:],
        'word': found_str
    }
    # print(s)


def make_insert_term_task(definition, title):
    definition_res = definition.replace(title, f'***{title}***')
    title_cleaned = [x.lemma for x in nlp_ru(re.sub('[́̀]', '', title).lower()).sentences[0].words]
    definition_cleaned = [x.lemma for x in nlp_ru(re.sub('[́̀]', '', definition).lower()).sentences[0].words]

    term_quality = []
    definition_quaity = []

    for word in title_cleaned:
        if word in model.key_to_index:
            word_quality = [model.similarity(x, word) for x in information_words]
            term_quality += word_quality
        else:
            if len(word) > 1:
                term_quality.append(-10)

    for word in definition_cleaned:
        if word in model.key_to_index:
            word_quality = [model.similarity(x, word) for x in information_words]
            definition_quaity += word_quality
        else:
            continue

    return {
        'quality_term': sum(term_quality) / len(term_quality),
        'quality_def': sum(definition_quaity) / len(definition_quaity),
        'definition': definition_res
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
                    res.append(f"{group['h2']}***{child_tag.text}***")
                else:
                    res.append(f"{group['children'][idx - 1].text}***{child_tag.text}***")
    # print(children_tmp)
    # children_names = [c.name for c in children_tmp]
    return res