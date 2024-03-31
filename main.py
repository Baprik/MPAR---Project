from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
from interface import launch_interface
from mdp import gramPrintListener
from tools import PCTL, best_adv_for_PCTL, monteCarloStat, best_adv_for_MC, Qlearning, inv ,QlearningAuto,SPRT
import argparse



def main(name, analyse):
    #lexer = gramLexer(StdinStream())
    lexer = gramLexer(FileStream("ex2.mdp")) #pour éviter d'écrirer le < ex.mdp
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    printer.current_state = printer.states[0]
    print(printer.states)
    print(printer.trans)
    printer.raiseErreurs()
    print(printer.rewards)
    if analyse:
        print(f"Le meilleur adversaire selon PCTL :{best_adv_for_PCTL(printer, 10, ['S4'], [], 'S0')}")
        print(f"Le meilleur adversaire selon PCTL :{best_adv_for_MC(printer, 10,'S0','S4')}")
        adv = printer.create_adv()
        SPRT(0.1,0.01,printer,"S0" ,"S4" , adv ,100)
        print(f"Le Q obtenue est: {QlearningAuto(100, printer, 1/2, inv)}")
    else:
        launch_interface(printer)

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Programme avec analyse")
    parser.add_argument('--analysis',default=False, help='Activer l\'analyse')
    parser.add_argument('--name', default="ex.mdp", help='Activer l\'analyse')
    args = parser.parse_args()

    main(args.name, args.analysis)