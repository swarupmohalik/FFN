import subprocess
import codecs
import sys
import time

from src.FFNEvaluation import sampleEval
pythonProg="src/sampleEval.py"

#Commandline arguments processing
try:
    onnxFile = sys.argv[1]
    vnnlibFile = sys.argv[2]
except:
    print ("\n!!! Failed to provide onnx file and vnnlib file path on the command line!")
    sys.exit(1)  # Exit from program

try:
    resultFile = sys.argv[3]
except:
    print ("\n!!! No result_file path is provided on the command line!")
    print ("Default result_file is - out.txt")
    resultFile = "out.txt"

try:
    timeout = float(sys.argv[4])
except:
    print ("\n!!! timeout is not on the command line!")
    print ("Default timeout is set as - 60 sec")
    timeout = 60.0

#Variable Initialization
timeElapsed = float(0.0)
startTime = time.time()

outFile = open(resultFile, "w")

while(timeElapsed < timeout) :
    status = sampleEval(onnxFile,vnnlibFile)

    endTime = time.time()
    timeElapsed = endTime - startTime

    if (status == "violated"):
       resultStr = status+", "+str(round(timeElapsed,4))
       print("\nOutput is written in - \"",resultFile,"\"")
       outFile.write(resultStr)
       outFile.close()
       exit()
    
print("\nOutput is written in - \"",resultFile,"\"")
resultStr ="timeout , "+str(round(timeElapsed,4))
outFile.write(resultStr)
outFile.close()
