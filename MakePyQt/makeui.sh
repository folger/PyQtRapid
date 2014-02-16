#! /bin/bash

# for f in $(ls); do
#   if [ "${f:${#f}-3:3}" == ".ui" ]; then
#     n=ui_${f:0:${#f}-3}.py

#     echo "Converting $f to $n"
#     pyuic4 $f -o $n
#   fi
# done

for f in $(find . -name "*.ui"); do
  filename=$(basename $f)
  name="${filename%.*}"
  n=$(dirname $f)/ui_$name.py
  echo "Converting $f to $n"
  pyuic4 $f -o $n
done

