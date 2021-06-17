FNN : Fast Falsification of Neural Networks using Property Directed Testing
----------------------------------------------------------------------------

Getting Started
-------------------------

The Dockerfile shows how to install all the dependencies (mostly python and numpy packages) and set up the environment. 

To build an image
-----------------
sudo docker build . -t ffn_image 

To get a shell after building the image:
-------------------------------------------
sudo docker run -i -t ffn_image bash

How to evaluate
---------------

cd Script

To convert network model written in .onnx file format to .nnet file format 
--------------------------------------------------------------------------
python convert_acas_onnx2nnet.py 

To run a single instance
------------------------------
python ../python/sampling_evaluate.py 7 ../nnet/ACASXU_run2a_1_7_batch_2000.nnet 
 ---It evaluates Property 7 for network ACASXU_run2a_1_7_batch_2000.nnet


To run a all instances
------------------------------
python runScript_all.py


To check output
----------------------
cat Report_all.txt


Directory Structure
----------------------
  ---nnet
  ---converter
  ---python
  ---Script

nnet : Contains .nnet files for Acas Xu benchmark. 
       Description for .nnet format is available in ReadMe_nnet

converter : pthon source code to convert network model written in .onnx file format to .nnet file format


python : Contains python source codes for FNN

Script : 
        A. Contains script to convert network model written in .onnx file format to .nnet file format
           Usage : python convert_acas_onnx2nnet.py

        B.  Contains 3 different scripts to run FNN

         1. For a single run option is  - 
                 python ../python/sampling_evaluate.py 7 ../nnet/ACASXU_run2a_1_7_batch_2000.nnet 
            It evaluates Property 7 for network ACASXU_run2a_1_7_batch_2000.nnet


         2. For multiple runs (10 properties for all 45 networks) option is - 
                python ./runScript_all.py
            Generated result (Report_all) is kept in Result directory
 
         3. To generate results shown in the paper option is - 
                python runScriptToGeneratePaperResult.sh
            Generated result(Report_paper) is kept in Result directory



Note: Since FFN has randomization, results may vary accross the runs.
