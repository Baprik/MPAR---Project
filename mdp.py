from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
import sys
import random

        
class gramPrintListener(gramListener):

    def __init__(self):
        self.states = []
        self.actions = []
        self.trans = []
        # La clé serait l'état dans lequel on est + le choix et la valeur associée : liste de tuples vers l'état d'arrivée et le poids associé
        pass

    def raiseErreur_proba(self) :
        raise ValueError("Problème sur l'affectation des probabilités")
        
    def enterDefstates(self, ctx):
        self.states = [str(x) for x in ctx.ID()]
        print(self.states)
        #print("States: %s" % str([str(x) for x in ctx.ID()]))

    def enterDefactions(self, ctx):
        self.actions = [str(x) for x in ctx.ID()]
        print(self.actions)
        #print("Actions: %s" % str([str(x) for x in ctx.ID()]))


    def enterTransact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        act = ids.pop(0)
        weights = [int(str(x)) for x in ctx.INT()]
        if sum(weights) != 10 :
            self.raiseErreur_proba()
        for i in range(len(ids)) :
            self.trans.append((dep,ids[i],weights[i],True, act)) #(depart,arrivée,weight,choice,action)
        #print("Entrer dans Transact")
        #print("Transition from " + dep + " with action "+ act + " and targets " + str(ids) + " with weights " + str(weights))
        #print(self.trans)

    def enterTransnoact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        weights = [int(str(x)) for x in ctx.INT()]
        for i in range(len(ids)) :
            self.trans.append((dep,ids[i],weights[i],False, None)) #(depart,arrivée,weight,choice,action)
        #print("Entrée dans Transnoact")
        #print("Transition from " + dep + " with no action and targets " + str(ids) + " with weights " + str(weights))
        #print(self.trans)
    
    def possible_choices(self, state : str)  :
        ''' Retourne les transitions possibles pour un état donné'''
        choices = []
        for transition in self.trans :
            if transition[0] == state :
                choices.append((transition[1], transition[2], transition[-1])) # (Arrivée, Poids, Choix (None si pas de choix))
        return choices
    
    def etat_suivant(self, state_ini : str, action_choisie : str) :
        if action_choisie == None :
            total_weight = sum(t[1] for t in self.possible_choices(state_ini) if t[-1] == None)
            print(f"Total_weight : {total_weight}")
            weight = 0 
            x = random.uniform(0,1)
            print(f"x : {x}")
            for tuple in self.possible_choices(state_ini) :
                weight += tuple[1]
                if x <= (weight/total_weight) :
                   return tuple[0]
        else :
            total_weight = sum(t[1] for t in self.possible_choices(state_ini) if t[-1] == action_choisie)
            print(f"Total_weight : {total_weight}")
            weight = 0 
            x = random.uniform(0,1)
            print(f"x : {x}")
            for tuple in self.possible_choices(state_ini) :
                if tuple[-1] == action_choisie :
                    print(f"tuple : {tuple}")
                    weight += tuple[1]
                    if x <= (weight/total_weight) :
                        return tuple[0]

def main():
    lexer = gramLexer(StdinStream())
    # lexer = gramLexer(FileStream("ex.mdp")) pour éviter d'écrirer le < ex.mdp
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    print(printer.trans)
    print("Choix possibles pour S1")
    print(printer.possible_choices('S1'))
    print(printer.etat_suivant('S1', 'a'))

if __name__ == '__main__':
    main()
