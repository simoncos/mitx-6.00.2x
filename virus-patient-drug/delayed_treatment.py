# -*- coding: utf-8 -*-
# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from virus_patient_drug import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    finalPopList_a = []
    finalPopList_b = []
    finalPopList_c = []
    finalPopList_d = []    
    
    for t in range(numTrials):
                
        # 初始化Patient
        viruses_a = []
        virus = ResistantVirus(0.1,0.05,{'guttagonol': False},0.005)
        for v in range(100):
            viruses_a.append(virus)
        viruses_b = viruses_a[:]
        viruses_c = viruses_a[:]
        viruses_d = viruses_a[:]

        patient_a = TreatedPatient(viruses_a,1000)
        patient_b = TreatedPatient(viruses_b,1000)
        patient_c = TreatedPatient(viruses_c,1000)
        patient_d = TreatedPatient(viruses_d,1000)

        # 未加入guttagonol的迭代,d的治疗未delay
        for timestep in range(0,300):
            patient_a.update()
            
        for timestep in range(0,150):
            patient_b.update()
            
        for timestep in range(0,75):
            patient_c.update()        
        
        # 加入guttagonol，再进行迭代
        patient_a.addPrescription('guttagonol')
        patient_b.addPrescription('guttagonol')
        patient_c.addPrescription('guttagonol')
        patient_d.addPrescription('guttagonol')

        for timestep in range(300,300 + 150):
            patient_a.update()
        for timestep in range(150,150 + 150):
            patient_b.update()
        for timestep in range(75,75 + 150):
            patient_c.update()
        for timestep in range(0,0 + 150):
            patient_d.update()
    
        finalPopList_a.append(patient_a.getTotalPop())
        finalPopList_b.append(patient_b.getTotalPop())
        finalPopList_c.append(patient_c.getTotalPop())
        finalPopList_d.append(patient_d.getTotalPop())

    
    pylab.subplot(2,2,1)
    pylab.hist(finalPopList_a)
    pylab.ylabel('Number of Trials')
    pylab.title('Treatment Delayed 300')

    pylab.subplot(2,2,2)
    pylab.hist(finalPopList_b)
    pylab.ylabel('Number of Trials')
    pylab.title('Treatment Delayed 150')
    
    pylab.subplot(2,2,3)
    pylab.hist(finalPopList_c)
    pylab.xlabel('Final Virus Population') # 先plot，再加label、legend、title，最后show
    pylab.ylabel('Number of Trials')
    pylab.title('Treatment Delayed 75')

    pylab.subplot(2,2,4)
    pylab.hist(finalPopList_d)
    pylab.xlabel('Final Virus Population') # 先plot，再加label、legend、title，最后show
    pylab.ylabel('Number of Trials')
    pylab.title('Treatment Delayed 0')    
    
    
    pylab.show()


#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """

    finalPopList_a = []
    finalPopList_b = []
    finalPopList_c = []
    finalPopList_d = []    
    
    for t in range(numTrials):
                
        # 初始化Patient
        viruses_a = []
        virus = ResistantVirus(0.1,0.05,{'guttagonol': False, 'grimpex': False},0.005)
        for v in range(100):
            viruses_a.append(virus)
        viruses_b = viruses_a[:]
        viruses_c = viruses_a[:]
        viruses_d = viruses_a[:]

        patient_a = TreatedPatient(viruses_a,1000)
        patient_b = TreatedPatient(viruses_b,1000)
        patient_c = TreatedPatient(viruses_c,1000)
        patient_d = TreatedPatient(viruses_d,1000)

        # 未加入guttagonol的迭代
        for timestep in range(0,150):
            patient_a.update()
            patient_b.update()
            patient_c.update()
            patient_d.update()        
        
        # 加入guttagonol，再进行迭代
        patient_a.addPrescription('guttagonol')
        patient_b.addPrescription('guttagonol')
        patient_c.addPrescription('guttagonol')
        patient_d.addPrescription('guttagonol')

        for timestep in range(150,150 + 300):
            patient_a.update()
        for timestep in range(150,150 + 150):
            patient_b.update()
        for timestep in range(150,150 + 75):
            patient_c.update()
        for timestep in range(150,150 + 0):
            patient_d.update()

        # 加入grimpex，再进行迭代
        patient_a.addPrescription('grimpex')
        patient_b.addPrescription('grimpex')
        patient_c.addPrescription('grimpex')
        patient_d.addPrescription('grimpex')

        for timestep in range(150):
            patient_a.update()
            patient_b.update()
            patient_c.update()
            patient_d.update()

        finalPopList_a.append(patient_a.getTotalPop())
        finalPopList_b.append(patient_b.getTotalPop())
        finalPopList_c.append(patient_c.getTotalPop())
        finalPopList_d.append(patient_d.getTotalPop())

    
    pylab.subplot(2,2,1)
    pylab.hist(finalPopList_a)
    pylab.ylabel('Number of Trials')
    pylab.title('Second Drug Delayed 300')

    pylab.subplot(2,2,2)
    pylab.hist(finalPopList_b)
    pylab.ylabel('Number of Trials')
    pylab.title('Second Drug Delayed 150')
    
    pylab.subplot(2,2,3)
    pylab.hist(finalPopList_c)
    pylab.xlabel('Final Virus Population') 
    pylab.ylabel('Number of Trials')
    pylab.title('Second Drug Delayed 75')

    pylab.subplot(2,2,4)
    pylab.hist(finalPopList_d)
    pylab.xlabel('Final Virus Population') # 先plot，再加label、legend、title，最后show
    pylab.ylabel('Number of Trials')
    pylab.title('Second Drug Delayed 0')    
    
    
    pylab.show()
