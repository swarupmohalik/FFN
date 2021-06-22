TOOL_NAME=FFN
VERSION_STRING=v1

# check arguments
if [ "$1" != ${VERSION_STRING} ]; then
	echo "Expected first argument (version string) '$VERSION_STRING', got '$1'"
	exit 1
fi

echo "Installing $TOOL_NAME"
DIR=$(dirname $(dirname $(realpath $0)))


#apt update
#apt install software-properties-common
#add-apt-repository ppa:deadsnakes/ppa
#apt install python3.6
#apt install python3-pip
#apt-get install protobuf-compiler libprotoc-dev

pip3 install "onnx==1.8.0"
pip3 install numpy
pip3 install z3-solver
pip3 install onnxruntime
pip3 install torch
pip3 install future

