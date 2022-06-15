word = "abac"

word = list(word)
letter =input()
def printCases(word,ls):

    if word not in ls:
        ls.append(''.join(word))
    for i in range(len(word)):
        if word[i] == letter:
            printCases(word[0:i]+word[i+1:],ls)

    return ls
ls =[]
print(printCases(word,ls))
