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
import cgitb

cgitb.enable()

import cgi
import yate
from quina import QuinaStats
from sena import SenaStats
from lotofacil import LotoFacilStats
import re


def main():
    form_data = cgi.FieldStorage()
    
    print(yate.start_response())
    print(yate.include_header('Estatísticas para Loterias do Brasil'))
    
    if not form_data:
        print(yate.header('Escolha um jogo: ', header_level=3))
        print(yate.start_form('jogos.py'))
        print(yate.drop_box('Jogos', {'Quina':'Quina',
            'Mega-Sena': 'Mega-Sena',
            'LotoFácil':'LotoFácil'}, 'Mega-Sena'))
    
        print(yate.header('Escolha uma estatística: ', header_level=3))
        print(yate.drop_box('Estat', {
            'doze': 'Dezenas Mais Sorteadas',
            'rule': 'Distribuição entre Pares e Impares',
            'wors': 'Maior tempo sem ser sorteado',
            'more': 'Mais Sorteado',
            'aver': 'Média de tempo sem ser sorteado',
            'sugs': 'Sugere números com melhor escore padrão',
            'sugl': 'Sugere números menos sorteados recentemente',
            'sugm': 'Sugere números sorteados recentemente',
            'last': 'Última vez sorteado',
            'unit': 'Unidades Mais Sorteadas'},
            'more'))
    
        print(yate.end_form('Enviar'))
    
    elif form_data.getvalue('Jogos') and form_data.getvalue('Estat'):
        jogo = form_data.getvalue('Jogos')
        estat = form_data.getvalue('Estat')
        if jogo == 'Quina':
            obj = QuinaStats('../data/D_QUINA.HTM')
        elif jogo == 'Mega-Sena':
            obj = SenaStats('../data/d_megasc.htm')
        elif jogo == 'LotoFácil':
            obj = LotoFacilStats('../data/D_LOTFAC.HTM')
        else:
            print(yate.para('Opção Inexistente'))
            print(yate.include_footer('&copy LotoEstat 2012'))
            return
    
        if form_data.getvalue('Estat') == 'more':
            print(yate.header('Números Mais Sorteados'))
            print(yate.para('Lista decrescente dos números mais sorteados da ' + form_data.getvalue('Jogos') + '.'))
            
            to_print = obj.prepare_to_print('More', for_print=False)
            print(yate.start_tb(['Dezena ', ' Número de Vezes Sorteado']))
            for each in to_print:
                print(yate.inner_tb([each[0],each[1]]))
            print(yate.end_tb())
        
        elif form_data.getvalue('Estat') == 'rule':
            print(yate.header('Distribuição entre Pares e Impares'))
            print(yate.para('Combinação de pares e ímpares entre os números da ' + form_data.getvalue('Jogos') + '.'))
            to_print = obj.print_rule_even_by_odd(for_print=False) 
            print(yate.start_tb(['Dezenas Pares ', ' Dezenas Ímpares ', ' Número de Vezes Sorteado']))
            p = re.compile('\d+')
            for each in to_print:
                even, odd = p.findall(each[0])
                print(yate.inner_tb([even, odd, each[1]]))
            print(yate.end_tb())
        
        elif form_data.getvalue('Estat') == 'unit':
            print(yate.header('Unidades Mais Sorteadas'))
            print(yate.para('Lista das Unidades mais Sorteadas dos Jogos da ' + form_data.getvalue('Jogos') + '.'))
            to_print = obj.print_more_often_unit(for_print=False) 
            print(yate.start_tb(['Dezenas terminadas em ', ' Número de Vezes Sorteado']))
            p = re.compile('\d+')
            for each in to_print:
                unidade = p.findall(each[0])
                print(yate.inner_tb([unidade[0], each[1]]))
            print(yate.end_tb())
        
        elif form_data.getvalue('Estat') == 'doze':
            print(yate.header('Dezenas Mais Sorteadas'))
            print(yate.para('Lista das Dezenas mais Sorteadas dos Jogos da ' + form_data.getvalue('Jogos') + '.'))
            to_print = obj.print_more_often_dozen(for_print=False) 
            print(yate.start_tb(['Dezenas Começadas por ', ' Número de Vezes Sorteado']))
            p = re.compile('\d+')
            for each in to_print:
                dezena = p.findall(each[0])
                print(yate.inner_tb([dezena[0], each[1]]))
            print(yate.end_tb())
        
        elif form_data.getvalue('Estat') == 'last':
            print(yate.header('Última vez Sorteado'))
            print(yate.para('A quanto tempo a dezena não é sorteada entre os números premiados da ' + form_data.getvalue('Jogos') + '.'))
            
            to_print = obj.prepare_to_print('Last', for_print=False)
            print(yate.start_tb(['Dezena ', ' Tempo sem ser sorteada']))
            for each in to_print:
                print(yate.inner_tb([each[0],each[1]]))
            print(yate.end_tb())
        
        elif form_data.getvalue('Estat') == 'wors':
            print(yate.header('Maior tempo sem ser sorteado'))
            print(yate.para('Pior tempo de espera que um número aguardou para ser sorteado entre todos os sorteios da ' + form_data.getvalue('Jogos') + '.'))
            
            to_print = obj.prepare_to_print('Worst', for_print=False)
            print(yate.start_tb(['Dezena ', ' Pior tempo sem ser sorteada']))
            for each in to_print:
                print(yate.inner_tb([each[0],each[1]]))
            print(yate.end_tb())
        
        elif form_data.getvalue('Estat') == 'aver':
            print(yate.header('Média de tempo sem ser sorteado'))
            print(yate.para('Tempo médio que um número leva até ser sorteado, obtidos à partir do histórico de resultados  da ' + form_data.getvalue('Jogos') + '.'))
            
            to_print = obj.prepare_to_print('Average', for_print=False)
            print(yate.start_tb(['Dezena ', ' Média de espera entre dois sorteios']))
            for each in to_print:
                print(yate.inner_tb([each[0],each[1]]))
            print(yate.end_tb())
        
        elif form_data.getvalue('Estat') == 'sugm':
            print(yate.header('Sugere números sorteados recentemente'))
            print(yate.para('Ordena os números da ' + form_data.getvalue('Jogos') + ' levando em conta as estatísticas individuais, favorecendo os números que saíram com mais frequencia e que foram sorteados recentemente.'))
            to_print = obj.suggest_num(method='Most Recently', for_print=False)
            if form_data.getvalue('Jogos') == 'Quina':
                dez_sug = 7 
            elif form_data.getvalue('Jogos') == 'Mega-Sena':
                dez_sug = 15 
            elif form_data.getvalue('Jogos') == 'LotoFácil':
                dez_sug = 15 

            cabecalho_tabela = []
            for num in range(1, dez_sug + 1):
                cabecalho_tabela.append(str(num) + 'ª dezena')
            print(yate.start_tb(cabecalho_tabela))
            lis = []
            for each in to_print[:dez_sug]:
                lis.append(each[0])
            print(yate.inner_tb(lis))
            print(yate.end_tb())
        
        elif form_data.getvalue('Estat') == 'sugl':
            print(yate.header('Sugere números menos sorteados recentemente'))
            print(yate.para('Ordena os números da ' + form_data.getvalue('Jogos') + ' levando em conta as estatísticas individuais, favorecendo os números que saíram com mais frequencia e que estão a mais tempo sem serem sorteados.'))
            to_print = obj.suggest_num(method='Least Recently', for_print=False)
            if form_data.getvalue('Jogos') == 'Quina':
                dez_sug = 7 
            elif form_data.getvalue('Jogos') == 'Mega-Sena':
                dez_sug = 15
            elif form_data.getvalue('Jogos') == 'LotoFácil':
                dez_sug = 15

            cabecalho_tabela = []
            for num in range(1, dez_sug + 1):
                cabecalho_tabela.append(str(num) + 'ª dezena')
            print(yate.start_tb(cabecalho_tabela))
            lis = []
            for each in to_print[:dez_sug]:
                lis.append(each[0])
            print(yate.inner_tb(lis))
            print(yate.end_tb())
        
        elif form_data.getvalue('Estat') == 'sugs':
            print(yate.header('Sugere números com melhor escore padrão'))
            print(yate.para('Ordena os números da ' + form_data.getvalue('Jogos') + ' levando em conta o escore padrão de cada um, favorecendo os números com menor desvio padrão da média de tempo de espera para um número ser sorteado.'))
            to_print = obj.suggest_num(method='Score', for_print=False)
            if form_data.getvalue('Jogos') == 'Quina':
                dez_sug = 7 
            elif form_data.getvalue('Jogos') == 'Mega-Sena':
                dez_sug = 15
            elif form_data.getvalue('Jogos') == 'LotoFácil':
                dez_sug = 15

            cabecalho_tabela = []
            for num in range(1, dez_sug + 1):
                cabecalho_tabela.append(str(num) + 'ª dezena')
            print(yate.start_tb(cabecalho_tabela))
            lis = []
            for each in to_print[:dez_sug]:
                lis.append(each[0])
            print(yate.inner_tb(lis))
            print(yate.end_tb())
        
        print(yate.para('Atualizado em : %s') % obj.print_updated_data())

    else :
        print(yate.para('Opção por Jogo ou Estatística não efetuada.'))
    
    print(yate.include_footer('&copy LotoEstat 2012'))

main()
