from difflib import SequenceMatcher
import string
from tabulate import tabulate
import pandas as pd

input = "input.txt"
with open(input) as f:
    input_lines = f.read().split('\n')

nonterminals = input_lines[1].split(" ")

terminals = input_lines[0].split(" ")


def insert_rules(nonterminals):  # create dict to insert values
    dictionar = {}
    for letter in nonterminals:
        if letter not in dictionar:
            dictionar[letter] = []
    for rule in input_lines[2:]:
        rule = rule.split(" ")
        dictionar[rule[0]].append(rule[1])
    return dictionar


def print_original(dict):  # prints original rules
    print("Original rules:")
    print("P = {")
    for k in dict:
        print(k, " -> ", " | ".join(dict[k]))
    print("}")


def common_part(list):  # takes common part to rename it(means to add new nonterminal)
    string2 = list[0]
    for i in range(1, len(list)):
        string1 = string2
        string2 = list[i]
        match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
    final_common = (string1[match.a: match.a + match.size])
    return final_common


def eliminate_lf(dictionar):  # check if a nonterminal derives into 2 or more variables,and introduce new nonterminals
    dictionar_new = {}
    alphabet = string.ascii_uppercase
    alphabet = list(alphabet)
    alphabet.reverse()
    count = 0
    for k in dictionar:
        for v in dictionar[k]:
            dictionar_new[k] = []
            if len(dictionar[k]) < 2:
                dictionar_new[k].append(v)
            else:
                dictionar_new[alphabet[count]] = []
                dictionar_new[k].append(common_part(dictionar[k]) + alphabet[count])
                dictionar_new[alphabet[count]].append(v.removeprefix(common_part(dictionar[k])))
                dictionar_new[alphabet[count]] += "ε"
        count += 1

    return dictionar_new


def print_lf(dict):
    print()
    print("After removing left factoring:")
    print("P = {")
    for k in dict:
        print(k, " -> ", " | ".join(dict[k]))
    print('}')
    print()


def first_funct(dictionary):
    dict = {}
    dict2 = {}
    for k in dictionary:
        dict[k] = []
        for v in dictionary[k]:
            if v[0].islower():
                dict[k] += v[0]
                dict['B'] = ['a']
            else:
                if v[0] in dictionary.keys():
                    dict[v[0]]=[]

                    dict[k] += dict[v[0]]
                for k1 in dictionary:
                    if dictionary[k1][0][0].isupper():
                        dict[k1] = dictionary[dictionary[k1][0][0]]
    for k in dict:
        dict2[k] = []
        for v in dict[k]:
            if len(v) >1:
                dict2[k]=v[0]
            else:
                dict2[k]+=v

    print(dict2)
    return dict2


def follow_funct_elem(dictionary, key, list):
    for v in dictionary[key]:
        for char in v:
            if char.isupper()  and char not in list:
                list += char
                follow_funct_elem(dictionary, char, list)
    return list


def follow_funct(dictionary):
    dict = {}
    list = []

    for k in dictionary:
        for v in dictionary[k]:

            if v[0].islower():
                list.append(k)

    for k in dictionary:
        for v in dictionary[k]:
            for char in range(len(v)):
                if (v[char] in list) and v[-1] != v[char]:
                    if v[char + 1].isupper():

                        dict[v[char]] = first_funct(dictionary)[v[char-1]]
                        list_of_elem = []
                        if "ε" in dict[v[char]]:
                            dict[v[char]].remove("ε")
                            list_of_elem = []

                        for key in follow_funct_elem(dictionary, v[char], list_of_elem):
                            dict[key] = dict[v[char]]
        if k not in dict:
            dict[k] = []
            dict[k].append("$")

    return dict


def parsing_table(first, follow, dictionary):
    keys = [k for k in dictionary]
    data = {}

    for n in terminals:
        data[n] = '_'

    data['$'] = '_'
    df = pd.DataFrame(data, index=keys)

    for k in dictionary:
        if "ε" in first[k]:
            if "$" in follow[k]:
                df.loc[k, "$"] = "ε"

            else:
                df.loc[k, follow[k]] = "ε"

        for char in first[k]:
            if char != "ε":
                df.loc[k, char] = dictionary[k][0]
    df.loc["X", "$"] = 'ε'
    return df


def lastStep(word, table_of_parsing):
    stack = "$S"
    input = word + '$'
    dict = {}
    dict["Stack"] = ["$S"]
    dict["Input"] = [word]

    while stack != '$':

        if stack[1].islower() and stack[1] == input[0]:
            stack = "$" + stack[2::]
            input = input[1::]

        elif stack[1] == "ε":
            stack = '$' + stack[2::]
        else:
            add_part = stack[1]
            stack = stack[2::]
            stack = '$' + table_of_parsing.loc[add_part, input[0]] + stack

        dict['Stack'].append(stack)
        dict['Input'].append(input)
        print("Stack is :" + stack + "  Input is :" + input)
    print("Stack is :" + stack + "  Input is :" + input)
    print(tabulate(dict, headers=["Stack", "Input"], tablefmt="fancy_grid"))


def check_Grammar(word, table_of_parsing):
    try:
        lastStep(word, table_of_parsing)
        print("Succes grammar!!!")
    except:
        print("Not correct grammar!!! Try again.")


rules = insert_rules(nonterminals)
print_original(rules)

rules_lf = eliminate_lf(rules)
print_lf(rules_lf)

first = first_funct(rules_lf)
follow = follow_funct(rules_lf)
follow = {k: follow[k] for k in first.keys()}  # arrange in needed order

table = {"Nonterminals": [k for k in first.keys()],
         "First": [v for k, v in first.items()],
         "Follow": [v for k, v in follow.items()]}

print(follow_funct(rules_lf))
print(tabulate(table, headers="keys", tablefmt="fancy_grid"))

table_of_parsing = parsing_table(first, follow, rules_lf)
print(table_of_parsing)

word = "adbaacbaaa"

check_Grammar(word, table_of_parsing)


rules = insert_rules(nonterminals)
print_original(rules)

rules_lf = eliminate_lf(rules)
print_lf(rules_lf)

first = first_funct(rules_lf)