import numpy as np
def findObjectiveFuncionType(propName):
    #File propName contains negation of the actual property
    f = open(propName,"r")
    x=f.readline()
    p=x.strip().split()
    if ( p[1] == "Y_0"):
       target=0
    if ( p[1] == "Y_1"):
       target=1
    if ( p[1] == "Y_2"):
       target=2
    if ( p[1] == "Y_3"):
       target=3
    if ( p[1] == "Y_4"):
       target=4
    output=[]
    output.append(target)
    if ( p[1] == "<" or  p[1] == "<="):
       objType = 1 # 1 for mininimize
    else:
       objType = 0 # 0 for maximize
    output.append(objType)
    return output



def checkAndSegregateSamplesForMaximum(posSample,negSample, smple,oldPos,targetNode):      
    a=smple[0][1]
    large = a[targetNode]
    last_index=0
    posSample.append(smple[0])
    for i in range(1,len(smple)):
        a=smple[i][1]
        newLarge = a[targetNode]
        if newLarge > large :
            posSample.remove(smple[last_index])
            posSample.append(smple[i])
            negSample.append(smple[last_index])
            last_index=i
            large=newLarge
        else:
            if newLarge < large :
               negSample.append(smple[i])
    if (len(oldPos) > 0) :
        cPos=posSample[0][1]
        oldPos1=oldPos[0][1]
        if ( oldPos1[targetNode] > cPos[targetNode] ) :
            negSample.append(posSample[0])
            posSample.remove(posSample[0])
            posSample.append(oldPos[0])

def checkAndSegregateSamplesForMinimum(posSample,negSample, smple,oldPos,targetNode):      
    a=smple[0][1]
    small = a[targetNode]
    last_index=0
    posSample.append(smple[0])
    for i in range(1,len(smple)):
        a=smple[i][1]
        newSmall = a[targetNode]
        if newSmall < small :
            posSample.remove(smple[last_index])
            posSample.append(smple[i])
            negSample.append(smple[last_index])
            last_index=i
            small=newSmall
        else:
            if newSmall < small :
               negSample.append(smple[i])
    if (len(oldPos) > 0) :
        cPos=posSample[0][1]
        oldPos1=oldPos[0][1]
        if ( oldPos1[targetNode] < cPos[targetNode] ) :
            negSample.append(posSample[0])
            posSample.remove(posSample[0])
            posSample.append(oldPos[0])

