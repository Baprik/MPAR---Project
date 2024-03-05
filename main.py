from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
from interface import launch_interface
from mdp import gramPrintListener



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
    launch_interface(printer)

if __name__ == '__main__':
    main()