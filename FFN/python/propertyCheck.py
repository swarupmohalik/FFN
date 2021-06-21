import numpy as np
import re
import subprocess
def findObjectiveFuncionType(prop):
    print("Mou",prop)
    if (prop == "1" or prop == "2" or prop == "6" or prop == "8" or prop == "10"):
        target= 0
        objType = 0 # 0 for maximize
    if (prop == "3" or prop == "4"):
        target= 0
        objType = 1 # 1 for minimize
    if (prop == "5") :
        target= 4
        objType = 0 # 1 for minimize
    if (prop == "7" or prop == "9"):
        target= 3
        objType = 1 # 1 for minimize
    if (prop == "9"):
        target= 3
        objType = 0 # 1 for maximize
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

def loadInputRange(prop):          
    inRange=[]   
    lower=[]      
    upper=[]       
    if (prop == "1") :        
        lower=[55947.691,-3.141592,-3.141592,1145,0]     
        upper=[60760,3.141592,3.141592, 1200, 60]      
    if (prop == "2") :       
        lower=[55947.691,-3.141592,-3.141592,1145,0]    
        upper=[60760,3.141592,3.141592, 1200, 60]    
    if (prop == "3") :  
        lower=[1500,-0.06,3.10,980,960]     
        upper=[1800,0.06,3.141592,1200,1200]        
    if (prop == "4") :  
        lower=[1500,-0.06,0,1000,700]         
        upper=[1800,0.06,0,1200,800]    
    if (prop == "5") : 
        lower=[250,0.2,-3.1415926,100,0]     
        upper=[400,0.4,-3.1415926+0.005,400,400]       
    if (prop == "6") : 
        lower=[12000,-3.141592,-3.141592,100,0]   
        upper=[62000,-0.7,-3.141592+0.005,200,1200]        
    if (prop == "7") :  
        lower=[0,-3.141592,-3.141592,100,0]    
        upper=[60760,3.141592,3.141592,1200,1200]      
    if (prop == "8") :  
        lower=[0,-3.141592,-0.1,600,600]     
        upper=[60760,-3.141592*0.75,0.1,1200,1200]     
    if (prop == "9") :    
        lower=[2000,-0.4,-3.141592,100,0]    
        upper=[7000,-0.14,-3.141592+0.01,150,150]        
    if (prop == "10") :     
        lower=[36000,0.7,-3.141592,900,600]       
        upper=[60760,3.141592,-3.141592+0.01,1200,1200]       
    inRange.append(lower)  
    inRange.append(upper)   
    tMat=np.transpose(inRange)     
    return tMat      

