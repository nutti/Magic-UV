#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: pep8.sh <target>"
    exit 1
fi

tgt=${1}

files=`find ${tgt} -name "*.py"`
ignores=("__init__.py" "utils/compatibility.py" "lib/bglx.py")

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
    which pycodestyle > /dev/null
    if [ $? -eq 0 ]; then
        pycodestyle ${file} --config pycodestyle
    else
        pep8 ${file}
    fi
    ret=`echo $?`
    if [ ${ret} -ne 0 ]; then
        exit 1
    fi
done
