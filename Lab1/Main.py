import pandas as pd

#Declare the language

Vn = "{S , R , L}"
Vt="{a , b , c , d , e , f}"
P="{S->aS , S->bS , S->cR , S->dL , R->dL , R->e , L->fL , L->eL , L->d}"

#Change the input to work properly
Vn = Vn.replace(" ", "").replace("{", "").replace("}", "").split(",")
Vt = Vt.replace(" ", "").replace("{", "").replace("}", "").split(",")
P = P.replace(" ", "").replace("{", "").replace("}", "").split(",")
#Add the End notations for production rules that point to terminal only characters
Vn.append("End")

#Now we create the matrix with "-"
FiniteAutomate = [["-"] * (len(Vn)) for i in range(len(Vn))]


#Fill the matrix with characters
#This is the version for regular grammar X->yZ or X->y

#For every phrase we should do properly
for phrase in P:
    #Check if last element is Upper Case-non terminal
    if phrase[len(phrase) - 1].isupper():
        #Now we place the terminal symbol(lowercase) in FA in that way that the row is the variable on the left and the column is variable on the right
        FiniteAutomate[Vn.index(phrase[0])][Vn.index(phrase[len(phrase) - 1])]=phrase[3]
    else:
        #In other case (when last element is a terminal one(lowercase) then we place it in the row is the variable on the left and the column the last char from phrase
        FiniteAutomate[Vn.index(phrase[0])][-1]=phrase[3]

#Put in Dataframe to be more convinient to watch
FANames = []
for i in range(len(Vn)):
    FANames.append("q" + str(i))
FiniteAutomata=pd.DataFrame(FiniteAutomate, index=FANames, columns=FANames)
print(FiniteAutomata)



#Check if a word is correct and corresponds to vocabulary

text = input("Introduce a word to verify if accepted by FA: ")

#If fl is 1 it means that is not correct
fl = 0
#Variable that keeps the current nonterminal symbol and we start from S it means 0
keep = 0

#Check for each phrase
for i in range(len(text)):
    #If it is not containing in vocabulary(terminal symbols)
    if text[i] not in Vt:
        fl = 1
        break
    #Check if the last letter is not in the terminal column of current row, the text cant exist in the vocabulary
    if i == len(text)-1 and not FiniteAutomate[keep][-1] == text[i]:
        fl = 1
        break
    else:
        #Finding the next nonterminal variable based on the connecting letter
        if text[i] in FiniteAutomate[keep][:-1]:
            keep = FiniteAutomate[keep].index(text[i])

if fl ==0:
    print("It is accepted by vocabulary")
else:
    print("It is not accepted by vocabulary")