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
    L = ["""
char* slice_str(char * input) {
    int length = strlen(input);
    if(length == 0) {
        return \"\";
    }
    char * new_str = malloc(sizeof(char)*(length-1));
    for (int i = 1; i < length; i++) {
        new_str[i-1] = input[i];
    }
    new_str[length-1] = '\\0';
    return new_str;
}
"""]

    dico_elements_parses = {}
    for i,l in enumerate(f.readlines()):
        l.replace(" ", "")
        [head, rule] = [e.strip() for e in l.strip().split(":")]
        if head not in dico_elements_parses.keys():
            dico_elements_parses[head] = ["parse%s%d" % (head,i)]
        else:
            dico_elements_parses[head].append("parse%s%d" % (head,i))

        L.insert(0,"char* parse%s%d(char * input);" % (head,i))
        L.append("char* parse%s%d(char * input) {" % (head,i))
        L.append("\tprintf(\"Passage dans parse%s%d %%s\\n\",input);" % (head,i))
        L.append("\tchar* okReste = input;")

        for i,lettre in enumerate(rule):
            if lettre.lower() != lettre:
                """passage à revoir : comment séparer les parties à tester avec les variables"""
                L.append(f"\tokReste = parse{lettre}(okReste);") # A revoir comment on extrait la partie intéressante ; comment on découpe ;
                """split dans une boucle en déplacant le moment où on coupe entre la variable courante et la suivante
                Si un terminal après s'arrêter au terminal"""
                L.append("\tif (okReste == NULL) return 0;")
            else:
                L.append(f"\tif (okReste[0] != '{lettre}')")
                L.append(f"\t\treturn 0;")
                L.append("\telse {")
                L.append(f"\t\t okReste = slice_str(okReste);")
                L.append("\t}")
        L.append("\treturn okReste;")
        L.append("}\n")
    for head,liste_fct in dico_elements_parses.items():
        L.insert(0,"char* parse%s(char *input);" % head)
        L.append("char* parse%s(char *input) {" % head)
        L.append("\tprintf(\"Passage dans parse%s %%s\\n\",input);" % head)
        L.append("\tchar* okReste = 0;int i = 0;")
        L.append(f"\tchar* (*fun_ptrs[{len(liste_fct)}])(char*) = " + "{"+",".join(liste_fct)+"};")
        L.append("\twhile(i<%d && (okReste == 0 || strlen(okReste) != 0)) {" % len(liste_fct))
        L.append("\t\tokReste = fun_ptrs[i](input);")
        L.append("\t\ti++;\n\t}")
        L.append("\treturn okReste;")
        L.append("}")

    """ Including libraries """
    L.insert(0, "#include <stdio.h>")
    L.insert(0, "#include <stdlib.h>")
    L.insert(0, "#include <string.h>")
    
    """ Adding the main() """
    L.append("int main(int argc, char** argv) {") # main definition with args
    # Check if there is the right number of parameters (2: program name and the word to parse)
    L.append("\tif(argc != 2) {")
    L.append("\t\tprintf(\"Command type: %s \'word_to_parse\'\\n\", argv[0]);")
    L.append("\t\texit(1);")
    L.append("\t}")

    L.append("\tchar * wordToParse = argv[1];")
    L.append("\tchar* okReste = parse" + list(dico_elements_parses.keys())[0] + "(wordToParse);")
    L.append("\tif(okReste != 0 && strlen(okReste) == 0) {")
    L.append("\t\tprintf(\"OK\\n\");")
    L.append("\t}")
    L.append("\telse {")
    L.append("\t\tprintf(\"KO\\n\");")
    L.append("\t}")

    L.append("\treturn 0;")
    L.append("}")
with open(args.nom_fichier_output+".c", "w") as f:
    f.write("\n".join(L))
print("\n".join(L))
