import sys
import time
import signal
import argparse

from src.FFNEvaluation import sampleEval

# Register an handler for the timeout
def handler(signum, frame):
    raise Exception("kill running :: Timeout occurs")

def runSingleInstanceForAllCategory(onnxFile,vnnlibFile,resultFile,timeout):
   'called from run_all_catergory.py'
   # Register the signal function handler
   signal.signal(signal.SIGALRM, handler)

   # Define a timeout for "runSingleInstance"
   signal.alarm(int(timeout))

   try:
       retStatus = runSingleInstance(onnxFile,vnnlibFile,resultFile,timeout)
       return retStatus
   except Exception as exc:
       printStr = "timeout," + str(timeout) + "\n" 
       print(exc)

def runSingleInstance(onnxFile,vnnlibFile,resultFile,timeout):
   #Variable Initialization
   startTime = time.time()

   while(1):
       status = sampleEval(onnxFile,vnnlibFile)
       endTime = time.time()
       timeElapsed = endTime - startTime
       print("Time elapsed: ",timeElapsed)

       if (status == "violated"):
          resultStr = status+", "+str(round(timeElapsed,4))
          return resultStr
    
   resultStr = "timeout,"+str(round(timeElapsed,4)) + "\n"
   return resultStr


#Main function
if __name__ == '__main__':

   #Commandline arguments processing

   # Instantiate the parser
   parser = argparse.ArgumentParser(description='Optional app description')

   # Required onnx file path 
   parser.add_argument('onnxfile',
                    help='A required onnx model file path')

   # Required vnnlib file path
   parser.add_argument('vnnlibfile', 
                    help='A required vnnlib file path')

   # Optional resultfile path
   parser.add_argument('--resultfile',
                    help='An optional result file path')

   # optional timeout parameter
   parser.add_argument('--timeout',
                    help='An optional timeout')

   args = parser.parse_args()
   try:
      onnxFile = args.onnxfile
      vnnlibFile = args.vnnlibfile
   except:
      print ("\n!!! Failed to provide onnx file and vnnlib file path on the command line!")
      sys.exit(1)  # Exit from program


   resultFile = args.resultfile 

   #Set default for resultFile
   if ( resultFile is None ):
      print ("\n!!! No result_file path is provided on the command line!")
      print ("Default result_file is - out.txt")
      resultFile = "out.txt"

   timeout = args.timeout

   #Set default for timeout
   if ( timeout is None ):
      print ("\n!!! timeout is not on the command line!")
      print ("Default timeout is set as - 60 sec")
      timeout = 60.0


   # Register the signal function handler
   signal.signal(signal.SIGALRM, handler)

   print(timeout)
   # Define a timeout for "runSingleInstance"
   signal.alarm(int(timeout))

   try:
       retStatus = runSingleInstance(onnxFile,vnnlibFile,resultFile,timeout)
       outFile = open(resultFile, "w")
       print("\nOutput is written in - \"{0}\"".format(resultFile))
       outFile.write(retStatus)
       outFile.close()
   except Exception as exc:
       print("\nOutput is written in - \"{0}\"".format(resultFile))
       outFile = open(resultFile, "w")
       printStr = "timeout," + str(timeout) + "\n" 
       outFile.write(printStr)
       outFile.close()
       print(exc)

