FROM ubuntu:18.04

ENV MUV_CONSOLE_MODE true

WORKDIR /root

RUN env
RUN apt-get update -y -qq
RUN apt-get install -y \
            blender \
            wget \
            python3 \
            python3-pip \
            zip

RUN wget http://mirror.cs.umn.edu/blender.org/release/Blender2.77/blender-2.77-linux-glibc211-x86_64.tar.bz2
RUN tar jxf blender-2.77-linux-glibc211-x86_64.tar.bz2
