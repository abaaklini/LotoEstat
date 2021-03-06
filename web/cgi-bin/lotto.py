#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
"""Copyright (C) 2011 Alexandre Baaklini, abaaklini@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

"""
"""
from quina import QuinaStats
from sena import SenaStats
from lotofacil import LotoFacilStats

if __name__ == '__main__':
    done = False
    
    while not done :
    
        print ('')
        print ('\033[92m' + "The following lottery games are available: " + '\033[0m')
        print ('')
        print ("quina : show statistics for quina lottery game")
        print ("mega  : show statistics for mega-sena lottery game")
        print ("facil : show statistics for lotofacil lottery game")
        print ("done  : exit the program")
        print ('')
        cmd = raw_input('\033[92m' + 'Choose the game :' + '\033[0m')
        print ('')

        if cmd == 'quina':
            quina = QuinaStats('../data/D_QUINA.HTM')
            quina.screen_interf()
        elif cmd == 'mega':
            sena = SenaStats('../data/d_megasc.htm')
            sena.screen_interf()
        elif cmd == 'facil':
            facil = LotoFacilStats('../data/D_LOTFAC.HTM')
            facil.screen_interf()
        elif cmd == 'done' :
            done = True
        else :
            print ("I don't understand the command " + cmd)
