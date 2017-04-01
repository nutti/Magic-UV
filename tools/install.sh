#!/bin/sh

if [ $# -ne 2 ]; then
    echo "Usage: pylint_sample.sh <os> <version>"
fi

os=${1}
version=${2}
target=""

if [ ${os} = "mac" ]; then
    target=${HOME}/Library/Application\ Support/Blender/${version}/scripts/addons/uv_magic_uv
elif [ ${os} = "linux" ]; then
    target=${HOME}/.config/blender/${version}/scripts/addons/uv_magic_uv
else
    echo "Invalid operating system."
    exit 1
fi

if [ ! -d ${target} ]; then
    echo ${target}" not exist."
    exit 1
fi

rm -rf ${target}
cp -r uv_magic_uv ${target}
