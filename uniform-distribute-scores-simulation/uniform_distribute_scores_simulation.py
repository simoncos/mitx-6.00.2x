# -*- coding: utf-8 -*-
import random
import pylab

def sampleQuizzes():

    '''
    You are taking a class that plans to assign final grades based on two midterm quizzes and a final exam. 
    The final grade will be based on 25% for each midterm, and 50% for the final. 
    You are told that the grades on the exams were each uniformly distributed integers:
    
    Midterm 1: 50 <= grade <= 80
    
    Midterm 2: 60 <= grade <= 90
    
    Final Exam: 55 <= grade <= 95
    
    Write a function called sampleQuizzes() that implements a Monte Carlo simulation that estimates the probability of a student having a final score >= 70 and <= 75. Assume that 10,000 trials are sufficient to provide an accurate answer.
    '''

    num = 0
    for t in range(10000):
        midterm1 = random.choice(range(50,81))
        midterm2 = random.choice(range(60,91))
        final = random.choice(range(55,96))
        score = midterm1*0.25 + midterm2*0.25 + final*0.5 
        if score >=70 and score<=75:
            num += 1
    return num / float(10000)

def generateScores(numTrials):
    scores = []
    for t in range(numTrials):
        midterm1 = random.choice(range(50,81))
        midterm2 = random.choice(range(60,91))
        final = random.choice(range(55,96))
        score = midterm1*0.25 + midterm2*0.25 + final*0.5 
        scores.append(score)
    return scores

def plotQuizzes():
    
    '''
    Write a procedure called plotQuizzes() that produces 
    a plot of the distribution of final scores for all of the trials. 
    Try your best to match exactly how the histogram below looks 
    (including the bins, titles and labels on the axes).
    '''
    scores = generateScores(10000)
    pylab.hist(scores,7)
    pylab.ylabel('Number of Trials')
    pylab.xlabel('Final Scores')
    pylab.title('Distribution of Scores')
    pylab.show()

def probTest(limit):

    '''
    You observe that the probability of first seeing a 1 on the n-th roll decreases as n increases. 
    You would like to know the smallest number of rolls such that this probability is less than some limit. 
    Complete the Python procedure, probTest(limit), to compute this.
    '''
    
    # monte carlo仿真法，发现random.choice()不如想象中均匀
    
    prob = 1
    n = 0
    
    while prob >= limit:
        n += 1
        # print n         
        numBingo = 0
        for trial in range(10000): 
            rollList = []
            for roll in range(n):
                roll = random.choice([1,2,3,4,5,6])
                rollList.append(roll)
            # print rollList
            lastRoll = rollList.pop()
            if 1 not in rollList and lastRoll == 1:
                numBingo += 1
        prob = numBingo / float(10000)
        # print prob
    return n

def probTest_probability(limit): #直接使用概率来算
    n = 1
    while 5.0**(n-1)/6.0**n > limit:
        n += 1
    return n