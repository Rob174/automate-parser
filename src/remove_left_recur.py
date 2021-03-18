

def main_remove_direct_lrecursivity(input_path,output_path):
    def delete_direct_lrecursivity(dico_elements_parses):
        new_dico_elements_parses = {}
        for head,liste in dico_elements_parses.items():
            left_recursive = False
            LnonRec = []
            Lrec = []
            for regle_liste in liste:
                if len(regle_liste) == 0:
                    LnonRec.append(regle_liste)
                elif head == regle_liste[0]:
                    left_recursive = True
                    Lrec.append(regle_liste)
                else:
                    LnonRec.append(regle_liste)

            new_dico_elements_parses[head] = LnonRec
            if left_recursive:
                i = 0
                new_variable_name = head + str(i)
                while new_variable_name in dico_elements_parses.keys() or new_variable_name in new_dico_elements_parses.items():
                    i+=1
                    new_variable_name = head + str(i)
                print(LnonRec)
                new_dico_elements_parses[head] += [l + [new_variable_name] for l in LnonRec]
                new_dico_elements_parses[new_variable_name] = []
                for l in Lrec:
                    new_dico_elements_parses[new_variable_name].append(l[1:])
                    new_dico_elements_parses[new_variable_name].append(l[1:]+ [new_variable_name])
        return new_dico_elements_parses
    with open(input_path, "r") as f:
        dico_elements_parses = {}
        for i,l in enumerate(f.readlines()):
            [head, rule] = [e.strip() for e in l.strip().split(":")]
            if head not in dico_elements_parses.keys():
                dico_elements_parses[head] = [rule.split()]
            else:
                dico_elements_parses[head].append(rule.split())
        print(dico_elements_parses)
        print("-------------------------------------------------")
        new_dico_elements_parses = delete_direct_lrecursivity(dico_elements_parses)
        print(new_dico_elements_parses)
        print("-------------------------------------------------")
    with open(output_path,"w") as f1:
        for head,regles in new_dico_elements_parses.items():
            for regle in regles:
                f1.write(f"{head} : "+" ".join(regle)+"\n")