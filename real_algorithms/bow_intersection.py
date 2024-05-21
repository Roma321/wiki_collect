import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def bow_intersection(s1, s2):
    bag1 = set([morph.normal_forms(x.strip())[0] for x in s1.split() if x.strip()])
    bag2 = set([morph.normal_forms(x.strip())[0] for x in s2.split() if x.strip()])
    return len(bag1.intersection(bag2)) / min(len(bag1), len(bag2))
