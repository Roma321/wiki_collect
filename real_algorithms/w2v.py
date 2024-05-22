import json
import os

from real_algorithms.main import listfiles, dir, lemmatize
from utils import model

import numpy as np


# 74.4% при 0.623

def cosine_similarity(a, b):
    # print(len(a))
    # print(len(b))
    # print(a)
    # print(b)
    numerator = np.dot(a, b)
    denominator = np.sqrt(np.dot(a, a)) * np.sqrt(np.dot(b, b))
    if denominator == 0:
        print(a, b)
        # return 1
    return numerator / denominator


def w2v_similarity_total(s1, s2):
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', s1, '&&&&&&&&&&&&&&&&&&&&&&&&', s2)
    s1_vector = np.sum([model.get_vector(x) for x in lemmatize(s1) if x in model.key_to_index], axis=0)
    s2_vector = np.sum([model.get_vector(x) for x in lemmatize(s2) if x in model.key_to_index], axis=0)
    # print(s1_vector)
    if is_nullish(s1_vector):
        return 1 if s1 in s2 else 0
    if is_nullish(s2_vector):
        return 1 if s2 in s1 else 0
    return cosine_similarity(s1_vector, s2_vector)


def is_nullish(vector):
    return (isinstance(vector, (list, tuple, np.ndarray)) and (
            all(v == 0.0 for v in vector) or len(vector) == 0)) or (
            not isinstance(vector, (list, tuple, np.ndarray)) and vector == 0.0)


def train_w2v():
    best = 0
    best_coef = 0
    for try_coef in [x / 1000 for x in range(1, 700, 1)]:
        martix = [[0, 0], [0, 0]]
        for file in listfiles():
            file_path = os.path.join(dir, file)
            with open(file_path, 'r') as f:
                j = json.load(f)
                correct_answer = j['correct'][0]
                other_correct_answer = j['correct'][1:]
                wrong_answer = j['wrong']
                if j['meta']['type'] == 'definition':
                    for other in other_correct_answer:
                        coef = w2v_similarity_total(correct_answer, other)
                        if coef > try_coef:
                            martix[0][0] += 1
                        else:
                            martix[0][1] += 1
                    for wrong in wrong_answer:
                        coef = w2v_similarity_total(correct_answer, wrong)
                        if coef < try_coef:
                            martix[1][1] += 1
                        else:
                            martix[1][0] += 1
                if j['meta']['type'] == 'ul':
                    for other_group in other_correct_answer:
                        for other in other_group:
                            # print([w2v_similarity_total(other, correct_answer_1) for correct_answer_1 in
                            #        correct_answer])
                            is_correct_alg_opinion = max(
                                [w2v_similarity_total(other, correct_answer_1) for correct_answer_1 in
                                 correct_answer]) > try_coef
                            if is_correct_alg_opinion:
                                martix[0][0] += 1
                            else:
                                martix[0][1] += 1

                    for wrong in wrong_answer:
                        is_correct_alg_opinion = max(
                            [w2v_similarity_total(wrong, correct_answer_1) for correct_answer_1 in
                             correct_answer]) > try_coef
                        if not is_correct_alg_opinion:
                            martix[1][1] += 1
                        else:
                            martix[1][0] += 1
        # f1 = martix[0][0] / sum(martix[0]) + martix[1][1] / sum(martix[1])
        # print(f"----{f1}-----")
        # if f1 > best:
        #     best = f1

        my_measure = (martix[0][0] / sum(martix[0]) + martix[1][1] / sum(martix[1])) / 2
        print(f"----{my_measure}-----")
        if my_measure > best:
            best = my_measure
            best_coef = try_coef
    print(best, best_coef)


# train_w2v()
# print(w2v_similarity_total("Мама мыла раму", "Имперские штуромвики захватили планету"))
