import re


def delete_inside_parentheses_and_brackets(text):
    result = re.sub(r"\([^()]*\)", "", text)
    result = re.sub(r'\[[^\]]*\]', '', result)
    return result