#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-

from lotofacil import LotoFacilStats
import random

def random_num ():
    result = []

    while len(result) < 8: 
        temp = random.randrange(2,25,2) #Par
        if temp < 10:
            temp = '0'+str(temp)
            if (temp,0) not in result:
                result.append((temp, 0))
        else:
            if (str(temp),0) not in result:
                result.append((str(temp), 0))

    while len(result) < 15: 
        temp = random.randrange(1,25,2) #Impar
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
    start = 50
    end = 706
    facil = LotoFacilStats('D_LOTFAC.HTM', start - 1)
    stat = {'11ac':0, '12ac':0, '13ac':0, '14ac':0, '15ac':0}

    # um mesmo numero aleatorio para todos os sorteios
    #result = random_num()

    for ind in range(start, end):
        #result = facil.suggest_num(method='Score', for_print=False)
        #result = facil.suggest_num(method='Most Recently', for_print=False)
        #result = facil.suggest_num(method='Least Recently', for_print=False)
        #um numero aleatorio a cada sorteio
        result = random_num()

        par = 0
        impar = 0
        aux_list = []

        # para ser usado com o metodo suggest_num
        #for el in result:
        #    if len(aux_list) >= 15:
        #        break

        #    if utils.isodd(int(el[0])):
        #        if impar < 7:
        #            aux_list.append(el)
        #            impar += 1
        #    elif not utils.isodd(int(el[0])):
        #        if par < 8:
        #            aux_list.append(el)
        #            par += 1

        #result = aux_list[:15]
        result = result[:15]
        for each in result:
            (x,y) = each
            suggested.append(x)

        facil = LotoFacilStats('D_LOTFAC.HTM', ind)
        dozens = facil.all_content[-1]['Dozens']
        doz_aux = []
        num_acertos = 0
        for doz_elem in dozens:
            if doz_elem in suggested:
                doz_aux.append(doz_elem)
                num_acertos += 1

        if num_acertos == 11 : stat['11ac'] += 1
        elif num_acertos == 12 : stat['12ac'] += 1
        elif num_acertos == 13 : stat['13ac'] += 1
        elif num_acertos == 14 : stat['14ac'] += 1
        elif num_acertos == 15 : stat['15ac'] += 1

        both_value = (sorted(suggested), doz_aux)
        print (both_value)
        suggested = []

    print(stat)
