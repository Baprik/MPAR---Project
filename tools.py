from mdp import gramPrintListener
import numpy as np 
from copy import deepcopy
from math import log, log10

def PCTL(gram : gramPrintListener, iter : int, S0 : list, S1 : list, adv : dict = {}) -> dict:
    n_states = len(gram.states)
    n_ = n_states - len(S0) - len(S1)
    A = np.zeros([n_,n_])
    b = np.zeros([n_])
    states_ = deepcopy(gram.states)
    for state in S0:
        states_.remove(state)
    for state in S1:
        states_.remove(state)
    for state_x in states_:
        for state_y in states_:
            x = states_.index(state_x)
            y = states_.index(state_y)
            p = gram.return_proba(state_x, state_y, adv[state_x])
            A[x][y] = p 
    
    for state_x in states_:
        for state_0 in S0:
            x = states_.index(state_x)
            p = gram.return_proba(state_x, state_0, adv[state_x])
            b[x] += p 
    
    y = deepcopy(b)
    for _ in range(iter):
        y = np.dot(A,y) + b 
    
    y_dic = {state_x : y[states_.index(state_x)] for state_x in states_}

    return y_dic

def best_adv_for_PCTL(gram : gramPrintListener, iter, S0, S1, target):
    y = 0
    best_adv = {}
    liste_adv = gram.liste_adv_possible()
    for adv in liste_adv:
        y_ = PCTL(gram, iter, S0, S1, adv)[target]
        if y_ > y:
            y= y_
            best_adv = adv 
    return (best_adv, y)

def monteCarloStat(gram : gramPrintListener, nb_coup, iter_MC, current_state, target_state,adv):
    access = 0 
    for _ in range(iter_MC):
        gram.current_state = current_state
        access += gram.access(target_state,nb_coup,adv)
    return access/iter_MC

def best_adv_for_MC(gram :gramPrintListener, nb_coup : int, current_state : str, target_state : str, precision = 0.01, erreur = 0.01) -> tuple[dict, float]:
    iter_mc = int(round((log(2) - log(erreur))/(2*precision)**2))
    y = 0
    best_adv = {}
    liste_adv = gram.liste_adv_possible()
    for adv in liste_adv:
        y_ = monteCarloStat(gram,nb_coup, iter_mc, current_state, target_state, adv)
        if y_ > y:
            y= y_
            best_adv = adv 
    return (best_adv, y)

def SPRT(p : float,eps : float,model : gramPrintListener,current_state :str ,target_state : str, adv : dict,nb_coup :int, alpha = 0.01, beta = 0.01) -> None:
    A = (1- beta)/alpha
    B = beta/ (1 - alpha)
    inf = p - eps
    sup = p + eps
    dm = 0
    m = 0 
    Rm = 1
    m +=1
    if model.access(target_state, nb_coup, adv) == 1:
        dm += 1
        Rm *= inf/sup
    else:
        Rm *= (1-inf)/(1-sup)
    while Rm < A and Rm > B:
        model.current_state = current_state
        m +=1
        if model.access(target_state, nb_coup, adv) == 1:
            dm += 1
            Rm *= inf/sup
        else:
            Rm *= (1-inf)/(1-sup)
    if Rm > A :
        print(f"proba < {round(inf, int(abs(log10(eps))))}")
    if Rm < B:
        print(f"proba > {round(sup, int(abs(log10(eps))))}")


def Qlearning(Tmax: int, model: gramPrintListener, gamma: float, alpha) -> dict:
    #Initialize(Q0)
    Q = {}
    for state in model.states:
        if model.possible_choices(state) != None:
            for choix in model.possible_choices(state):
                Q[(state,choix)] = model.rewards[state]
        else:
            Q[(state,None)] = model.rewards[state]
    print(Q)
    for t in range(Tmax):
        s = 0
        a = 0
        print(f"Liste action: {model.states} or -1 for end")
        if s == -1:
            return Q
        s = input()
        while s not in model.states:
            print(f"{s} n'est pas un état du modèle. Liste action: {model.states} or -1 for end")
            if s == -1:
                return Q
            s = input()
            
        if model.possible_choices(s) == None :
            a = None
        else:
            while a not in set(model.possible_choices(s)):
                print(f"Liste action: {set(model.possible_choices(s))}")
                a = input()
        model.current_state = s
        s_ = model.etat_suivant(s,a)
        r = model.rewards[s_]
        choices_possibles =  model.possible_choices(s_)
        print(f"Vous avez atteint l'état {s_}, le gain est {r}." )
        if choices_possibles == None:
            choices_possibles = [None]
        delta = r + gamma * max([Q[(s_,b)] for b in choices_possibles]) - Q[(s,a)]
        Q[(s,a)] = Q[(s,a)] + alpha(t)* delta 
    return Q

def QlearningAuto(Tmax, model : gramPrintListener, gamma, alpha):
    #Initialize(Q0)
    Q = {}
    apprentissage = {}
    for state in model.states:
        if model.possible_choices(state) != None:
            for choix in model.possible_choices(state):
                Q[(state,choix)] = model.rewards[state]
                apprentissage[(state,choix)] = 0
        else:
            Q[(state,None)] = model.rewards[state]
            apprentissage[(state,None)] = 0
    print(Q)
    s= model.states[0]

    for t in range(Tmax):
        ## CHOIX DE L'ACTION (on regarde l'action la moins choisie)
        if model.possible_choices(s) == None :
            a = None
        else:
            min_values = 100000
            for (state, action), value in apprentissage.items():
                if state == s and value < min_values:
                    min_values = value
                    a = action
        apprentissage[(s,a)] += 1
        model.current_state = s
        s_ = model.etat_suivant(s,a)
        r = model.rewards[s_]
        choices_possibles =  model.possible_choices(s_)
        if choices_possibles == None:
            choices_possibles = [None]
        delta = r + gamma * max([Q[(s_,b)] for b in choices_possibles]) - Q[(s,a)]
        Q[(s,a)] = Q[(s,a)] + alpha(t)* delta 
        s = s_
    print(f"{apprentissage=}")
    return Q

def inv(k):
    return 1/(k+1)

