#!/bin/bash

./clean.sh

ulimit -c unlimited

./compile.sh
./Main
