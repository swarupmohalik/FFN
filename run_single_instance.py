import subprocess
import codecs
import sys
import time

pythonProg="src/sampleEval.py"
ONNXFile=sys.argv[1]
vnnlibFile=sys.argv[2]
timeout=float(sys.argv[4])
totalTime=float(0.0)
START_TIME=time.time()
outFile = open(sys.argv[3], "w")
while(totalTime < timeout) :
    result = subprocess.run("python " +pythonProg+"  "+  ONNXFile + "  "+ vnnlibFile + ">A", shell=True)
    END_TIME=time.time()
    totalTime=END_TIME - START_TIME
    file1 = open("A", "r")
    readfile = file1.read()
    file1.close()
    print(ONNXFile,vnnlibFile)
    print("Time elapsed:",totalTime)
    file2 = open("A", "r")
    for line in file2:
        if "Target" in line: 
           print(line)
           break
    file2.close()
    if "violated" in readfile: 
       outs=ONNXFile+","+vnnlibFile+", violated, "+str(totalTime)
       outFile.write(outs)
       outFile.close()
       exit(0)
    if (totalTime >= timeout):
       outs=ONNXFile+","+vnnlibFile+", timeout, "+str(totalTime)
       outFile.write(outs)
       outFile.close()
       exit(0)
