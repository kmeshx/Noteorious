##NAME: KUSHA MAHARSHI

##SECTION: D

##FALL 2017

##15-112 Term Project


from word2number import w2n
import nltk

numberDic = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

numcheckDic = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight","nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen","sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million", "billion", "trillion"}

mathDic = {'times': '*', 'divided by': '/', 'plus': '+', 'minus': '-', 'subtracted from': '-', 'added to': '+', 'over': '/', 'factorial': '!'}

puncDic = {',', '.', ':', '!', '?'}


##Convert to Math and Symbols

def punktRemover(inputStr):
    
    for p in puncDic:
        inputStr = inputStr.replace(p, '')
    return inputStr
    
    
def convertToSymbols(inputStr):
    
    #unpuncStr = punktRemover(inputStr)
    wordArray = inputStr.split(" ")
    llh = len(wordArray)
    
    for wordind in range(llh):
        curword = wordArray[wordind]
        if(wordind>0):
            prevWord = wordArray[wordind-1]
        else:
            prevWord = ''
            
        if(wordind<llh-1):
            nexWord = wordArray[wordind+1]
        else:
            nexWord = ''
            
        if(wordind+2 < llh):
            nexnexWord = wordArray[wordind+2]
        else: 
            nexnexWord = ''
            
        if((curword in mathDic) and (prevWord in numcheckDic) and (nexWord in numcheckDic)):
            #num1 = w2n.word_to_num(prevWord)
            num1, numnum1 = findNumbersPre(wordArray, wordind)
            #print("nn: ", num1, numnum1)
            #num2 = w2n.word_to_num(nexWord)
            num2, numnum2 = findNumbersPost(wordArray, wordind)
            #print("nn2: ", num2, numnum2)
            wordArray[wordind] = str(num1) + " " + mathDic[curword]+" "+ str(num2)
            for ri in range(1, numnum1+1):
                wordArray[wordind-ri] = ''
            for ri in range(1, numnum2+1):
                wordArray[wordind+ri] = ''
            if(wordind > 0):
                wordArray[wordind-1] = ''
            if(wordind < llh-1):
                wordArray[wordind+1]=''
            
        elif(curword+" "+nexWord in mathDic and (prevWord in numcheckDic) and (nexnexWord in numcheckDic)):
            if(wordind+2 < llh):
                nexnexWord = wordArray[wordind+2]
            else: 
                nexnexWord = ''
                
            #num1 = w2n.word_to_num(prevWord)
            num1, numnum1 = findNumbersPre(wordArray, wordind)
            #print("nn: ", numnum1)
            #num2 = w2n.word_to_num(nexnexWord)
            num2, numnum2 = findNumbersPost(wordArray, wordind+1)
            #print("nn2: ", numnum2)
            wordArray[wordind] = str(num1) + " " + mathDic[curword+" "+nexWord]+" "+ str(num2)
            if(wordind > 0):
                wordArray[wordind-1] = ''
            if(wordind < llh-1):
                wordArray[wordind+1]=''
            if(wordind < llh-2):
                wordArray[wordind+2]=''
            for ri in range(1, numnum1+1):
                wordArray[wordind-ri] = ''
            for ri in range(1, numnum2+1):
                wordArray[wordind+1+ri] = ''
            
            numnum2+=1
            
                
    toRetString = ' '.join(wordArray)
    
    toRetString = ' '.join(toRetString.split())
    
    return toRetString
    
    
    
def findNumbersPre(wordArray, wordind):
    nc = 0
    bound = 10
    retnum, curnum = '', ''
    if(wordind - bound < 0):
        bound = wordind
   
    
    #print("b: ", bound)
    retnumnum = bound

    for i in range(1, bound+1):
        #retnumnum+=1
        #subnumstr = ' '.join(wordArray[wordind-i: wordind])
        #print("s", subnumstr)
        
        if(wordArray[wordind-i] not in numcheckDic):
            nc+=1
            retnumnum = i-1
            retnum = w2n.word_to_num(' '.join(wordArray[wordind-i+1: wordind]))
            break
        
        #elif(wordArray[wordind-i] in numcheckDic):
        #retnum = w2n.word_to_num(subnumstr)
            
    if(nc==0):
        return w2n.word_to_num(' '.join(wordArray[wordind-bound:wordind])), bound
          
    return retnum, retnumnum
    
def findNumbersPost(wordArray, wordind):
    nc = 0
    bound = 10
    retnum, curnum = '', ''
    if(wordind + bound > len(wordArray)-1):
        bound = len(wordArray)-1 - wordind
    
    #print("b2: ", bound)
    retnumnum = bound

    for i in range(1, bound+1):
        #retnumnum+=1
        
        """subnumstr = ' '.join(wordArray[wordind+1:wordind+1+i])
        print("s", subnumstr)"""
        
        
        if(wordArray[wordind+i] not in numcheckDic):
            nc+=1
            retnumnum = i-1
            retnum = w2n.word_to_num(' '.join(wordArray[wordind+1: wordind+i]))
            break
        
        """elif(wordArray[wordind+i] in numcheckDic):
            retnum = w2n.word_to_num(subnumstr)"""
        #retnum = w2n.word_to_num(subnumstr)
    if(nc==0):
        return w2n.word_to_num(' '.join(wordArray[wordind+1:wordind+bound+1])), bound
    
    return retnum, retnumnum
    