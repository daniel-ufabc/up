#!/bin/bash

cd ~/Downloads
./send.py
mkdir -p /tmp/prochazka
mv *.ipynb /tmp/prochazka
rm -rf prova.bash send.py terminei.bash
