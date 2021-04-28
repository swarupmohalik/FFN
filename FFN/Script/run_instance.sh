mkdir ../nnets
echo "Version: " $1
echo "Benchmark:: " $2
echo "Network path:: " $3
echo "vnnlib file path:: " $4
echo "Result file path" $5
echo "Timeout :: " $6 "secs"
vnnlibFile=$4
network=$3
grep assert $vnnlibFile|head -10|cut -d " " -f4|cut -d ")" -f1>inputBounds
grep assert $vnnlibFile|tail +11 |cut -d "(" -f3 |cut -d ")" -f1>prop
propNum=`echo $vnnlibFile|cut -d "_" -f2|cut -d "." -f1`
/usr/bin/python3.6 ../python/genPropertyFromVnnlib.py prop
/usr/bin/python3.6 ../python/acas_onnx2nnet.py $3 >netFile
grep Error netFile
if [ $? == 0 ]
then
   echo error >$5
fi
   
read -r nnetFile < netFile
[ -f R1 ] && rm R1;
b=0.0
s1=0
iterFlag=1
timeoutFlag=0
timeout=0
while(true)
do
  /usr/bin/python3.6 ../python/sampling_evaluate.py $propNum $nnetFile inputBounds prop >A
  a=`grep "Time" A |cut -d " " -f4`
  b=`echo $a + $b | bc`
  grep "Number of samples ::" A >/dev/null
  if [ $? == 0 ]   
  then     
    s=`grep "Number of samples ::" A |cut -d " " -f6`
    s1=$(($s + $s1))
  else
    s=0
  fi
  grep "Adversarial !" A >/dev/null
  if [ $? == 0 ]   
  then     
    tm=$b
    echo ADVERSARIAL FOUND :: Time :: $tm :: NUMSAMPLE :: $s1>R
    echo ADVERSARIAL >>R1
    aaa=`grep "Adversarial !" A |cut -d "!" -f2`      
    echo $aaa
    break
  else
    tm=$b
    s1=$(($s1+1500))
  fi       
  tTime=10.0
  timeout=`echo "$tm > $tTime"|bc`
  if [ $timeout  == 1 ]
  then
    echo TimeOut 
    timeoutFlag=1
    tm=`echo $tm - $a | bc`
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
grep "ADVERSARIAL" R1 >/dev/null     
if [ $? == 0 ]   
then
   echo violated >$5
   echo violated :: adversarial inputs :: $aaa
   echo Time taken :: $nt
   echo Number of samples  :: $ns
else
   echo timeout >$5
   echo timeout
   echo Time taken :: $nt
   echo Number of samples  :: $ns
fi       
rm A R R1 propSpecification.py prop inputBounds netFile
rm -rf ../nnet

