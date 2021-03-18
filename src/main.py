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
    # Definition de fonctions / element prealables pour extraire les elements de V
    L = ["""
typedef struct _next {
    char* next_val;
    char* suite;
}next;

int strequ(char* str1,char* str2) {
    /** Fonction permettant de comparer 2 terminaux
      * Output : int : 0 false 1 true
      **/
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
    /** Fonction permettant d'avoir acces au prochain litteral / non litteral a traiter
      * Output : next (struct) : contient a la fois le prochain element de V et la suite (string) du mot a parser dans 2 champs
      **/
    next* n;
    n = malloc(sizeof(next));
    if(input == 0) { // si on demande le prochain element de V alors que l'on est dans une situation ou le parsage est deja un echec
        n->next_val = 0;
        n->suite = 0;
        return n;
    }
    int length = strlen(input);
    if(length == 0) { // si on demande le prochain element de V alors que l'on est a la fin du mot (chaine vide "" avec le \\0
        n->next_val = 0;
        n->suite = 0;
        return n;
    }
    // Sinon on peut preparer les emplacements pour stocker le prochain element et la suite du mot (en prenant large en memoire)
    n->next_val = malloc(length*sizeof(char));
    n->suite = malloc(length*sizeof(char));
    int dans_next_val = 1; //indique si on n'a pas encore fini de rassembler le prochain element de V
    int longueur_next_val;
    for (int i = 0;i < length;i++) {
        if(input[i] != ' ' && dans_next_val == 1) { // Si l'on n'a pas encore fini d'extraire le prochain element de V
            n->next_val[i] = input[i];
        }
        else if (input[i] == ' ' && dans_next_val == 1) { // Si l'on est a la limite (espace) entre le prochain element de V et la suite du mot
            n->next_val[i] = '\\0';
            dans_next_val = 0;
            longueur_next_val = strlen(n->next_val);
        }
        else {// Si l'on a la suite du mot
            n->suite[i-longueur_next_val-1] = input[i];
        }
    }
        
    return n;
}
"""]

    dico_elements_parses = {}
    for i,l in enumerate(f.readlines()):
        # Extraction pour chaque regle du non terminal et de sa dérivation possible
        [head, rule] = [e.strip() for e in l.strip().split(":")]
        # On groupe toutes les règles dérivant d'un même non terminal source ensemble
        if head not in dico_elements_parses.keys():
            dico_elements_parses[head] = ["parse%s%d" % (head,i)]
        else:
            dico_elements_parses[head].append("parse%s%d" % (head,i))
        # Création de la fonction chargée de parser suivant la règle actuelle extraite
        L.insert(0,"char* parse%s%d(char * input);" % (head,i)) # Définitio nde la fonction en en-tête du fichier
        L.append("char* parse%s%d(char * input) {" % (head,i))
        L.append("\tprintf(\"Passage dans parse%s%d %%s\\n\",input);" % (head,i))
        L.append("\tchar* okReste = input;") # Contiendra ce qu'il reste à parser et NULL si il y a eu échec de parsage
        rules = rule.split()
        # Remplissage de la fonction de parsage pour chaque :
        for i,lettre in enumerate(rules):
            # On consomme au fur et à mesure la chaine (grâce à next_val) dans okReste et on sort si on ne peut pas parser
            if lettre.lower() != lettre: # non-terminal
                # Une fonction globale de parsage d'un non_terminal retourne 0 (NULL) si il y eu échec et sinon la chaine restante
                L.append(f"\tokReste = parse{lettre}(okReste);")
                L.append(f"\tif (okReste == NULL) return 0;")
            else: # ou terminal
                # Une fonction de parsage précise travaille (non/)terminal après (non/)terminal
                L.append(f"\tnext* n{i} = next_val(okReste);")
                L.append(f"\tif ((n{i}->next_val == 0 && n{i}->suite == 0) || strequ(n{i}->next_val,\"{lettre}\") == 0)")
                L.append(f"\t\treturn 0;")
                L.append("\telse {")
                L.append(f"\t\t okReste = n{i}->suite;")
                L.append("\t}")
        L.append("\treturn okReste;")
        L.append("}\n")
    # Constitution des fonctions de parsage globales
    for head,liste_fct in dico_elements_parses.items():
        L.insert(0,"char* parse%s(char *input);" % head) # Ajout de la fonction à l'en tête du fichier
        L.append("char* parse%s(char *input) {" % head)
        L.append("\tprintf(\"Passage dans parse%s %%s\\n\",input);" % head)
        L.append("\tchar* okReste = 0;int i = 0;")
        # La fonction tente de parser en utilisant à la suite toutes les règles possibles.
        # La première qui fonctionne est retenue
        # Ceela est réalisé à l'aide d'un tableau contenant les fonctions de parsage disponibles
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
