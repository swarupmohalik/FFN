import os
import re
def generateInputBounds(bName):
    f = open(bName,"r")
    i=0
    inBound=[]
    for x in f:
        if (i == 0) :
            a=[]
            i=i+1
            a.append(float(x.strip()))
        else:
            i=0
            a.append(float(x.strip()))
            inBound.append(a)
    f.close()
    return inBound


