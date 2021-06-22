echo "Version: " $1
echo "benchmark:: " $2
echo "network path:: " $3
echo "vnnlib file path:: " $4
echo "result file path:: " $5
echo "timeout:: MMMM" $6

#export TOOL_PATH=$PWD
#echo "MOUMITA" $TOOL_PATH
#ls $TOOL_PATH/*
propFile=$4

propNum=`echo $propFile|cut -d "_" -f2|cut -d "." -f1`
echo $4| grep "prop_6.vnnlib" 
if [ $? == 0 ]   
then     
propFile="prop_6a.vnnlib"
fi

grep assert $propFile|grep -v "Y" | head -10|cut -d " " -f4|cut -d ")" -f1>inputRangeFile
lno=`grep -n "assert" $propFile|head -n 11|tail +11|cut -d : -f1`
cat $propFile|tail +$lno>propSpecFile
ls *
totTm=0.0
totSmpl=0
timeoutFlag=0
timeout=0
while(true)
do
  python3 vnncomp2021/FFN/python/sampleEval.py inputRangeFile $propNum propSpecFile  $3 >A
  tm=`grep "Time" A |cut -d " " -f4`
  totTm=`echo $tm + $totTm | bc`
  grep "Number of samples ::" A 1</dev/null
  if [ $? == 0 ]    
  then     
    smpl=`grep "Number of samples ::" A |cut -d " " -f6`
    totSmpl=$(($smpl + $totSmpl))
  else
    smpl=0
  fi
  grep "Adversarial !" A  1</dev/null      
  if [ $? == 0 ]   
  then     
    echo ADVERSARIAL FOUND :: Time :: $totTm :: NUMSAMPLE :: $totSmpl>R
    echo ADVERSARIAL >>R1
    break
  else
    totSmpl=$(($totSmpl+1500))
  fi       
  timeout=`echo "$totTm > $6"|bc`
  if [ $timeout  == 1 ]
  then
    if [ $propFile == "prop_6a.vnnlib" ]
    then
        propFile="prop_6b.vnnlib"
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
if [ $timeoutFlag  == 1 ]   
then
  echo TIMEOUT  FOUND :: Time :: $tm :: NUMSAMPLE :: $s1>R
  echo TIMEOUT >>R1
  ns=0
  nt=0.0
else
  nt=`grep "Time" R |cut -d " " -f6`
  ns=`grep "NUMSAMPLE" R |cut -d " " -f10`
fi
grep "ADVERSARIAL" R1 1</dev/null      
if [ $? == 0 ]   
then     
echo $4  ::  $3 ::  ADVERSARIAL FOUND ::  Time :: $nt :: NUMSAMPLE :: $ns >>Report_all
echo violated >$5
else
echo $4  ::  $3 ::  TIMEOUT >>Report_all
echo timeout >$5
fi       
rm -f A R R1 test.smt inputRangeFile propSpecFile

