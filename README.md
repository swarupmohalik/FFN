Getting Started
-------------------------

The Dockerfile shows how to install all the dependencies (mostly python and numpy packages) and set up the environment.

     sudo ./run_in_docker.sh


Internally it calls three scripts for evaluation
--------------------------------------------------
install_tool.sh: takes in single argument "v1", a version string. This script is executed once to, for example, download any dependencies for your tool, compile any files, or setup any required licenses (if it can be automated). Note that some licences cannot be automatically retrived, so that the tool authors will be be responsible for a manual step prior to running any scripts to get the licenses.

prepare_instance.sh: four arguments, first is "v1", second is a benchmark identifier string such as "acasxu", third is path to the .onnx file and fourth is path to .vnnlib file. This script prepares the benchmark for evaluation (for example converting the onnx file to pytorch or reading in the vnnlib file to generate c++ source code for the specific property and compiling the code using gcc. You can also use this script to ensure that the system is in a good state to measure the next benchmark (for example, there are no zombie processes from previous runs executing and the GPU is available for use). This script should not do any analysis. The benchmark name is provided, as per benchmark settings are permitted (per instance settings are not, so do NOT use the onnx filename or vnnlib filename to customize the verification tool settings). If you want to skip a benchmark category entirely, you can have prepare_instance.sh return a nonzero value (the category is passed in as a command=line argument).

run_instance.sh: six arguments, first is "v1", second is a benchmark identifier string such as "acasxu", third is path to the .onnx file, fourth is path to .vnnlib file, fifth is a path to the results file, and sixth is a timeout in seconds. Your script will be killed if it exceeds the timeone by too much, but sometimes gracefully quitting is better if you want to release resources cleanly like GPUs. The results file should be created after the script is run and is a simple text file containing one word on a single line: holds, violated, timeout, error, or unknown.

Differences from Main branch
--------------------------------
1. Run scripts are shell scripts, and written according to vnncomp 2021 instructions. 
2. All commandline arguments are mandatory
3. run_single_instance shows one word output only (no output for time taken to get this output)
4. No --option specified in commandline for optional arguments
