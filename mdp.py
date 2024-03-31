from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
import sys
import random

class MarkovError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class StateError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ActionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class gramPrintListener(gramListener):

    def __init__(self):
        self.states = []
        self.actions = []
        self.trans = []
        self.current_state = None 
        self.previous_state = None 
        self.choice = None
        self.states_decision = []
        self.states_non_dec = []
        self.rewards = {}
        # La clé serait l'état dans lequel on est + le choix et la valeur associée : liste de tuples vers l'état d'arrivée et le poids associé
        pass

    def raiseErreur_state(self) :
        for tuple in self.trans :
            if tuple[0] not in self.states:
                raise StateError(f"L'état {tuple[0]} dans la transition n'a pas été préalablement déclaré")
            if tuple[1] not in self.states:
                raise StateError(f"L'état {tuple[1]} dans la transition n'a pas été préalablement déclaré")
    
    def raiseErreur_action(self) :
        for tuple in self.trans :
            if tuple[-1] != None :
                if tuple[-1] not in self.actions:
                    raise ActionError(f"L'action {tuple[-1]} n'a pas été préalablement déclaré")
                
    def raiseErreur_poids(self) :
        for tuple in self.trans :
            if tuple[2] <= 0 :
                raise ValueError(f"Le poids associé à la transition de {tuple[0]} à {tuple[1]} ne peut pas être négatif ou nul")
    
    def raiseErreur_DecisionMarkovien(self) :
        for tuple in self.trans :
            if tuple[-1] != None and tuple[0] not in self.states_decision :
                self.states_decision.append(tuple[0])
            elif tuple[-1] == None and tuple[0] not in self.states_non_dec :
                self.states_non_dec.append(tuple[0])
        for state in self.states_decision :
            if state in self.states_non_dec :
                raise MarkovError(f"L'état {state} ne peut pas mélanger une transition avec action et sans action")
    
    def raiseErreur_doublons(self) :
        for tuple1 in self.trans :
            for tuple2 in self.trans :
                if tuple1 != tuple2 and tuple1[-1] == None :
                    if tuple1[0] == tuple2[0] and tuple1[1] == tuple2[1] :
                        raise MarkovError(f"Il y a plusieurs transitions indiqués allant de {tuple1[0]} à {tuple1[1]}, merci de bien vouloir l'indiquer en une seule et même ligne")
                if tuple1 != tuple2 and tuple1[-1] != None and tuple1[-1] == tuple2[-1] : # Cas où on a plusieurs actions qui mènent au même point
                    if tuple1[0] == tuple2[0] and tuple1[1] == tuple2[1] :
                        raise MarkovError(f"Il y a plusieurs transitions indiqués allant de {tuple1[0]} à {tuple1[1]}, merci de bien vouloir l'indiquer en une seule et même ligne")
    
    def raiseErreurs(self) :
        self.raiseErreur_action()
        self.raiseErreur_state()
        self.raiseErreur_poids()
        self.raiseErreur_DecisionMarkovien()
        self.raiseErreur_doublons()

    def enterStaterew(self, ctx):
        self.states = [str(x) for x in ctx.ID()]
        print(f"States : {self.states}")
        rewards = [int(str(x)) for x in ctx.INT()]
        self.rewards = dict(zip(self.states, rewards))
        for state in self.states :
            if state not in self.rewards.keys() :
                self.rewards[state] = 0
        print(f"Rewards : {self.rewards}")

    def enterStatenorew(self, ctx):
        self.states = [str(x) for x in ctx.ID()]
        print(f"States : {self.states}")
        rewards = [0 for x in ctx.ID()]
        self.rewards = dict(zip(self.states, rewards))
        print(f"Rewards : {self.rewards}")

    def enterDefactions(self, ctx):
        self.actions = [str(x) for x in ctx.ID()]
        print(f"Actions : {self.actions}")

    def enterTransact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        act = ids.pop(0)
        weights = [int(str(x)) for x in ctx.INT()]
        for i in range(len(ids)) :
            self.trans.append((dep,ids[i],weights[i],True, act)) #(depart,arrivée,weight,choice,action)

    def enterTransnoact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        weights = [int(str(x)) for x in ctx.INT()]
        for i in range(len(ids)) :
            self.trans.append((dep,ids[i],weights[i],False, None)) #(depart,arrivée,weight,choice,action)
    
    def possible_choices(self, state : str)  :
        ''' Retourne les choix possibles pour un état donné'''
        choices = None
        for transition in self.trans :
            if transition[0] == state and transition[-1] != None :
                if choices == None:
                    choices = []
                choices.append( transition[-1]) # (Arrivée, Poids, Choix (None si pas de choix))
        return choices
    
    def possible_trans(self, state : str)  :
        ''' Retourne les transitions possibles pour un état donné'''
        choices = []
        for transition in self.trans :
            if transition[0] == state :
                choices.append((transition[1], transition[2], transition[-1])) # (Arrivée, Poids, Choix (None si pas de choix))
        return choices
    
    def etat_suivant(self, state_ini : str, action_choisie : str) :
        if action_choisie == None :
            total_weight = sum(t[1] for t in self.possible_trans(state_ini) if t[-1] == None)
            weight = 0 
            x = random.uniform(0,1)
            #print(f"x : {x}")
            for tuple in self.possible_trans(state_ini) :
                weight += tuple[1]
                if x <= (weight/total_weight) :
                   self.previous_state = self.current_state
                   self.current_state = tuple[0]
                   #print(f"Etat actuel : {tuple[0]}")
                   return tuple[0]
        else :
            total_weight = sum(t[1] for t in self.possible_trans(state_ini) if t[-1] == action_choisie)
            weight = 0 
            x = random.uniform(0,1)
            #print(f"x : {x}")
            for tuple in self.possible_trans(state_ini) :
                if tuple[-1] == action_choisie :
                    weight += tuple[1]
                    if x <= (weight/total_weight) :
                        self.previous_state = self.current_state
                        self.current_state = tuple[0]
                        #print(f"Etat actuel : {tuple[0]}")
                        self.choice = action_choisie
                        return tuple[0]
    
    def return_proba(self, S1, S2, action = None) -> float:
        total_weight = sum(t[1] for t in self.possible_trans(S1) if t[-1] == action)
        for tran in self.trans:
            if tran[0] == S1 and tran[1] == S2 and tran[4] == action:
                return tran[2]/total_weight
        return 0 
    
    def create_adv(self, is_random = False):
        adv = {}
        if is_random:
            for state in self.states:
                choices = self.possible_choices(state)
                if choices == None:
                    adv[state] = None
                else:
                    choice = random.choice(choices)
                    adv[state] = choice
        else:
            for state in self.states:
                choices = self.possible_choices(state)
                choice = None
                adv[state] = choice
                while choices != None and choice not in choices:
                    choice = input(f"Choisissez le choix pour votre adversaire à l'état {state} parmis les choix {set(choices)}.")
                    adv[state] = choice
        return adv
    
    def liste_adv_possible(self, n = 100):
        liste_adv = []
        for _ in range(n):
            is_in = False
            new_adv = self.create_adv(is_random= True)
            for adv in liste_adv:
                if adv == new_adv:
                    is_in = True
                    break
            if not is_in:
                liste_adv.append(new_adv)
        return liste_adv

    def access(self, state_target, nb_coup, adv):
        k = 0 
        while k < nb_coup:
            k += 1
            self.etat_suivant(self.current_state,adv[self.current_state])
            if self.current_state == state_target:
                return 1 
        
        return 0 

