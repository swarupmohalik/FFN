FNN : Fast Falsification of Neural Networks using Property Directed Testing
----------------------------------------------------------------------------

A. Folder structure
   -------------------

   1. ReadMe
   2. src  -- contains python source files
   3. benchmarks -- contains diferent benchmark categories
      Each category contains mainly - 
      a) .onnx files -- NN is given in .onnx file format
      b) .vnnlib files  -- provide normalized input ranges and property specification
      c) category_instance.csv files -- provide instances to be run for that category 
        Format of category_instance.csv is  -
        --------------------------------------
        .onnx file path,.vnnlib file path,timeout

   4. run_single_instance.py -- script to run a single instancei, how to run is given in "C"
   5. run_all_categories.py --to run all instances from a given category, how to run us given in "C" 
  
benchmarks folder
-----------------
   
B: Getting Started
   -------------------------

1. Run using Docker 
   --------------------------
    The Dockerfile shows how to install all the dependencies (mostly python and numpy packages) and set up the environment. 

    To build an image
    -----------------
    sudo docker build . -t ffn_image 

    To get a shell after building the image:
    -------------------------------------------
    sudo docker run -i -t ffn_image bash

2. Run without docker 
   ------------------------

   ---tested on Ubuntu 18.04 and 20.04
   
   a) Run in Ubuntu 20.04
   --------------------------
     sudo apt update
     sudo apt install python3
     sudo apt install python3-pip
     pip3 install onnx==1.8.0
     pip3 install onnxruntime==1.8.0
     pip3 install numpy==1.17.4

   b) Run in Ubuntu 18.04
   --------------------------
     sudo apt update
     sudo apt install python3.6
     sudo apt install python3-pip
     pip3 install onnx==1.8.0
     pip3 install onnxruntime==1.8.0
     pip3 install numpy==1.17.4

   
C. Evaluation
   ---------------
1: To run a single instance
   ------------------------------
python run_single_instance.py <onnx_file_path> <vnnlib_file_path> <result_file_path> <timeout_parameter>


Example run:

python run_single_instance.py benchmarks/acasxu/ACASXU_run2a_1_1_batch_2000.onnx benchmarks/acasxu/prop_2.vnnlib result_file 10

 ---It evaluates "acasxu" benchmark Property 2 for network ACASXU_run2a_1_1_batch_2000.nnet
 
 ---After evaluation, result is stored in result_file
 
 ---timeout parameter is set as 10 sec


2: To run all instances of a given benchmark category (from "benchmark" folder)
   ---------------------------------------------------------------------------
python run_all_categories.py  <category> <result_file_path>

Example run:

python run_all_categories.py acasxu Report 

 ---It evaluates all networks(.onnx files in acaxu directory) for all the properies(all .vnnlib files in acasxu directory) from "acasxu" benchmark category 
 
 ---After evalauation result is stored in Report

***Note: Since FFN has randomization, results may vary accross the runs.
