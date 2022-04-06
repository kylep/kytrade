#!/bin/bash

# Generate the setup.py and PKG-INFO files

# I need setup.py to be able to `pip install` with `-e` and `-U`,
# which Poetry does not support

if [ ! -d bin/ ]; then
  echo "ERROR: Run this from the base dir"
  exit 1
fi

rm -rf dist/
poetry build
cd dist
archive="$(ls | grep .tar.gz)"
tar -xzvf $archive
directory="$(ls -d */)"
cp $directory/setup.py ../
cp $directory/PKG-INFO ../
