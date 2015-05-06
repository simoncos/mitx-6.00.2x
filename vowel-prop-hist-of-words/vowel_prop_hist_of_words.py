# -*- coding: utf-8 -*-
import pylab

# You may have to change this path
WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of uppercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def plotVowelProportionHistogram(wordList, numBins=15):
    """
    Plots a histogram of the proportion of vowels in each word in wordList
    using the specified number of bins in numBins
    """
    propList=[]
    for word in wordList:
        print word # 测试用
        vowel=0.0
        for s in word:
            if s in ['a','e','i','o','u']:
                vowel += 1
        prop=vowel/float(len(word))    
        propList.append(prop)
    pylab.hist(propList,numBins)      
    pylab.title('Vowel Proportion Histogram of ' + WORDLIST_FILENAME)
    pylab.xlabel('Vowel Proportion')
    pylab.ylabel('Number of Words of Specific Vowel Proportion')
    pylab.show()

if __name__ == '__main__':
    wordList = loadWords()
    plotVowelProportionHistogram(wordList)
