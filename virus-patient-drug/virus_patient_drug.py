# -*- coding: utf-8 -*-
# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        
        if random.random() < self.getClearProb():
            return True
        else:
            return False
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        
        if random.random() < self.getMaxBirthProb() * (1.0 - popDensity):
                return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        
class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)        


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        
        viruses_copy = self.viruses[:]
        for v in viruses_copy:
            if v.doesClear() == True:
                self.viruses.remove(v)
        
        self.popDensity = len(self.viruses) / float(self.maxPop)
        
        viruses_copy_new = self.viruses[:]
        for v in viruses_copy_new:
            try:
                newVirus = v.reproduce(self.popDensity)
                if newVirus != None:    # 剔除未生产子代，reproduce()只抛异常，返回为None
                    self.viruses.append(newVirus)
                else:
                    raise NoChildException() #异常处理，直接continue进入下一次循环
            except NoChildException:
                continue
                    
        return len(self.viruses)


#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    sumPopList = [0 for n in range(300)]
    
    for t in range(numTrials):
        
        # 初始化Patient
        viruses = []
        virus = SimpleVirus(maxBirthProb,clearProb)
        for v in range(numViruses):
            viruses.append(virus)
        patient = Patient(viruses,maxPop)
        
        # 将每次trial得到的结果加到之前所有结果的sum之中
        for timestep in range(300):
            patient.update()
            sumPopList[timestep] += patient.getTotalPop()
    
    # 将最后得到的sum处理为average
    averagePopList =[]
    for a in sumPopList:
        averagePopList.append(a / float(numTrials))
    
    pylab.plot([n for n in range(300)],averagePopList) # 两个参数均为list，分别对应x-label和y-label
    pylab.xlabel('timestep') # 先plot，再加label、legend、title，最后show
    pylab.ylabel('averagePop in each of 300 timesteps')
    pylab.legend(['averagePopWithoutDrug']) # 不加[]则只显示出来一个a
    pylab.title('Simulation Without Drugs')
    pylab.show()
#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        SimpleVirus.__init__(self,maxBirthProb,clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if not self.resistances.has_key(drug): #药物抵抗列表中不存在的药物，默认为不抵抗（原题要求中未提到）
            return False
        return self.resistances[drug] #字典类型，取值用[]


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        # 检查这个virus particle 是否对所有激活的drugs抵抗，如果否，reproduce()无后续行为（return了）
        for d in activeDrugs:
            if not self.isResistantTo(d):
                return None

        if random.random() < self.maxBirthProb * (1 - popDensity):
            newResistances = dict(self.resistances)
            for r in self.resistances:
                if random.random() < self.mutProb: # 抗性反向变异
                    newResistances[r] = not newResistances[r]
            return ResistantVirus(self.maxBirthProb,self.clearProb,newResistances,self.mutProb)
        

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self,viruses,maxPop)
        self.postcondition = [] #初始化在该Patient上被激活的drugs

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        
        if newDrug not in self.postcondition: 
            self.postcondition.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.postcondition


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        resistantVirusList = self.getViruses()[:]
        for virus in self.getViruses():
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    resistantVirusList.remove(virus)
                    break #若发现该virus对某种drug不抵抗，将其删除，并break drug循环，结束该virus循环
        return len(resistantVirusList)



    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        viruses_copy = self.viruses[:]
        for v in viruses_copy:
            if v.doesClear() == True:
                self.viruses.remove(v)
        
        self.popDensity = len(self.viruses) / float(self.maxPop)
        
        viruses_copy_new = self.viruses[:]
        for v in viruses_copy_new:
            try:
                newVirus = v.reproduce(self.popDensity,self.postcondition) # 此处参数与另一个update()中不同
                if newVirus != None:    # 剔除未生产子代，reproduce()只抛异常，返回为None
                    self.viruses.append(newVirus)
                else:
                    raise NoChildException() #异常处理，直接continue进入下一次循环
            except NoChildException:
                continue
                    
        return len(self.viruses)



#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    sumPopList = [0 for n in range(300)]
    sumPopList_resistant = [0 for n in range(300)]
    
    for t in range(numTrials):
        
        # 初始化Patient
        viruses = []
        virus = ResistantVirus(maxBirthProb,clearProb,resistances,mutProb)
        for v in range(numViruses):
            viruses.append(virus)

        patient = TreatedPatient(viruses,maxPop)

        # 未加入guttagonol的迭代
        for timestep in range(0,150):
            patient.update()
            sumPopList[timestep] += patient.getTotalPop()
            sumPopList_resistant[timestep] += patient.getResistPop(['guttagonol']) 

        # 加入guttagonol，再进行迭代
        patient.addPrescription('guttagonol')
        for timestep in range(150,300):
            patient.update()
            sumPopList[timestep] += patient.getTotalPop()
            sumPopList_resistant[timestep] += patient.getResistPop(patient.postcondition) # 在这个仿真中，patient.getResistPop(['guttagonol']) 也可以

    # 将最后得到的sum处理为average
    averagePopList = []
    averagePopList_resistant = []
    for sumPop in sumPopList:
        averagePopList.append(sumPop / float(numTrials))
    for sumPop_resistant in sumPopList_resistant:
        averagePopList_resistant.append(sumPop_resistant / float(numTrials))

    pylab.plot([n for n in range(300)],averagePopList)
    pylab.plot([n for n in range(300)],averagePopList_resistant)
    pylab.xlabel('timestep') # 先plot，再加label、legend、title，最后show
    pylab.ylabel('averagePop in each of 150 timesteps')
    pylab.legend(('total virus popluation','guttagonol-resistant virus population')) 
    pylab.title('Simulation With/Without Drug guttagonol')
    pylab.show()