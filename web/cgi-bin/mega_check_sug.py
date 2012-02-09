#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-

from sena import SenaStats
import pdb
import random
import utils

def random_num ():
    result = []
    par = 0
    impar = 0

    while len(result) < 8: 
        temp = random.randrange(2,60,2) #Par
        if temp < 10:
            temp = '0'+str(temp)
            if (temp,0) not in result:
                result.append((temp, 0))
        else:
            if (str(temp),0) not in result:
                result.append((str(temp), 0))

    while len(result) < 15: 
        temp = random.randrange(1,60,2) #Impar
        if temp < 10:
            temp = '0'+str(temp)
            if (temp,0) not in result:
                result.append((temp, 0))
        else:
            if (str(temp),0) not in result:
                result.append((str(temp), 0))
    return result

if __name__ == '__main__':

    suggested = []
    start = 100
    end = 1354
    sena = SenaStats('../data/d_megasc.htm', start - 1)
    stat = {'0ac':0, '1ac':0, '2ac':0, '3ac':0, '4ac':0, '5ac':0, '6ac':0}

    # um mesmo numero aleatorio para todos os sorteios
    #result = random_num()

    for ind in range(start, end):
        result = sena.suggest_num(method='Score', for_print=False)
        #result = sena.suggest_num(method='Most Recently', for_print=False)
        #result = sena.suggest_num(method='Least Recently', for_print=False)
        #um numero aleatorio a cada sorteio
        #result = random_num()

        par = 0
        impar = 0
        aux_list = []

        for el in result:
            if len(aux_list) >= 15:
                break

            if utils.isodd(int(el[0])):
                if impar < 7:
                    aux_list.append(el)
                    impar += 1
            elif not utils.isodd(int(el[0])):
                if par < 8:
                    aux_list.append(el)
                    par += 1

        result = aux_list[:15]
        #result = result[:15]
        for each in result:
            (x,y) = each
            suggested.append(x)

        sena = SenaStats('../data/d_megasc.htm', ind)
        dozens = sena.all_content[-1]['Dozens']
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
        elif num_acertos == 6 : stat['6ac'] += 1

        both_value = (sorted(suggested), doz_aux)
        print (both_value)
        suggested = []

    print(stat)
