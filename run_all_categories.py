import sys
import subprocess

CATEGORY=sys.argv[1]
ReportFile=sys.argv[2]
TIMEOUT=60
ONNX_FILE_PATH="ls benchmarks/"+CATEGORY+"/*.onnx>modelList"
result=subprocess.check_output(ONNX_FILE_PATH  , shell=True)
VNNLIB_FILE_PATH="ls benchmarks/"+CATEGORY+"/*.vnnlib>vnnliblist"
result=subprocess.check_output(VNNLIB_FILE_PATH  , shell=True)

modelFile = open("modelList","r")
models = modelFile.readlines()

propFile = open("vnnliblist","r")
props = propFile.readlines()

outFile = open(ReportFile,"w")
for prop in props :
   for model in models:
      prog="python run_single_instance.py" +" "+ model.strip() + "  "+ prop.strip() + " Res " + str(TIMEOUT)
      result = subprocess.run(prog, shell=True)
      temp_outFile = open("Res","r")
      line = temp_outFile.readlines()
      temp_outFile.close()
      print(line)
      outFile.write(line[0]+"\n")
outFile.close()
modelFile.close()
propFile.close()
