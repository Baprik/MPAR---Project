from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
from interface import launch_interface
from mdp import gramPrintListener
from tools import PCTL



def main():
    #lexer = gramLexer(StdinStream())
    lexer = gramLexer(FileStream("ex2.mdp")) #pour éviter d'écrirer le < ex.mdp
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    printer.current_state = printer.states[0]
    printer.raiseErreurs()
    print(printer.trans)
    #print(printer.return_proba('S11','S22','a'))
    
    adv = printer.create_adv(is_random=False)
    print(f'{adv=}')
    print(PCTL(printer, 10, ['S4'], [], adv))
    #launch_interface(printer)
    

if __name__ == '__main__':
    main()