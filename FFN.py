import sys
import time
import signal


from src.FFNEvaluation import sampleEval

printStatus= "\nStatus : "
printTimeout= "\n\nTime taken : "

# Register an handler for the timeout
def handler(signum, frame):
    raise Exception("")#kill running :: Timeout occurs")

def runSingleInstance(onnxFile,vnnlibFile):
   #Variable Initialization
   startTime = time.time()
  
   onnxFileName = onnxFile.split('/')[-1]
   vnnFileName = vnnlibFile.split('/')[-1]

   print(f"\nTesting network model {onnxFileName} for property file {vnnFileName}")

   'Calling sampleEval until any adversarial found or timout ocuurs'
   while(1):
       status = sampleEval(onnxFile,vnnlibFile)
       endTime = time.time()
       timeElapsed = endTime - startTime
       #print("Time elapsed: ",timeElapsed)

       if (status == "violated"):
          resultStr = printStatus +status+printTimeout+str(round(timeElapsed,4))+" second"
          return resultStr
    
   resultStr = printStatus +"timeout"+printTimeout+str(round(timeElapsed,4)) + " second"
   return resultStr


#Main function
if __name__ == '__main__':

   onnxFile= sys.argv[1]
   vnnlibFile=sys.argv[2]
   timeout=sys.argv[3]
   # Register the signal function handler
   signal.signal(signal.SIGALRM, handler)

   # Define a timeout for "runSingleInstance"
   signal.alarm(int(timeout))
   
   '"runSingleInstance" will continue until any adversarial found or timeout occurs'
   'When timeout occurs codes written within exception will be executed'
   try:
       retStatus = runSingleInstance(onnxFile,vnnlibFile)
       print(retStatus)
   except Exception as exc:
       printStr = printStatus+"timeout"+printTimeout + str(timeout) + " second\n" 
       print(printStr)
       print(exc)

