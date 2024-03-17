from mdp import gramPrintListener
import numpy as np 
from copy import deepcopy

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






