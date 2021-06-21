rm Report_all
ls ../benchmarks/acasxu/*.onnx>netList
ls ../benchmarks/acasxu/*.vnnlib>vnnFile
cat vnnFile | while read vnn
do
   echo $vnn
   cat netList| while read net
   do
      echo $net
      ./run_instance.sh 1.1 acas $net $vnn Result 60 
   done
done
   
rm netList vnnFile 
  
