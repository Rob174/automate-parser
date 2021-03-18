#!/bin/bash

echo "Specify the path for your grammar:";
read grammar;
echo "${grammar} is your grammar file path, now specify a path for your parser";
read parser;
python3 main.py ${grammar} -o ${parser};
nom_fichier="${parser}.c";
echo "${nom_fichier}"
gcc -Wall -o ${parser}   ${nom_fichier};
