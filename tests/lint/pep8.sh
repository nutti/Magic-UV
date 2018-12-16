#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: pep8.sh <target>"
    exit 1
fi

tgt=${1}

files=`find ${tgt} -name "*.py"`
ignores=("__init__.py" "addon_updater.py" "addon_updater_ops.py" "lib/bglx.py")

# pep8
for file in ${files[@]}; do
    # ignore file in ignores
    found=0
    for ign in ${ignores[@]}; do
        if [ `echo "${file}" | grep "${ign}"` ]; then
            found=1
        fi
    done
    if [ ${found} -eq 1 ]; then
        continue
    fi
    echo "======= pep8 test "${file}" ======="
    pep8 ${file}
    ret=`echo $?`
    if [ ${ret} -ne 0 ]; then
        exit 1
    fi
done
