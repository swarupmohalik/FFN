import numpy as np
import math
import time
import random
import re
import numpy
import onnx
import onnxruntime as rt
from random import randint
import sys
sys.path.append('..')

from vnnlib import read_vnnlib_simple, get_io_nodes
from util import predict_with_onnxruntime, remove_unused_initializers
from util import  findObjectiveFuncionType, checkAndSegregateSamplesForMaximum, checkAndSegregateSamplesForMinimum

numRuns=50
numSamples=100

def sampling(onnxModel,inVals,inp_dtype, inp_shape):
   flatten_order='C'
   inputs = np.array(inVals, dtype=inp_dtype)
   inputs = inputs.reshape(inp_shape, order=flatten_order) # check if reshape order is correct
   assert inputs.shape == inp_shape

   output = predict_with_onnxruntime(onnxModel, inputs)
   flat_out = output.flatten(flatten_order) # check order
   return flat_out

def propCheck(inputs,specs,outputs):
   res="unknown"
   for prop_mat, prop_rhs in specs:
       vec = prop_mat.dot(outputs)
       sat = np.all(vec <= prop_rhs)

       if sat:
          res = 'violated'
          break

   if res == 'violated':
      print("Adversarial inputs found !!!")
      print("Adversarial inputs are :  ", inputs)
      print("STATUS:: ",res) 
      return 1

   return 0
    

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

def makeSample(onnxModel,numInputs,inRanges,samples,specs,start_time,inp_dtype, inp_shape):
    sampleInputList=[]
    #numSamples=numInputs*30   # 30 times of number of inputs
    #numSamples=150   # fixed for all benchmarks
    for k in range(numSamples):
        j=0
        while( j < 5):
            inValues=[]
            for i in range(numInputs):
                inValues.append(round(random.uniform(inRanges[i][0],inRanges[i][1]),6))
            if ( inValues in sampleInputList):
                #print("Duplicate",j,inValues,sampleInputList)
                j=j+1
            else :
                break
        sampleInputList.append(inValues)
        sampleVal=sampling(onnxModel,inValues,inp_dtype, inp_shape)
        retVal=propCheck(inValues,specs,sampleVal)
        if retVal == 1: #Adversarial found
            return 1
        s=[]
        s.append(inValues)
        s.append(sampleVal)
        samples.append(s)
    return 0

def runSample(onnxModel,numInputs,numOutputs,inputRange,tAndOT,spec, start_time,inp_dtype, inp_shape):
    k=0
    oldPosSamples=[]
    target = tAndOT[0]
    objectiveType = tAndOT[1]
    while (k != numRuns):
        samples=[]
        posSamples=[]
        negSamples=[]
        ret = makeSample(onnxModel,numInputs,inputRange,samples,spec,start_time,inp_dtype,inp_shape)
        if ( ret == 1): #Adversarial found
           return 

        if ( objectiveType == 1) :
           checkAndSegregateSamplesForMinimum(posSamples,negSamples,samples,oldPosSamples,target)
        else:
           checkAndSegregateSamplesForMaximum(posSamples,negSamples,samples,oldPosSamples,target)
        oldPosSamples=posSamples
        flag=False
        for i in range(numInputs):
            if ( inputRange[i][1] - inputRange[i][0] > 0.000001):
               flag=True
               break
        if( flag == False):
           print("!!! No further sampling Possible for this iteration!!!")
           print("Inputs are now :: ", inputRange)
           print("STATUS :: unknown")
           #timeTaken = (time.process_time() - start_time)
           #print("Time taken :: %.4f" %(timeTaken))
           exit()
        learning(posSamples,negSamples,inputRange,numInputs)
        k=k+1
    return 


#Main function
start_time = time.process_time()
onnx_filename = sys.argv[1]
vnnlib_filename = sys.argv[2]

#onnx model load
onnxModel = onnx.load(onnx_filename)
onnx.checker.check_model(onnxModel, full_check=True)
onnxModel = remove_unused_initializers(onnxModel)
inp, out, inp_dtype = get_io_nodes(onnxModel)
inp_shape = tuple(d.dim_value if d.dim_value != 0 else 1 for d in inp.type.tensor_type.shape.dim)
out_shape = tuple(d.dim_value if d.dim_value != 0 else 1 for d in out.type.tensor_type.shape.dim)
numInputs = 1
numOutputs = 1

for n in inp_shape:
    numInputs *= n

for n in out_shape:
    numOutputs *= n

print(f"Testing onnx model with {numInputs} inputs and {numOutputs} outputs")

#parse vnnlib file 

box_spec_list = read_vnnlib_simple(vnnlib_filename, numInputs, numOutputs)

inp_shape = tuple(d.dim_value if d.dim_value != 0 else 1 for d in inp.type.tensor_type.shape.dim)
status = 'unknown'

targetAndType = findObjectiveFuncionType(box_spec_list[0][1],numOutputs)

for i in range (len(box_spec_list)):
    box_spec = box_spec_list[i]
    inRanges = box_spec[0]
    specList = box_spec[1]
    random.seed()
    runSample(onnxModel,numInputs,numOutputs,inRanges,targetAndType,specList, start_time,inp_dtype, inp_shape)
#timeTaken = (time.process_time() - start_time)
#print("Time taken :: %.6f" %(timeTaken))




