from difflib import SequenceMatcher
import string
from tabulate import tabulate

input = "input.txt"
with open(input) as f:
    input_lines = f.read().split('\n')

nonterminals = input_lines[0].split(" ")



def insert_rules(nonterminals):     #create dict to insert values
    dictionar = {}
    for letter in nonterminals:
        if letter not in dictionar :
            dictionar[letter] = []
    for rule in input_lines[1:]:
        rule = rule.split(" ")
        dictionar[rule[0]].append(rule[1])
    return dictionar

def print_original(dict):       #prints original rules
    print("Original rules:")
    print("P = {")
    for k in dict:
        print(k, " -> ", " | ".join(dict[k]))
    print("}")

def common_part(list):      #takes common part to rename it(means to add new nonterminal)
    string2 = list[0]
    for i in range(1, len(list)):
        string1 = string2
        string2 = list[i]
        match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
    final_common = (string1[match.a: match.a + match.size])
    return final_common

def eliminate_lf(dictionar):        #check if a nonterminal derives into 2 or more variables,and introduce new nonterminals
    dictionar_new = {}
    alphabet = string.ascii_uppercase
    alphabet = list(alphabet)
    alphabet.reverse()
    count = 0
    for k in dictionar:
        for v in dictionar[k]:
            dictionar_new[k] = []
            if len(dictionar[k])<2:
                dictionar_new[k].append(v)
            else:
                dictionar_new[alphabet[count]] = []
                dictionar_new[k].append(common_part( dictionar[k] ) + alphabet[count])
                dictionar_new[alphabet[count]].append(v.removeprefix(common_part(dictionar[k]) ) )
                dictionar_new[alphabet[count]]+="ε"
        count+=1

    return dictionar_new

def print_lf(dict):
    print()
    print("After removing left factoring:")
    print("P = {")
    for k in dict:
        print(k," -> "," | ".join(dict[k]))
    print('}')
    print()

def first_each_elem(dictionary,nonterm):
    result = []
    for v in dictionary[nonterm]:
        for char in v:
            if char.islower():
                result += char
                break
            else :
                result += first_each_elem(dictionary,char)
                break
    return result

def first_funct(dictionary):
    dict = {}
    for k in dictionary:
        dict[k] = first_each_elem(dictionary,k)
    return dict

def follow_funct_elem(dictionary,key):
    result = []
    for k in dictionary:
        for v in dictionary[k]:
            for char in range(len(v)-1):
                if key == v[char] and v[char+1].islower():
                    result+=v[char+1]
            if v[-1] == key and v[-1] != k:
                result += follow_funct_elem(dictionary,k)

    return result

def follow_funct(dictionary):
    dict = {}
    for k in dictionary:
        dict[k] = follow_funct_elem(dictionary,k)

    return dict

rules = insert_rules(nonterminals)
print_original(rules)

rules_lf = eliminate_lf(rules)
print_lf(rules_lf)


first = first_funct(rules_lf)
print(first)
table = {"Nonterminals":[k for k in first.keys()],"First":[v for k,v in first.items()],"Follow":["-","-","-","-","-","-"]}
print(follow_funct(rules_lf))
print(tabulate(table,headers="keys",tablefmt="fancy_grid"))