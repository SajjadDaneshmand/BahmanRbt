from collections import Counter


def word_cleaning(val):
    val = str(val)
    no_space = val.replace(' ', '')
    characters = list(set(no_space))
    word = ''.join(characters)
    return word


def chars(string):
    lst = []
    for name in string:
        word = word_cleaning(name)
        for char in word:
            lst.append(char)
    return lst


def max_character(lst):
    dictionary = Counter(lst)
    return max(dictionary, key=dictionary.get)


