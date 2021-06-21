#All dependencies are install via dockerfile
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.6.9
python3 -V

sudo apt install python3-pip

sudo apt-get install protobuf-compiler libprotoc-dev
pip3 install "onnx==1.8.0"
pip3 install numpy
pip3 install z3-solver
pip3 install onnx==1.8.0
pip3 install onnxruntime
pip3 install torch
pip3 install future

