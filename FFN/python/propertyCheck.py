import numpy as np
import re
import subprocess
def findObjectiveFuncionType(prop):
    
    if (prop == "1" or prop == "2" or prop == "6" or prop == "8" or prop == "10"):
        target= 0
        objType = 0 # 0 for maximize
    elif (prop == "3" or prop == "4"):
        target= 0
        objType = 1 # 1 for minimize
    elif (prop == "5") :
        target= 4
        objType = 0 # 1 for minimize
    elif (prop == "7" ):
        target= 3
        objType = 1 # 1 for minimize
    elif (prop == "9"):
        target= 3
        objType = 0 # 1 for maximize
    else:
        target= 0 #default
        objType = 0 # 1 for maximize default
        
    output=[]
    output.append(target)
    output.append(objType)
    return output

def checkProperty(prop,vals,pSpec):      
    pSp=" ".join(str(x) for x in pSpec)
    aa=[]
    for i in range(len(vals)):
        a="Y_"+str(i)
        val="{:.20f}".format(vals[i])
        pSp=pSp.replace(a, str(val))
        
    f = open("test.smt", "w")
    f.write(pSp)
    f.write("(check-sat-using smt)")
    f.close()
    result = subprocess.check_output("z3 test.smt > aa"  , shell=True)
    if 'unsat' in open('aa').read():
        return 0
    else :
        print("Adversarial !!!!!   ",vals)
        return 1




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



