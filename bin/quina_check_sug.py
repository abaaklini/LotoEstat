#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-

from quina import QuinaStats
import pdb
import random
import utils
import sys

def random_num ():
    result = []
    par = 0
    impar = 0

    for x in range(4):
        temp = random.randrange(2,80,2) #Par
        if temp < 10:
            result.append(('0'+ str(temp), 0))
        else:
            result.append((str(temp), 0))

    for x in range(3):
        temp = random.randrange(1,80,2) #Impar
        if temp < 10:
            result.append(('0'+ str(temp), 0))
        else:
            result.append((str(temp), 0))
    return result

def main():

    suggested = []
    start = 150
    end = 2801
    quina = QuinaStats('../data/D_QUINA.HTM', start - 1)
    stat = {'0ac':0, '1ac':0, '2ac':0, '3ac':0, '4ac':0, '5ac':0}

    if len(sys.argv) < 2 or sys.argv[1] not in ['score', 'most', 'least', 'rand_all', 'rand_one']:
        print ('Usage : %s  [score|most|least|rand_all|rand_one]' % (sys.argv[0],))
        return 1

    if sys.argv[1] == 'rand_one':
        # um mesmo numero aleatorio para todos os sorteios
        result = random_num()

    method = None

    if sys.argv[1] == 'score':
        method = 'Score'

    if sys.argv[1] == 'most':
        method = 'Most Recently'

    if sys.argv[1] == 'least':
        method = 'Least Recently'

    for ind in range(start, end):
        if method:
            result = quina.suggest_num(method, for_print=False)
            par = 0
            impar = 0
            aux_list = []

            for el in result:
                if len(aux_list) >= 7:
                    break

                if utils.isodd(int(el[0])):
                    if impar < 3:
                        aux_list.append(el)
                        impar += 1
                elif not utils.isodd(int(el[0])):
                    if par < 4:
                        aux_list.append(el)
                        par += 1

            result = aux_list[:7]

        elif sys.argv[1] == 'rand_all':
            result = random_num()
            result = result[:7]

        else:
            result = result[:7]

        for each in result:
            (x,y) = each
            suggested.append(x)

        quina = QuinaStats('../data/D_QUINA.HTM', ind)
        dozens = quina.all_content[-1]['Dozens']
        doz_aux = []
        num_acertos = 0
        for doz_elem in dozens:
            if doz_elem in suggested:
                doz_aux.append(doz_elem)
                num_acertos += 1

        if num_acertos == 0 : stat['0ac'] += 1
        elif num_acertos == 1 : stat['1ac'] += 1
        elif num_acertos == 2 : stat['2ac'] += 1
        elif num_acertos == 3 : stat['3ac'] += 1
        elif num_acertos == 4 : stat['4ac'] += 1
        elif num_acertos == 5 : stat['5ac'] += 1

        both_value = (sorted(suggested), doz_aux)
        print (both_value)
        suggested = []

    print(stat)
if __name__ == '__main__': main()

