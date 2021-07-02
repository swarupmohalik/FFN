import sys
import csv
import subprocess
from run_single_instance import runSingleInstance

#Commandline arguments processing
try:
    category = sys.argv[1]
except:
    category = "test"
    print ("\n!!! No benchmark category is provided on the command line!")
    print ("Default benchmark category is taken as - \"test\"")

try:
    reportFile = sys.argv[2]
except:
    reportFile =" report_"+category+".txt"
    print ("\n!!! No result_file is provided on the command line!")
    print (" Taking default result_file - ", reportFile)

#Reading cat_instance.csv for .onnx file path, .vnnlib file path and timeout

catInsCsvFile = "benchmarks/"+category+"/"+category+"_instances.csv"
insCsvFile = open(catInsCsvFile, 'r')
outFile = open(reportFile, 'w')
reader = csv.reader(insCsvFile)
for row in reader:
    onnxFile = "benchmarks/"+category+"/"+row[0]
    vnnlibFile = "benchmarks/"+category+"/"+row[1]
    timeout = row[2]
    resultStr = runSingleInstance(onnxFile,vnnlibFile,"out.txt",timeout)
    printStr=onnxFile+","+vnnlibFile+","+resultStr
    outFile.write(printStr)

insCsvFile.close()
outFile.close()

