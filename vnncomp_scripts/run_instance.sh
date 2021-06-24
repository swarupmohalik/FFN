

echo "Version: " $1
echo "benchmark:: " $2
echo "network path:: " $3
echo "vnnlib file path:: " $4
echo "result file path:: " $5
echo "timeout:: " $6


propFile=$4

propNum=`echo $propFile|cut -d "_" -f2|cut -d "." -f1`
echo $4| grep "prop_6.vnnlib" 
if [ $? -eq 0 ]   
then     
propFile="FFN/FFN/prop_6a.vnnlib"
fi

grep assert $propFile|grep -v "Y" |grep "X"|cut -d " " -f4|cut -d ")" -f1>inputRangeFile
numInput=`cat inputRangeFile|wc -l`
numInput=$(($numInput+1))
lno=`grep -n "assert" $propFile|head -$numInput|tail +$numInput|cut -d : -f1`
cat $propFile|tail +$lno>propSpecFile


totTm=0.0
totSmpl=0
timeoutFlag=0
timeout=0
while(true)
do
  python3 FFN/FFN/python/sampleEval.py inputRangeFile $propNum propSpecFile  $3 2</dev/null>A
  if [ $? -ne 0 ]
  then
     echo error >$5
     exit 0
  fi

  tm=`grep "Time" A |cut -d " " -f4`
  totTm=`echo $tm + $totTm | bc`
  grep "Number of samples ::" A 1</dev/null
  if [ $? -eq 0 ]    
  then     
    smpl=`grep "Number of samples ::" A |cut -d " " -f6`
    totSmpl=$(($smpl + $totSmpl))
  else
    smpl=0
  fi
  grep "Adversarial !" A  1</dev/null      
  if [ $? -eq 0 ]   
  then     
    echo ADVERSARIAL FOUND :: Time :: $totTm :: NUMSAMPLE :: $totSmpl>R
    echo ADVERSARIAL >>R1
    break
  else
    totSmpl=$(($totSmpl+1500))
  fi       
  timeout=`echo "$totTm > $6"|bc`
  if [ $timeout -eq 1 ]
  then
    S=`echo $propFile|grep "prop_6a"`
    if [ $? -eq 0 ]
    then
        propFile="FFN/FFN/prop_6b.vnnlib"
	totTm=0.0
	totSmpl=0
	timeoutFlag=0
	timeout=0
        continue
    fi   
    timeoutFlag=1
    totTm=`echo $totTm - $tm | bc`
    break
  fi
done    
if [ $timeoutFlag  -eq 1 ]   
then
  echo TIMEOUT >>R1
fi
grep "ADVERSARIAL" R1 1</dev/null      
if [ $? -eq 0 ]   
then     
    echo violated >$5
else
    echo timeout >$5
fi       
rm -f A R R1 test.smt inputRangeFile propSpecFile

