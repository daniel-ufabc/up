#!/bin/bash
cd ~/
DIR="$PWD"
BDIR="$DIR/.bcc"
CDIR="$DIR/.config/autostart"
mkdir -p "$BDIR"
cd "$BDIR"
wget http://177.104.60.13/up/old/prochazka/P3.ipynb
mkdir -p "$CDIR"
cd "$CDIR"
wget http://177.104.60.13/up/old/provabcc.desktop
cd "$DIR/Downloads"
rm -f *.ipynb
ln -sf "$BDIR/P3.ipynb" .
wget http://177.104.60.13/up/old/velocidades.csv
wget http://177.104.60.13/up/old/pratos.csv
exec jupyter notebook P3.ipynb 2> /dev/null &






