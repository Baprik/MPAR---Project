from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
from interface import launch_interface
from mdp import gramPrintListener
from tools import PCTL, best_adv_for_PCTL, monteCarloStat, best_adv_for_MC, Qlearning, inv 



def main():
    #lexer = gramLexer(StdinStream())
    lexer = gramLexer(FileStream("ex.mdp")) #pour éviter d'écrirer le < ex.mdp
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    printer.current_state = printer.states[0]
    print(printer.states)
    printer.raiseErreurs()
    print(printer.rewards)
    
    print(best_adv_for_PCTL(printer, 10, ['S4'], [], 'S0'))
    print(best_adv_for_MC(printer, 10,'S0','S4'))
    print(Qlearning(100, printer, 1/2, inv))
    #launch_interface(printer)
    print()
    

if __name__ == '__main__':
    main()