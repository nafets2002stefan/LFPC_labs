import copy
import string

INPUT_FILES = [
    'input.txt'
]
INPUT = open(INPUT_FILES[0], 'r').read().split('\n')
EPS = 'e'

# Returns subsets (generator)
def _power_set(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in _power_set(seq[1:]):
            yield [seq[0]] + item
            yield item


def _replace(str, subStr, mask):
    result = []
    for m in mask:
        modified = str
        pos = 1
        for i in m:
            for _ in range(i):
                pos = modified.find(subStr, pos - i)

            modified = modified[:pos] + modified[pos + 1:]
        result.append(modified)
    return result


def _print_rules(rules):
    for key in rules:
        print(key, '->', rules[key])


def _check_epsilon(rules):
    for key in rules:
        for el in rules[key]:
            if el == EPS:
                return True, key

    return False, None

def remove_epsilon(rules):
    local_rules = copy.deepcopy(rules)

    if_epsilon, epsilon_key = _check_epsilon(local_rules)

    while if_epsilon:
        local_rules[epsilon_key].remove(EPS)
        if len(local_rules[epsilon_key]) == 0:
            del local_rules[epsilon_key]

        for key in local_rules:
            for i , el in enumerate(local_rules[key]):
                if epsilon_key in el:
                    if epsilon_key in local_rules:
                        count = el.count(epsilon_key)
                        # Generate list with elements from 1 to previously counted value
                        arr = [i for i in range(1, count + 1)]
                        # Generate all subsets of previous list. This subsets mean the mask by which epsilon_key will be excluded.
                        # E.g., mask [1, 2] means that 1st and 2nd occurences of epsilon_key in production will be excluded.
                        subset = [x for x in _power_set(arr)]
                        add = _replace(el, epsilon_key, subset)[:-1]
                        local_rules[key] = local_rules[key] + add
                    else:
                        if len(local_rules[key][i]) == 1:
                            local_rules[key].remove(epsilon_key)
                        else:
                            local_rules[key][i] = el.replace(epsilon_key, '')

        if_epsilon, epsilon_key = _check_epsilon(local_rules)
    return local_rules

def _check_unit_production(key, rules):
    for el in rules[key]:
        if (len(el) == 1) and (el in rules):
            return True, el

    return False, None


def _remove_unit_production(key, initial_value, rules):
    if_unit_production, value = _check_unit_production(initial_value, rules)

    if if_unit_production:
        rules = _remove_unit_production(initial_value, value, rules)

    rules[key].remove(initial_value)
    rules[key] = rules[key] + rules[initial_value]

    return rules


def _check_terminals(str):
    for letter in str:
        if letter in string.ascii_lowercase:
            return True
    return False


def _check_nonterminals(str, rules):
    for letter in str:
        if letter in rules:
            return True
    return False


def _generate_symbol(pos, rules):
    letters = string.ascii_uppercase

    while letters[pos] in rules:
        pos -= 1

    return letters[pos], pos


def read_rules(inputArr, separator='->'):
    res = {}
    for el in inputArr:
        x = el.split(separator)

        if not x[0] in res:
            res[x[0]] = []

        res[x[0]].append(x[1])

    return res

def remove_unit_production(rules):
    local_rules = copy.deepcopy(rules)
    for key in local_rules:
        if_unit_production, val = _check_unit_production(key, local_rules)
        if if_unit_production:
            local_rules = _remove_unit_production(key, val, local_rules)

    return local_rules


def remove_inaccessible(rules):
    local_rules = copy.deepcopy(rules)
    accessedKeys = set()

    for key in local_rules:
        for el in local_rules[key]:
            for letter in el:
                if (letter in local_rules):
                    accessedKeys.add(letter)

    for key in list(local_rules):
        if key not in accessedKeys:
            del local_rules[key]

    return local_rules


def remove_nonproductive(rules):
    local_rules = copy.deepcopy(rules)

    productives = set()

    for key in local_rules:
        for el in local_rules[key]:
            if (len(el) == 1) and (el not in local_rules):
                productives.add(key)

    call_stack = 1
    while call_stack:
        for key in local_rules:
            if key in productives:
                continue

            for el in local_rules[key]:
                for letter in el:
                    if (letter in productives):
                        productives.add(key)
                        call_stack += 1

        call_stack -= 1

    for key in list(local_rules):
        if key not in productives:
            del local_rules[key]

            for innerKey in list(local_rules):
                for el in local_rules[innerKey]:
                    if key in el:
                        local_rules[innerKey].remove(el)

    return local_rules


def normalize(rules):
    local_rules = copy.deepcopy(rules)

    cache = {}
    terminals = string.ascii_lowercase
    letters_counter = len(string.ascii_uppercase) - 1

    # Change productions that have more than 2 symbols
    call_stack = 1
    while call_stack:
        for key in list(local_rules):
            for i, el in enumerate(local_rules[key]):
                if len(el) > 2:
                    if el in cache:
                        local_rules[key][i] = cache[el]
                    else:
                        symbol, letters_counter = _generate_symbol(letters_counter, local_rules)
                        cache[el] = symbol + el[len(el) - 1]

                        local_rules[symbol] = [el[:len(el) - 1]]
                        local_rules[key][i] = cache[el]

                        call_stack += 1

        call_stack -= 1

    # Change productions that have more than one noneterminal symbol with terminals
    for key in list(local_rules):
        for i, el in enumerate(local_rules[key]):
            if len(el) == 2 and _check_terminals(el):
                if el in cache:
                    local_rules[key][i] = cache[el]
                else:
                    for letter in el:
                        if letter in terminals:
                            if letter in cache:
                                local_rules[key][i] = local_rules[key][i].replace(letter, cache[letter])
                            else:
                                symbol, letters_counter = _generate_symbol(letters_counter, local_rules)
                                cache[letter] = symbol
                                local_rules[cache[letter]] = [letter]
                                local_rules[key][i] = local_rules[key][i].replace(letter, cache[letter])
                    cache[el] = local_rules[key][i]

    return local_rules

rules = read_rules(INPUT)
print("Initial Grammar:")
_print_rules(rules)

rules = remove_epsilon(rules)

rules = remove_unit_production(rules)
# print('REMOVE RENAMINGS')
# print_rules(rules)
rules = remove_inaccessible(rules)
# print('REMOVE INACCESSIBLES')
# print_rules(rules)

rules = remove_nonproductive(rules)
# print('REMOVE NONPRODUCTIVE')
# print_rules(rules)

rules = normalize(rules)
print("The Chomsky Normal Form:")
_print_rules(rules)
