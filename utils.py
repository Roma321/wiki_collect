import concurrent.futures
import re

import requests
import stanza
from bs4 import BeautifulSoup
from gensim.models import KeyedVectors

from string_utils import delete_inside_parentheses_and_brackets

stanza.download('ru')
nlp_ru = stanza.Pipeline('ru')
nlp_ru_lemma = stanza.Pipeline('ru', processors='tokenize,lemma')
model = KeyedVectors.load_word2vec_format('word_vectors.w2v')
purpose_words = ['в качестве', 'с целью', 'для того чтобы', 'для того, чтобы', 'чтобы', 'применяются', 'применяется',
                 'используется', 'используются', 'используют', 'нацеленный на', 'нацеленная на', 'нацеленные на', 'для']
information_words = ['компьютер', 'информация', 'алгоритм', 'интернет', 'технология', 'linux', 'процессор', 'программа',
                     'информатика', 'пароль']
ignore_headers = ['история', 'литература', 'см. также', 'ссылки', 'примечания']


def parallel_map(num_threads, data, map_function, step_info):
    results = []
    count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit the tasks to the executor
        futures = [executor.submit(map_function, idx, link) for idx, link in enumerate(data)]

        # Collect the results as they become available
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            count += 1
            if count % step_info == 0:
                print(count)
            results.append(result)
    return results


def rate_is_text_about_IT(text):
    text_lemma = [x.lemma for x in nlp_ru_lemma(re.sub('[́̀]', '', text).lower()).sentences[0].words]
    definition_quality = []
    for word in text_lemma:
        if word in model.key_to_index:
            word_quality = [model.similarity(x, word) for x in information_words]
            definition_quality += word_quality
        else:
            continue
    return sum(definition_quality) / len(definition_quality)


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
