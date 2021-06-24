# Dockerfile for vnncomp 2021
# this is an example that uses the tool_example scripts

FROM ubuntu:20.04

RUN echo "Starting..."
RUN apt-get update && apt-get install -y bc git # bc is used in vnncomp measurement scripts

################## install tool

ARG TOOL_NAME=FFN
ARG REPO=https://github.com/DMoumita/FFN.git
ARG COMMIT=6575598861d977fe7eecaafa0436458b7ae7b45c
ARG SCRIPTS_DIR=vnncomp_scripts

#ARG TOOL_NAME=nnenum
#ARG REPO=https://github.com/stanleybak/nnenum.git 
#ARG COMMIT=c93a39cb568f58a26015bd151acafab34d2d4929
#ARG SCRIPTS_DIR=vnncomp_scripts

RUN git clone $REPO
RUN cd $TOOL_NAME && git checkout $COMMIT && cd ..
RUN /$TOOL_NAME/$SCRIPTS_DIR/install_tool.sh v1

#################### run vnncomp
COPY . /vnncomp2021

# run all categories to produce out.csv
ARG CATEGORIES="acas"
RUN vnncomp2021/run_all_categories.sh v1 /$TOOL_NAME/$SCRIPTS_DIR vnncomp2021 out.csv "$CATEGORIES"
