import os
import re
import sys

f = open(sys.argv[1],"r")
i=0
for x in f:
  a=x.strip().split()
  str1=a[1]+" "+a[0]+" "+a[2]
  if(i ==0):
    str2=str1
    i=i+1
  else :
    str2=str2+ " and " + str1

  str2=str2.replace("_0","[0]")
  str2=str2.replace("_1","[1]")
  str2=str2.replace("_2","[2]")
  str2=str2.replace("_3","[3]")
  str2=str2.replace("_4","[4]")
  str2=str2.replace("_5","[5]")
  str2=str2.replace("_6","[6]")
  str2=str2.replace("_7","[7]")
  str2=str2.replace("_8","[8]")
  str2=str2.replace("_9","[9]")
  str2=str2.replace("_10","[10]")
f.close()

ofilename="propSpecification.py"
with open(ofilename,'w') as f1:
  f1.write("def checkPropSpec(Y):\n")
  f1.write("    if ( "+str2+"):\n")
  str3="print("+"\""+"Adversarial !"+"\","+"Y[0],Y[1],Y[2],Y[3],Y[4])"
  f1.write("        "+str3+"\n")
  f1.write("        return 1\n")
f1.close()


