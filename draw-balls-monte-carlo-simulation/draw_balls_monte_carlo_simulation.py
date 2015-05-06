# -*- coding: utf-8 -*-
import random

def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3 
    balls of the same color were drawn.
    '''
    
    yes = 0.0
        
    for n in range(numTrials):
        balls = [1,1,1,0,0,0]
        result = []
        for draw in range(3):
            random.shuffle(balls)
            result.append(balls.pop()) # 将球取出并放入result中
        if result == [1,1,1] or result == [0,0,0]:
            yes += 1
    return yes / numTrials

                        
#### 以下为参考答案代码

#def oneTrial():
#    '''
#    Simulates one trial of drawing 3 balls out of a bucket containing
#    3 red and 3 green balls. Balls are not replaced once
#    drawn. Returns True if all three balls are the same color,
#    False otherwise.
#    '''
#    balls = ['r', 'r', 'r', 'g', 'g', 'g']
#    chosenBalls = []
#    for t in range(3):
#        # For three trials, pick a ball
#        ball = random.choice(balls)
#        # Remove the chosen ball from the set of balls
#        balls.remove(ball) # 只会移除第一个值相符的元素
#        # and add it to a list of balls we picked
#        chosenBalls.append(ball)
#    # If the first ball is the same as the second AND the second is the same as the third,
#    #  we know all three must be the same color.
#    if chosenBalls[0] == chosenBalls[1] and chosenBalls[1] == chosenBalls[2]:
#        return True
#    return False
#
#def noReplacementSimulation(numTrials):
#    '''
#    Runs numTrials trials of a Monte Carlo simulation
#    of drawing 3 balls out of a bucket containing
#    3 red and 3 green balls. Balls are not replaced once
#    drawn. Returns the a decimal - the fraction of times 3 
#    balls of the same color were drawn.
#    '''
#    numTrue = 0
#    for trial in range(numTrials):
#        if oneTrial():
#            numTrue += 1
#
#    return float(numTrue)/float(numTrials)

print noReplacementSimulation(100)  # test      
