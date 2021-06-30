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

Evaluation
---------------
1: To run a all categories
   ------------------------------
python run_all_categories.py category result_file_path

Example run:

python run_all_categories.py acasxu Report 

 ---It evaluates all networks(.onnx files in acaxu directory) for all the properies(all .vnnlib files in acasxu directory) from "acasxu" benchmark category 
 ---After evalauation result is stored in Report

1: To run a single instance
   ------------------------------
python run_single_instance.py onnx_file_path vnnlib_file_path result_file_path timeout_parameter

Example run:

python run_single_instance.py benchmarks/acasxu/ACASXU_run2a_1_1_batch_2000.onnx benchmarks/acasxu/prop_2.vnnlib result_file 10
 ---It evaluates "acas" benchmark Property 2 for network ACASXU_run2a_1_1_batch_2000.nnet
 ---After evalauation result is stored in result_file
 ---timeout parameter is set as 10 sec


Note: Since FFN has randomization, results may vary accross the runs.
