import csv
import numpy as np
import math
import time
import random
import  propertyCheck as propCheck
from random import randint
import sys
sys.path.append('..')
from python.nnet import *
import Script.propSpecification as ps
import genInputsFromVnnlib as genSpec
import os


def sampling(inVals,numOutputs):
   oVals=[]
   outputs=[]
   oVals = nnet.evaluate_network(inVals)
   len1=len(oVals)
   for i in range(numOutputs):
      outputs.append(oVals[i])
   return outputs
    

def learning(cpos,cneg,iRange,numInputs):
    for i in range (len(cneg)):
        nodeSelect = randint(0,int(numInputs)-1)
        cp=cpos[0][0]
        cn=cneg[i][0]
        cposInVal=cp[nodeSelect]
        cnegInVal=cn[nodeSelect]
        if( cposInVal > cnegInVal):
            temp = round(random.uniform(cnegInVal, cposInVal), 6)
            if ( temp <= iRange[nodeSelect][1] and temp >= iRange[nodeSelect][0]):
                iRange[nodeSelect][0]=temp
        else:
            if (cposInVal < cnegInVal):
                temp = round(random.uniform(cposInVal, cnegInVal), 6)
                if ( temp <= iRange[nodeSelect][1] and temp >= iRange[nodeSelect][0]):
                   iRange[nodeSelect][1]=temp

def makeSample(numInputs,numOutputs,mat1,samples,start_time,pNum,num):
    sampleInputList=[]
    numSamples=numInputs*30   # 30 times of number of inputs
    print(mat1)
    for k in range(numSamples):
        j=0
        while( j < 5):
            inValues=[]
            for i in range(numInputs):
                inValues.append(round(random.uniform(mat1[i][0],mat1[i][1]),6))
            if ( inValues in sampleInputList):
                print("Duplicate",j,inValues,sampleInputList)
                j=j+1
            else :
                break
        sampleInputList.append(inValues)
        sampleVal=sampling(inValues,numOutputs)
        print(sampleVal)
        retVal=  ps.checkPropSpec(sampleVal) 
        if retVal  == 1:
            print("Input Range :", inValues)
            print("Sample Value obtained :", sampleVal)
            timeTaken = (time.clock() - start_time)
            #print("Time taken :: %.4f" %(timeTaken))
            print("Number of samples :: ", num*numSamples+k+1)
            return 0
            #exit(1)
        s=[]
        s.append(inValues)
        s.append(sampleVal)
        samples.append(s)
    print("Sample::",samples)
    return 1

def runSample(numInputs,numOutputs,mat1,tAndOT,start_time,pnum):
    k=0
    oldPosSamples=[]
    target = tAndOT[0]
    objectiveType = tAndOT[1]
    while (k != 100):
        print("------------------------------------------------")
        print(k)
        print("------------------------------------------------")
        samples=[]
        posSamples=[]
        negSamples=[]
        ret = makeSample(numInputs,numOutputs,mat1,samples,start_time,pnum,k)
        if ( ret == 0):
           #timeTaken = (time.clock() - start_time)
           #print("Time taken :: %.4f" %(timeTaken))
           return 1

        if ( objectiveType == 1) :
           propCheck.checkAndSegregateSamplesForMinimum(posSamples,negSamples,samples,oldPosSamples,target)
        else:
           propCheck.checkAndSegregateSamplesForMaximum(posSamples,negSamples,samples,oldPosSamples,target)
        oldPosSamples=posSamples
        flag=False
        for i in range(numInputs):
            if ( mat1[i][1] - mat1[i][0] > 0.000001):
               flag=True
               break;
        print("Input Range",mat1,len(posSamples[0][0]),len(samples[0]))
        print("Output value ::",posSamples[0][1])
        if( flag == False):
           print("\n\n !!! No further sampling Possible for this iteration!!!")
           timeTaken = (time.clock() - start_time)
           print("Time taken :: %.4f" %(timeTaken))
           exit()
        learning(posSamples,negSamples,mat1,numInputs)
        k=k+1
    return 0

#Main function

start_time = time.clock()
pNum = sys.argv[1]
print("Property Verifying for :: ",pNum)

f1Name=sys.argv[3]
f2Name=sys.argv[4]
mat1 = genSpec.generateInputBounds(f1Name)

targetAndType = propCheck.findObjectiveFuncionType(f2Name)
nnet = NNet(sys.argv[2])

print("Num Inputs: %d"%nnet.num_inputs())
print("Num Outputs: %d"%nnet.num_outputs())
numOutputs= nnet.num_outputs()
numInputs = nnet.num_inputs()
random.seed()
#print("Time taken :: %.14f" %(start_time))
runSample(numInputs,numOutputs,mat1,targetAndType,start_time,pNum)
#if ( ret == 0):
#    timeTaken = (time.clock() - start_time)
#    print("Time taken :: %.4f" %(timeTaken))
#    return 1
timeTaken = (time.clock() - start_time)
print("Time taken :: %.14f" %(timeTaken))




