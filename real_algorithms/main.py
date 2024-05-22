import os

import pymorphy2

morph = pymorphy2.MorphAnalyzer()
dir = '/home/roman/projects/my/wiki_collect/markup-part-1'


#
def listfiles():
    files = os.listdir(dir)
    return files


def get_f1(matrix):
    tn, fp, fn, tp = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
    return f1


def lemmatize(s):
    return set([morph.normal_forms(x.strip())[0] for x in s.split() if x.strip()])

# print(get_f1([[0, 10], [0, 10]]))
# train_bow()
# from utils import model
#
# s1 = 'столица'
# s2 = 'германия'
# # print(model.similarity(s1,s2))
# v1 = model.get_vector(s1)
# v2 = model.get_vector(s2)
# print(v1[:10], v2[:10])
# s = v1 + v2
# s *= 10
# print(s[:10])
# print(model.similar_by_vector(s))
