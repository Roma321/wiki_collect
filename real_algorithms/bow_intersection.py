import json
import os

from real_algorithms.main import listfiles, dir, lemmatize

# 69.9 % при границе в 0.255
def bow_intersection(s1, s2):
    bag1 = lemmatize(s1)
    bag2 = lemmatize(s2)
    if len(bag1) == 0 or len(bag2) == 0:
        return 0
    return len(bag1.intersection(bag2)) / min(len(bag1), len(bag2))


def train_bow():
    best = 0
    best_coef = 0
    for try_coef in [x / 1000 for x in range(150, 951, 5)]:
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
                        coef = bow_intersection(correct_answer, other)
                        if coef > try_coef:
                            martix[0][0] += 1
                        else:
                            martix[0][1] += 1
                    for wrong in wrong_answer:
                        coef = bow_intersection(correct_answer, wrong)
                        if coef < try_coef:
                            martix[1][1] += 1
                        else:
                            martix[1][0] += 1
                if j['meta']['type'] == 'ul':
                    for other_group in other_correct_answer:
                        for other in other_group:
                            is_correct_alg_opinion = max(
                                [bow_intersection(other, correct_answer_1) for correct_answer_1 in
                                 correct_answer]) > try_coef
                            if is_correct_alg_opinion:
                                martix[0][0] += 1
                            else:
                                martix[0][1] += 1

                    for wrong in wrong_answer:
                        is_correct_alg_opinion = max(
                            [bow_intersection(wrong, correct_answer_1) for correct_answer_1 in
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


# train_bow()
