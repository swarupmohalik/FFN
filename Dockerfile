# Dockerfile for vnncomp 2021
# this is an example that uses the tool_example scripts

FROM ubuntu:20.04

RUN echo "Starting..."
RUN apt-get update && apt-get install -y bc git # bc is used in vnncomp measurement scripts

################## install tool


ARG TOOL_NAME=vnnComp_2021
ARG REPO=https://github.com/DMoumita/vnnComp_2021.git 
ARG COMMIT=48850a9b7e4c68e1dd59c179d4f5fe6501e37cb0
ARG SCRIPTS_DIR=vnncomp_scripts

RUN git clone $REPO
RUN cd $TOOL_NAME && git checkout $COMMIT && cd ..
RUN /$TOOL_NAME/$SCRIPTS_DIR/install_tool.sh v1

#################### run vnncomp

