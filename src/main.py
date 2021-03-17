import os
import argparse
print(os.getcwd())
parser = argparse.ArgumentParser()
parser.add_argument('path_grammar', type=str,
                    help='Chemin vers le fichier de grammaire')
parser.add_argument('-o', dest='nom_fichier_output',
                    help="Spécifie le nom du fichier c de destination (sans l'extension)")

args = parser.parse_args()

with open(args.path_grammar, "r") as f:
    L = []

    dico_elements_parses = {}
    for i,l in enumerate(f.readlines()):
        l.replace(" ", "")
        [head, rule] = [e.strip() for e in l.strip().split(":")]
        if head not in dico_elements_parses.keys():
            dico_elements_parses[head] = ["parse%s%d" % (head,i)]
        else:
            dico_elements_parses[head].append("parse%s%d" % (head,i))

        L.insert(0, "int parse%s%d(char * input);" % (head,i))
        L.append("int parse%s%d(char * input) {" % (head,i))
        L.append("\tint ok;")

        for i,lettre in enumerate(rule):
            if lettre.lower() != lettre:
                """passage à revoir : comment séparer les parties à tester avec les variables"""
                L.append(f"\tok = parse{lettre}(input[{i*2}]);") # A revoir comment on extrait la partie intéressante ; comment on découpe ;
                """split dans une boucle en déplacant le moment où on coupe entre la variable courante et la suivante
                Si un terminal après s'arrêter au terminal"""
                L.append("\tif (ok == 0) return 0;")
            else:
                L.append(f"\tif (input[{i*2}] != '{lettre}') return 0;")
        L.append("\treturn 1;")
        L.append("}\n")
    for head,liste_fct in dico_elements_parses.items():
        L.insert(0, "int parse%s(char * input);" % head)
        L.append("int parse%s(char *input) {" % head)
        L.append("\tint ok = 0,i = 0;")
        L.append(f"\tint (*fun_ptrs[{len(liste_fct)}])(char*) = " + "{"+",".join(liste_fct)+"};")
        L.append("\twhile(i<%d && ok == 0)" % len(liste_fct))
        L.append("\t\tok = fun_ptrs[i](input);")
        L.append("\treturn ok;")
        L.append("}")

    """ Including libraries """
    L.insert(0, "#include <stdio.h>")
    L.insert(0, "#include <stdlib.h>")
    
    """ Adding the main() """
    L.append("int main(int argc, char** argv) {") # main definition with args
    # Check if there is the right number of parameters (2: program name and the word to parse)
    L.append("\tif(argc != 2) {")
    L.append("\t\tprintf(\"Command type: %s \"word_to_parse\"\", argv[0]);")
    L.append("\t\texit(1);")
    L.append("\t}")

    L.append("\tchar * wordToParse = agrv[1];")
    L.append("\tparse" + list(dico_elements_parses.keys())[0] + "0(wordToParse);")

    L.append("\treturn 0;")
    L.append("}")
with open(args.nom_fichier_output+".c", "w") as f:
    f.write("\n".join(L))
print("\n".join(L))
