# Dockerfile for vnncomp 2021
# this is an example that uses the tool_example scripts

FROM ubuntu:20.04

RUN echo "Starting..."
RUN apt-get update && apt-get install -y bc git # bc is used in vnncomp measurement scripts

################## install tool


ARG TOOL_NAME=vnnComp_2021
ARG REPO=https://github.com/DMoumita/vnnComp_2021.git 
ARG COMMIT=053afb6efcdebd40964852e5cb544f2b74c0854d
ARG SCRIPTS_DIR=vnncomp_scripts

RUN git clone $REPO
RUN cd $TOOL_NAME && git checkout $COMMIT && cd ..
RUN /$TOOL_NAME/$SCRIPTS_DIR/install_tool.sh v1

#################### run vnncomp
COPY . /vnncomp2021

# run all categories to produce out.csv
ARG CATEGORIES="acasxu"
RUN vnncomp2021/run_all_categories.sh v1 /$TOOL_NAME/$SCRIPTS_DIR vnncomp2021 out.csv "$CATEGORIES"
