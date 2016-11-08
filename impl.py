# -*- coding: utf-8 -*-
import re

print "Digite a palavra de entrada"
word = raw_input()
print "Digite o caminho do arquivo com as regras de produção da gramática"
filename = raw_input()
f = open(filename, 'r')
rules = f.read()

WORD_LENGTH = len(word)

matrix = [[0 for con in range(WORD_LENGTH)] for row in range(WORD_LENGTH)]
productions = {}
subwords = {}

for rule in rules.split("\n"):
    if rule.strip() != '':
        left, right = re.search(r'([A-Z]+) ?-> ?([A-Za-z ?]+)', rule).groups()
        right = right.replace(' ', '')
        if right in productions:
            productions[right].append(left)
        else:
            productions[right] = [left]

def word_combinations(word):
    word_length = len(word)
    words = []
    found_productions = []
    for i in range(word_length):
        words.append(word[0:i+1])
        if word[i+1:word_length] != '':
            words.append(word[i+1:word_length])

    return words

def cartesian_product(productions):
    result = []
    if len(productions) == 1:
        return productions

    for i in range(0,len(productions)-1,2):
        for production in productions[i]:
            for production2 in productions[i+1]:
                result.append(production+production2)

    return result

def derive_word(word, matrix_i, matrix_j):
    if len(word) == 1:
        subword_location = subwords[word]
        i = subword_location['i']
        j = subword_location['j']
        if word in productions:
            matrix[i][j] = productions[word]
    else:
        all_subwords = word_combinations(word)
        production_combinations = []
        for subword in all_subwords:
            subword_location = subwords[subword]
            i = subword_location['i']
            j = subword_location['j']
            if matrix[i][j] != 0:
                production_combinations.append(matrix[i][j])

        result = []
        for production in cartesian_product(production_combinations):
            if production in productions:
                result.append(productions[production])

        matrix[matrix_i][matrix_j] = list(set([item for sublist in result for item in sublist]))

for i in range(WORD_LENGTH):
    subword_length = i+1
    for j in range(WORD_LENGTH-subword_length+1):
        subword = word[j:j+subword_length]
        if subword not in subwords:
            subwords[subword] = {'i': i, 'j': j}

        derive_word(subword, i, j)

if len(matrix[WORD_LENGTH-1][0]) == 0:
    print "NÃO"
else:
    print "SIM"
