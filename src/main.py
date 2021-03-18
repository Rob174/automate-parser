import os
import argparse
print(os.getcwd())
parser = argparse.ArgumentParser()
parser.add_argument('path_grammar', type=str,
                    help='Chemin vers le fichier de grammaire')
parser.add_argument('-o', dest='nom_fichier_output',
                    help="Specifie le nom du fichier c de destination (sans l'extension)")

args = parser.parse_args()

with open(args.path_grammar, "r") as f:
    L = ["""
typedef struct _next {
    char* next_val;
    char* suite;
}next;

int strequ(char* str1,char* str2) {
    int length = strlen(str1);
    if(strlen(str2) != length)
        return 0;
    for (int i = 0; i < length;i++) {
        if(str1[i] != str2[i])
            return 0;
    }
    return 1;
}
next* next_val(char * input) {
    next* n;
    n = malloc(sizeof(next));
    if(input == 0) { 
        n->next_val = 0;
        n->suite = 0;
        return n;
    }
    int length = strlen(input);
    if(length == 0) { 
        n->next_val = 0;
        n->suite = 0;
        return n;
    }
    n->next_val = malloc(length*sizeof(char));
    n->suite = malloc(length*sizeof(char));
    int dans_next_val = 1;
    int longueur_next_val;
    for (int i = 0;i < length;i++) {
        if(input[i] != ' ' && dans_next_val == 1) {
            n->next_val[i] = input[i];
        }
        else if (input[i] == ' ' && dans_next_val == 1) {
            n->next_val[i] = '\\0';
            dans_next_val = 0;
            longueur_next_val = strlen(n->next_val);
        }
        else {
            n->suite[i-longueur_next_val-1] = input[i];
        }
    }
        
    return n;
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
        rules = rule.split()
        for i,lettre in enumerate(rules):
            if lettre.lower() != lettre: # Cas non-terminal
                """passage a revoir : comment separer les parties a tester avec les variables"""
                L.append(f"\tokReste = parse{lettre}(okReste);") # A revoir comment on extrait la partie interessante ; comment on decoupe ;
                """split dans une boucle en deplacant le moment ou on coupe entre la variable courante et la suivante
                Si un terminal apres s'arreter au terminal"""
                L.append(f"\tif (okReste == NULL) return 0;")
            else: # Cas terminal
                L.append(f"\tnext* n{i} = next_val(okReste);")
                L.append(f"\tif ((n{i}->next_val == 0 && n{i}->suite == 0) || strequ(n{i}->next_val,\"{lettre}\") == 0)")
                L.append(f"\t\treturn 0;")
                L.append("\telse {")
                L.append(f"\t\t okReste = n{i}->suite;")
                L.append("\t}")
        L.append("\treturn okReste;")
        L.append("}\n")
    for head,liste_fct in dico_elements_parses.items():
        L.insert(0,"char* parse%s(char *input);" % head)
        L.append("char* parse%s(char *input) {" % head)
        L.append("\tprintf(\"Passage dans parse%s %%s\\n\",input);" % head)
        L.append("\tchar* okReste = 0;int i = 0;")
        L.append(f"\tchar* (*fun_ptrs[{len(liste_fct)}])(char*) = " + "{"+",".join(liste_fct)+"};")
        L.append("\twhile(i<%d && (okReste == 0)) {" % len(liste_fct))
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
