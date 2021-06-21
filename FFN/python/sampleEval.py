import csv
import numpy as np
import math
import time
import random
import re
import numpy
import  propertyCheck as propCheck
import onnx
from onnx import numpy_helper
import onnxruntime as rt
import caffe2.python.onnx.backend as backend
from random import randint
import sys
sys.path.append('..')

numRuns=50
numSamples=100

def sampling(onnxModel,inVals,numOutputs):
   nnet_handle = backend.prepare(onnxModel, device="CPU")
   Input = np.array(inVals).astype(np.float32)
   oVals = nnet_handle.run(Input)
   output = oVals[0][-1]
   return output
    

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

def makeSample(onnxModel,numInputs,numOutputs,mat1,samples,start_time,pNum,num,propSpec):
    sampleInputList=[]
    #numSamples=numInputs*30   # 30 times of number of inputs
    #numSamples=150   # fixed for all benchmarks
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
        sampleVal=sampling(onnxModel,inValues,numOutputs)
        retVal=  propCheck.checkProperty(pNum,sampleVal,propSpec) 
        if retVal  == 1:
            return 0
        s=[]
        s.append(inValues)
        s.append(sampleVal)
        samples.append(s)
    return 1

def runSample(onnxModel,numInputs,numOutputs,mat1,tAndOT,start_time,propSpec, propNum):
    k=0
    oldPosSamples=[]
    target = tAndOT[0]
    objectiveType = tAndOT[1]
    while (k != numRuns):
        samples=[]
        posSamples=[]
        negSamples=[]
        ret = makeSample(onnxModel,numInputs,numOutputs,mat1,samples,start_time,propNum,k,propSpec)
        if ( ret == 0):
           return 

        if ( objectiveType == 1) :
           propCheck.checkAndSegregateSamplesForMinimum(posSamples,negSamples,samples,oldPosSamples,target)
        else:
           propCheck.checkAndSegregateSamplesForMaximum(posSamples,negSamples,samples,oldPosSamples,target)
        oldPosSamples=posSamples
        flag=False
        for i in range(numInputs):
            if ( mat1[i][1] - mat1[i][0] > 0.000001):
               flag=True
               break
        if( flag == False):
           print("\n\n !!! No further sampling Possible for this iteration!!!")
           timeTaken = (time.process_time() - start_time)
           print("Time taken :: %.4f" %(timeTaken))
           exit()
        learning(posSamples,negSamples,mat1,numInputs)
        k=k+1
    return 

#Main function

start_time = time.process_time()
inFile=sys.argv[1]
print(inFile)
propNum = sys.argv[2]
str2 = [line.strip() for line in open(inFile).readlines()]
mat1=numpy.array(str2,float)
mat1=mat1.reshape(int(len(str2)/2),2)
propSpec=[line.strip() for line in open(sys.argv[3]).readlines()]
targetAndType = propCheck.findObjectiveFuncionType(propNum)

#loading onnx model
onnxModel = onnx.load(sys.argv[4])
graph = onnxModel.graph

sess = rt.InferenceSession(sys.argv[4])
input_shape = sess.get_inputs()[0].shape
output_shape = sess.get_outputs()[0].shape

numInputs= input_shape[-1]
numOutputs = output_shape[-1]

# Check the model
try:
    onnx.checker.check_model(onnxModel)
except onnx.checker.ValidationError as e:
    print('The model is invalid: %s' % e)
else:
    print('The model is valid!')

print("Num Inputs: %d"%numInputs)
print("Num Outputs: %d"%numOutputs)


random.seed()
runSample(onnxModel,numInputs,numOutputs,mat1,targetAndType,start_time,propSpec, propNum)
timeTaken = (time.process_time() - start_time)
print("Time taken :: %.6f" %(timeTaken))




