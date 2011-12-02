#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
    TODO: 
"""
from quina import QuinaStats
from sena import SenaStats

if __name__ == '__main__':
    done = False
    
    while not done :
    
        print ('')
        print ('\033[92m' + "The following lottery games are available: " + '\033[0m')
        print ('')
        print ("quina : show statistics for quina lottery game")
        print ("mega  : show statistics for mega-sena lottery game")
        print ("done  : exit the program")
        print ('')
        cmd = raw_input('\033[92m' + 'Choose the game :' + '\033[0m')
        print ('')

        if cmd == 'quina':
            quina = QuinaStats('D_QUINA.HTM')
            quina.screen_interf()
        elif cmd == 'mega':
            sena = SenaStats('d_megasc.htm')
            sena.screen_interf()
        elif cmd == 'done' :
            done = True
        else :
            print ("I don't understand the command " + cmd)
