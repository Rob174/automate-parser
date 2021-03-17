#!/bin/bash

echo "Specify a name for your grammar:";
read grammar;
echo "${grammar} is your grammar, now specify a name for your parser";
read parser;
python main.py ${grammar} -o ${parser};
nom_fichier="${parser}.c";
echo "${nom_fichier}"
gcc -Wall -o ${parser}   ${nom_fichier};
