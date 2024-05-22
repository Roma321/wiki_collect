import json
import os

from real_algorithms.main import listfiles

# 0.725 и 52.3% для Левенштейна

def levenshtein_distance(s1, s2):
    """
    Calculates the Levenshtein distance between two strings.
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]


def train_levenstein():
    best = 0
    best_coef = 0
    for try_coef in [x / 1000 for x in range(500, 951, 5)]:
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
                        lev = levenshtein_distance(other, correct_answer)
                        coef = lev / len(correct_answer)
                        if coef < try_coef:
                            martix[0][0] += 1
                        else:
                            martix[0][1] += 1
                    for wrong in wrong_answer:
                        lev = levenshtein_distance(wrong, correct_answer)
                        coef = lev / len(correct_answer)
                        if coef > try_coef:
                            martix[1][1] += 1
                        else:
                            martix[1][0] += 1
                if j['meta']['type'] == 'ul':
                    for other_group in other_correct_answer:
                        for other in other_group:
                            is_correct_alg_opinion = min(
                                [levenshtein_distance(other, correct_answer_1) for correct_answer_1 in
                                 correct_answer]) < try_coef
                            if is_correct_alg_opinion:
                                martix[0][0] += 1
                            else:
                                martix[0][1] += 1

                    for wrong in wrong_answer:
                        is_correct_alg_opinion = min(
                            [levenshtein_distance(wrong, correct_answer_1) for correct_answer_1 in
                             correct_answer]) < try_coef
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
