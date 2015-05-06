'''
For this problem you are going to simulate growth of fox and rabbit population in a forest.

The following facts are true about the fox and rabbit population:

The maximum population of rabbits is determined by the amount of vegetation in the forest, which is relatively stable.

There are never fewer than 10 rabbits; the maximum population of rabbits is 1000.

For each rabbit during each time step, a new rabbit will be born with a probability of prabbit reproduction
prabbit reproduction= 1.0 − current rabbit population / max rabbit population
In other words, when the current population is near the maximum, the probability of giving birth is very low, and when the current population is small, the probability of giving birth is very high.

The population of foxes is constrained by number of rabbits.

There are never fewer than 10 foxes.

At each time step, after the rabbits have finished reproducing, a fox will try to hunt a rabbit with success rate of pfox eats rabbit
pfox eats rabbit = current rabbit population / max rabbit population
In other words, the more rabbits, the more likely a fox will eat one.

If a fox succeeds in hunting, it will decrease the number of rabbits by 1 immediately. Remember that the population of rabbits is never lower than 10.

Additionally, if a fox succeeds in hunting, then it has a 1/3 probability of giving birth in the current time-step.

If a fox fails in hunting then it has a 10 percent chance of dying in the current time-step.

If the starting population is below 10 then you should do nothing. You should not increase the population nor set the population to 10. 
Start with 500 rabbits and 30 foxes.

At the end of each time step, record the number of foxes and rabbits.

Run the simulation for 200 time steps, and then plot the population of rabbits and the population of foxes as a function of time step.

Use the following steps, and the template file exam_problem3.py (click to download .py file), as guides in your implementation of this simulation.

Step 1: Write the procedure, rabbitGrowth, that updates the number of rabbits during the first part of a time step

Step 2: Write the procedure, foxGrowth, that updates the number of rabbits and foxes during the second part of a time step

Step 3: Write the master procedure, runSimulation, that loops for some amount of time steps, doing the first part and then the second part of the simulation. Record the two populations in two different lists, and return those lists.
'''

import random
import pylab

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
CURRENTFOXPOP = 30

def rabbitGrowth():
    """ 
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up, 
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP
    # if MAXRABBITPOP == 1000 and CURRENTRABBITPOP  == 500:
    #     CURRENTRABBITPOP += 1
    if CURRENTRABBITPOP < MAXRABBITPOP:
        if random.random() <= (1.0 - CURRENTRABBITPOP/float(MAXRABBITPOP)):
            CURRENTRABBITPOP += 1
            
def foxGrowth():
    """ 
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat 
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP

    # if CURRENTRABBITPOP == 1000 and MAXRABBITPOP == 1000 and CURRENTFOXPOP == 50:
    #     CURRENTFOXPOP += 1 
    if random.random() <= CURRENTRABBITPOP/float(MAXRABBITPOP):
        CURRENTRABBITPOP -= 1
        if random.random() <= 1/float(3):
            CURRENTFOXPOP += 1
    else:
        if CURRENTFOXPOP > 10:
            if random.random() <= 1/float(10):
                CURRENTFOXPOP -= 1
    
            
def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the 
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """
    rabbitPopList, foxPopList = [],[]
    for s in range(numSteps):
        rabbitGrowth()
        foxGrowth()
        rabbitPopList.append(CURRENTRABBITPOP)
        foxPopList.append(CURRENTFOXPOP)
    return rabbitPopList,foxPopList

a = runSimulation(200)

coeff_r = pylab.polyfit(range(len(a[0])), a[0], 2)
coeff_f = pylab.polyfit(range(len(a[1])), a[1], 2)

pylab.subplot(211)
pylab.plot(pylab.polyval(coeff_r, range(len(a[0]))))

pylab.subplot(212)
pylab.plot(pylab.polyval(coeff_f, range(len(a[1]))))

pylab.show()