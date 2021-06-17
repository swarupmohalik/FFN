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

Three scripts for each tool -

1. `install_tool.sh`: takes in single argument "v1", a version string. This script is executed once to, for example, download any dependencies for your tool, compile any files, or setup any required licenses (if it can be automated). Note that some licences cannot be automatically retrived, so that the tool authors will be be responsible for a manual step prior to running any scripts to get the licenses.

2. `prepare_instance.sh`: four arguments, first is "v1", second is a benchmark identifier string such as "acasxu", third is path to the .onnx file and fourth is path to .vnnlib file. This script prepares the benchmark for evaluation (for example converting the onnx file to pytorch or reading in the vnnlib file to generate c++ source code for the specific property and compiling the code using gcc. You can also use this script to ensure that the system is in a good state to measure the next benchmark (for example, there are no zombie processes from previous runs executing and the GPU is available for use). This script should not do any analysis. The benchmark name is provided, as per benchmark settings are permitted (per instance settings are not, so do NOT use the onnx filename vnnlib filename to customize the verification tool settings).

3. `run_instance.sh`: six arguments, first is "v1", second is a benchmark identifier string such as "acasxu", third is path to the .onnx file, fourth is path to .vnnlib file, fifth is a path to the results file, and sixth is a timeout in seconds. Your script will be killed if it exceeds the timeone by too much, but sometimes gracefully quitting is better if you want to release resources cleanly like GPUs. The results file should be created after the script is run and is a simple text file containing one word on a single line: holds, violated, timeout, error, or unknown.


******Since docer image is provided no need to use install_tool.sh ******
******For FFN run no need to use prepare_instance.sh*********

To run a single instance
------------------------------
./run_instance v1 acas benchmark_path vnnlib_path result_file_path timeout_parameter

Example run:
./run_instance 1.1 acas ../../benchmarks/acasxu/ACASXU_run2a_1_1_batch_2000.onnx ../../benchmarks/acasxu/prop_2.vnnlib result_file 10
 ---It evaluates "acas" benchmark Property 2 for network ACASXU_run2a_1_1_batch_2000.nnet
 ---After evalauation result is stored in result_file
 ---timeout parameter is set as 10 sec


Note: Since FFN has randomization, results may vary accross the runs.
