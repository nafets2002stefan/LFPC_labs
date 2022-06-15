import string

def check_LR(P):
    for key in P:
        for value in P[key]:
            if value[0] == key:
                return True, key

    return False, ''


def check_LF(P):
    for key in P:
        for value in P[key]:
            if value.find(key) > -1:
                return True, key

    return False, ''


def check_F(F, NT):
    for key in F:
        for value in F[key]:
            if value[0] in NT:
                return True

    return False



class LL1:

    def __init__(self, file):
        with open(file) as f:
            input_lines = f.read().split('\n')

        # Defining variables
        self.non_terminal = list(input_lines[0].split())
        self.terminal = list(input_lines[1].split())
        self.start = self.non_terminal[0]
        self.available_letters = list(string.ascii_uppercase)
        for char in self.non_terminal:
            self.available_letters.remove(char)
        self.P = {}
        self.new_value = False

        #Read the grammar
        for line in input_lines[2:]:
            key, value = line.split()

            if key in self.P:
                self.P[key].append(value)
            else:
                self.P[key] = [value]

    def print(self):
        print('P={')
        for key in self.P:
            print(key, '-> ', end='')
            i = 0
            for value in self.P[key]:

                if i >= 1:
                    print('|', end='')

                # Replacing _ with ε symbol
                if value == '_':
                    print('ε', end='')
                    i += 1
                else:
                    print(value + '', end='')
                    i += 1

            print()
        print('}')

    def Parse(self, word):
        self.print()
        self.Step1()
        self.Step2()
        self.Step3()
        self.Step4()
        self.Step5()
        self.Step6(word)

    def Step1(self):
        LR, key = check_LR(self.P)
        if LR:
            self.Left_Recursion_Elimination(key)
            self.print()
            self.Step1()
        else:
            return

    def Left_Recursion_Elimination(self, key):
        print('Eliminate Left Recursion for', key)
        alpha = []
        beta = []
        letter = self.available_letters[0]
        self.available_letters.remove(letter)
        self.non_terminal.append(letter)
        for value in self.P[key]:
            if value[0] == key:
                alpha.append(value[1:] + letter)
            elif value == '_':
                beta.append(letter)
            else:
                beta.append(value + letter)

        del self.P[key]
        self.P[key] = beta
        self.P[letter] = alpha
        self.P[letter].append('_')

    def Step2(self):
        LF, key = check_LF(self.P)
        if LF:
            self.Left_Factoring_Elimination(key)
            self.print()
            self.Step2()
        else:
            return

    def Left_Factoring_Elimination(self, key):
        print('Eliminate Left Factoring for', key)
        T = []
        T.extend(self.P[key])
        min = 100
        for i in range(0, len(T)):
            if len(T[i]) < min:
                min = len(T[i])
            if T[i] == '_':
                T.remove('_')
        if len(T) == 1:
            i = 0
        else:
            for i in range(0, min):
                l = T[0][i]
                for value in T:
                    if (value[i] != l) or (value[i] == key):
                        break
            i += 1
        alpha = []
        beta = []
        letter = self.available_letters[0]
        self.available_letters.remove(letter)
        self.non_terminal.append(letter)

        for value in self.P[key]:
            if value != '_':
                alpha.append(value[:i] + letter)
                beta.append(value[i:])
            else:
                alpha.append('_')

        if '' in beta:
            beta.remove('')
            beta.append('_')

        self.P[key] = list(set(alpha))
        self.P[letter] = list(set(beta))

    # First
    def Step3(self):
        self.First = {}
        for key in self.non_terminal:
            self.First[key] = []
        for key in self.P:
            for value in self.P[key]:
                if (value[0] in self.terminal):
                    self.First[key].append(value[0])
                else:
                    self.First[key].append(value)
                self.First[key] = list(set(self.First[key]))

        while (check_F(self.First, self.non_terminal)):
            for key in self.First:
                tab = []
                for value in self.First[key]:
                    if (value[0] in self.non_terminal) and ('_' in self.First[value[0]]) and (len(value) > 1):
                        tab.extend(self.First[value[0]])
                        tab.remove('_')
                        tab.append(value[1:])
                    elif (value[0] in self.non_terminal):
                        tab.extend(self.First[value[0]])
                    else:
                        tab.append(value)
                tab = list(set(tab))
                self.First[key] = tab

    # Follow
    def Step4(self):
        self.Follow = {}
        for key in self.non_terminal:
            self.Follow[key] = []

        self.Follow['S'].append('$')
        for key in self.P:
            for value in self.P[key]:
                for i in range(0, len(value)):
                    if value[i] in self.non_terminal:
                        if i == len(value) - 1:
                            self.Follow[value[i]].append(key)
                        elif value[i + 1] in self.terminal:
                            self.Follow[value[i]].append(value[i + 1])
                        else:
                            tab = self.First[value[i + 1]]
                            if '_' in tab:
                                tab.remove('_')
                                tab.append(key)
                            self.Follow[value[i]].extend(tab)

        while (check_F(self.Follow, self.non_terminal)):
            for key in self.Follow:
                tab = []
                for value in self.Follow[key]:
                    if (value in self.non_terminal) and (key not in self.Follow[value]):
                        tab.extend(self.Follow[value])
                    elif value in self.terminal or value == '$':
                        tab.append(value)
                tab = list(set(tab))
                self.Follow[key] = tab

    # Adj. Table
    def Step5(self):
        self.collumn = {}
        i = 0
        for key in self.terminal:
            self.collumn[key] = i
            i += 1
        self.collumn['$'] = i

        self.rows = {}
        for key in self.non_terminal:
            self.rows[key] = [''] * (len(self.terminal) + 1)

        for key in self.P:
            for value in self.P[key]:
                a = []
                b = []
                if value[0] in self.terminal:
                    a.append(value[0])
                elif value[0] in self.non_terminal:
                    a.extend(self.First[value[0]])
                    if '_' in a:
                        a.remove('_')
                        b.extend(self.Follow[key])
                elif value == '_':
                    b.extend(self.Follow[key])
                for ter in b:
                    self.rows[key][self.collumn[ter]] = '_'
                for ter in a:
                    self.rows[key][self.collumn[ter]] = value

    def Step6(self, word):
        Stack = 'S$'
        Input = word + '$'
        Err = False
        print(' Stack |    Input    | Action ')
        print('------------------------------')
        while (not Err):
            space1 = ' ' * (7 - len(Stack))
            space2 = ' ' * (12 - len(Input))
            print(Stack + space1 + '|', Input + space2 + '|', end=' ')
            Err, Stack, Input, Action = self.Act(Stack, Input)
            print(Action)

        print()
        if Stack == '$' and Input == Stack:
            print('Success!')
        else:
            print('Error: the word is not correct')

    def Act(self, Stack, Input):
        if Stack == '$':
            return True, Stack, Input, 'Done!'
        if Stack[0] == Input[0]:
            return False, Stack[1:], Input[1:], '-'
        new = self.rows[Stack[0]][self.collumn[Input[0]]]
        if new == '_':
            return False, Stack[1:], Input, 'ε'
        elif new != '_':
            return False, new + Stack[1:], Input, new
        else:
            return True, '', '', ''


L = LL1('input.txt')
L.Parse('dbaacbaaa')
