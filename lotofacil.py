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

from __future__ import print_function
from lottery import Lottery
import pdb
import os
import pickle
import utils
from parsepage import ParsePage
import operator
import numpy as np
import matplotlib.pyplot as plt

class LotoFacilStats (Lottery):
    """
    """
    def __init__(self, data_file, sub_table = 0):
        """
        """
        self.num_dozens = 25
        self.doz_by_raffle =15 

        Lottery.__init__(self)
        if os.path.exists('facil.pickle'):
            if os.path.getmtime('facil.pickle') > os.path.getmtime(data_file):
                try:
                    with open('facil.pickle', 'rb') as data_bin:
                        self.all_content = pickle.load(data_bin)
                        if sub_table > 0:
                            self.all_content = self.all_content[:sub_table]

                except IOError as err:
                    print ("File error: " + str(err))
        else:
            p = ParsePage(self.doz_by_raffle) 
            p.feed(utils.get_content(data_file))
            self.all_content = p.get_full_data()
            if sub_table > 0:
                self.all_content = self.all_content[:sub_table]
            try:
                with open('facil.pickle', 'wb') as data_bin:
                    pickle.dump(self.all_content, data_bin)

            except IOError as err:
                print ("File error: " + str(err))

        self.init_stat_table()
        self.even_odd = {"e0xo15": [], "e1xo14": [], "e2xo13": [], "e3xo12": [], "e4xo11": [], "e5xo10": [], "e6xo9": [], "e7xo8": [], "e8xo7": [], "e9xo6": [], "e10xo5": [], "e11xo4": [], "e12xo3": [], "e13xo2": [], "e14xo1": [], "e15xo0": []}
        self.doze = {"0x": [], "1x": [], "2x": []}
        self.build_occur_list()
        self.build_delay_list()
        self.more_often_num()
        self.last_time()
        self.most_delay()
        self.aver_delay()
        self.fill_up_stand_dev()
        self.fill_up_stand_sco()
        self.rule_even_by_odd()
        self.more_often_dozen()
        self.more_often_unit()

    ##### Methods for Printing #####
    def print_more_often_dozen (self):
        """
        """
        di = {'0x': len(self.doze['0x']),
              '1x': len(self.doze['1x']),
              '2x': len(self.doze['2x']) * 6.0/10}

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        for each in sorted_list:
            print(each)

    def print_rule_even_by_odd(self):
        """
        """
        di = {'e0xo15': len(self.even_odd['e0xo15']),
              'e1xo14': len(self.even_odd['e1xo14']),
              'e2xo13': len(self.even_odd['e2xo13']),
              'e3xo12': len(self.even_odd['e3xo12']),
              'e4xo11': len(self.even_odd['e4xo11']),
              'e5xo10': len(self.even_odd['e5xo10']),
              'e6xo9': len(self.even_odd['e6xo9']),
              'e7xo8': len(self.even_odd['e7xo8']),
              'e8xo7': len(self.even_odd['e8xo7']),
              'e9xo6': len(self.even_odd['e9xo6']),
              'e10xo5': len(self.even_odd['e10xo5']),
              'e11xo4': len(self.even_odd['e11xo4']),
              'e12xo3': len(self.even_odd['e12xo3']),
              'e13xo2': len(self.even_odd['e13xo2']),
              'e14xo1': len(self.even_odd['e14xo1']),
              'e15xo0': len(self.even_odd['e15xo0'])}

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        for each in sorted_list:
            print(each)

    ##### Methods for Plotting #####
    def plot_doze (self):
        """
        """
        done = False
        
        while not done :
            cmd = utils.print_second_menu()
        
            if cmd == 'pie' :
                #Pie chart
                vals = []
                keys = []
                for i, k in enumerate(self.doze):
                    vals.append(len(self.doze[k]))
                    keys.append(k)

                plt.figure(figsize=(6,6))
                plt.pie(vals, labels=keys, autopct='%1.1f%%')
                plt.show()

            elif cmd == 'line' :
                vals = []
                keys = []
                dic = {}
                for k, v in self.doze.items():
                    dic[k] = len(v)
                sorted_list = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
                for each in sorted_list:
                    (k, v) = each
                    vals.append(v)
                    keys.append(k)

                plt.plot(vals)
                plt.xticks(np.arange(len(keys)), keys)
                plt.show()

            elif cmd == 'bar' :
                for i, k in enumerate(self.doze):
                    plt.bar(i, len(self.doze[k]))

                plt.xticks(np.arange(len(self.doze)) + 0.4, self.doze.keys())
                plt.show()

            elif cmd == 'delay' :
                done = False
                
                while not done :
                    opt = utils.print_option_menu(6)

                    if opt == 'done' :
                        break

                    delay = []
                    v = self.doze[opt + 'x']
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    plt.plot(delay, label=opt + 'x')
                    print (delay)
                    plt.title('Delay')
                    plt.xlabel('Times raffled')
                    plt.ylabel('Delay between raffles')
                    plt.legend()
                    plt.show()

            elif cmd == 'freq' :
                done = False
                
                while not done :
                    opt = utils.print_option_menu(6)
                
                    if opt == 'done' :
                        break

                    delay = []
                    v = self.doze[opt + 'x']
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    delay.sort()
                    plt.plot(delay, label=opt + 'x')
                    print (delay)
                    plt.title('Delay')
                    plt.xlabel('Times raffled')
                    plt.ylabel('Delay between raffles')
                    plt.legend()
                    plt.show()

            elif cmd == 'done' :
                done = True
            else :
                print ("I don't understand the command " + cmd)

    def plot_rule (self):
        """
        """
        done = False
        
        while not done :
            cmd = utils.print_second_menu()
        
            if cmd == 'pie' :
                #Pie chart
                vals = []
                keys = []
                for i, k in enumerate(self.even_odd):
                    vals.append(len(self.even_odd[k]))
                    keys.append(k)

                plt.figure(figsize=(6,6))
                plt.pie(vals, labels=keys, autopct='%1.1f%%')
                plt.show()

            elif cmd == 'line' :
                vals = []
                keys = []
                dic = {}
                for k, v in self.even_odd.items():
                    dic[k] = len(v)
                sorted_list = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
                for each in sorted_list:
                    (k, v) = each
                    vals.append(v)
                    keys.append(k)

                plt.plot(vals)
                plt.xticks(np.arange(len(keys)), keys)
                plt.show()

            elif cmd == 'bar' :
                for i, k in enumerate(self.even_odd):
                    plt.bar(i, len(self.even_odd[k]))

                plt.xticks(np.arange(len(self.even_odd)) + 0.4, self.even_odd.keys())
                plt.show()

            elif cmd == 'delay' :
                done = False
                dic = {'1' : 'e0xo15',
                       '2' : 'e1xo14', 
                       '3' : 'e2xo13', 
                       '4' : 'e3xo12', 
                       '5' : 'e4xo11',
                       '6' : 'e5xo10',
                       '7' : 'e6xo9', 
                       '8' : 'e7xo8', 
                       '9' : 'e8xo7', 
                       '10': 'e9xo6', 
                       '11' : 'e10xo5',
                       '12' : 'e11xo4',
                       '13' : 'e12xo3',
                       '14' : 'e13xo2',
                       '15' : 'e14xo1',
                       '16' : 'e15xo0'}
                
                while not done :
                
                    print ('')
                    print ('\033[92m' + "Choose the rule option:" + '\033[0m')
                    print ('1 - e0xo15')
                    print ('2 - e1xo14')
                    print ('3 - e2xo13')
                    print ('4 - e3xo12')
                    print ('5 - e4xo11')
                    print ('6 - e5xo10')
                    print ('7 - e6xo9')
                    print ('8 - e7xo8')
                    print ('9 - e8xo7')
                    print ('10 - e9xo6')
                    print ('11 - e10xo5')
                    print ('12 - e11xo4')
                    print ('13 - e12xo3')
                    print ('14 - e13xo2')
                    print ('15 - e14xo1')
                    print ('16 - e15xo0')
                    print ("done  : exit the program")
                    print ('')
                    cmd = raw_input('\033[92m' + 'Enter your option (or done): ' + '\033[0m')
                    print ('')

                    if cmd == 'done' :
                        break

                    delay = []
                    v = self.even_odd[dic[cmd]]
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    plt.plot(delay, label=dic[cmd])
                    print (delay)
                    plt.title('Delay')
                    plt.xlabel('Times raffled')
                    plt.ylabel('Delay between raffles')
                    plt.legend()
                    plt.show()

            elif cmd == 'freq' :
                done = False
                dic = {'1' : 'e0xo15',
                       '2' : 'e1xo14', 
                       '3' : 'e2xo13', 
                       '4' : 'e3xo12', 
                       '5' : 'e4xo11',
                       '6' : 'e5xo10',
                       '7' : 'e6xo9', 
                       '8' : 'e7xo8', 
                       '9' : 'e8xo7', 
                       '10': 'e9xo6', 
                       '11' : 'e10xo5',
                       '12' : 'e11xo4',
                       '13' : 'e12xo3',
                       '14' : 'e13xo2',
                       '15' : 'e14xo1',
                       '16' : 'e15xo0'}
                
                while not done :
                
                    print ('')
                    print ('\033[92m' + "Choose the rule option:" + '\033[0m')
                    print ('')
                    print ('1 - e0xo15')
                    print ('2 - e1xo14')
                    print ('3 - e2xo13')
                    print ('4 - e3xo12')
                    print ('5 - e4xo11')
                    print ('6 - e5xo10')
                    print ('7 - e6xo9')
                    print ('8 - e7xo8')
                    print ('9 - e8xo7')
                    print ('10 - e9xo6')
                    print ('11 - e10xo5')
                    print ('12 - e11xo4')
                    print ('13 - e12xo3')
                    print ('14 - e13xo2')
                    print ('15 - e14xo1')
                    print ('16 - e15xo0')
                    print ("done  : exit the program")
                    print ('')
                    cmd = raw_input('\033[92m' + 'Enter your option (or done): ' + '\033[0m')
                    print ('')

                    if cmd == 'done' :
                        break

                    delay = []
                    v = self.even_odd[dic[cmd]]
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    delay.sort()
                    plt.plot(delay, label=dic[cmd])
                    print (delay)
                    plt.title('Delay')
                    plt.xlabel('Times raffled')
                    plt.ylabel('Delay between raffles')
                    plt.legend()
                    plt.show()

            elif cmd == 'done' :
                done = True
            else :
                print ("I don't understand the command " + cmd)

    ##### Methods for Computing #####
    def rule_even_by_odd(self):
        """
        """
        for each in self.all_content:
            even = 0
            odd = 0
            for el in each["Dozens"]:
                if utils.isodd(int(el)):
                    odd += 1
                else:
                    even += 1

            if even == 0 and odd == 15:
                self.even_odd["e0xo15"].append(int(each['Number']))
            elif even == 1 and odd == 14:
                self.even_odd["e1xo14"].append(int(each['Number'])) 
            elif even == 2 and odd == 13:
                self.even_odd["e2xo13"].append(int(each['Number'])) 
            elif even == 3 and odd == 12:
                self.even_odd["e3xo12"].append(int(each['Number'])) 
            elif even == 4 and odd == 11:
                self.even_odd["e4xo11"].append(int(each['Number'])) 
            elif even == 5 and odd == 10:
                self.even_odd["e5xo10"].append(int(each['Number'])) 
            elif even == 6 and odd == 9:
                self.even_odd["e6xo9"].append(int(each['Number'])) 
            elif even == 7 and odd == 8:
                self.even_odd["e7xo8"].append(int(each['Number'])) 
            elif even == 8 and odd == 7:
                self.even_odd["e8xo7"].append(int(each['Number'])) 
            elif even == 9 and odd == 6:
                self.even_odd["e9xo6"].append(int(each['Number'])) 
            elif even == 10 and odd == 5:
                self.even_odd["e10xo5"].append(int(each['Number'])) 
            elif even == 11 and odd == 4:
                self.even_odd["e11xo4"].append(int(each['Number'])) 
            elif even == 12 and odd == 3:
                self.even_odd["e12xo3"].append(int(each['Number'])) 
            elif even == 13 and odd == 2:
                self.even_odd["e13xo2"].append(int(each['Number'])) 
            elif even == 14 and odd == 1:
                self.even_odd["e14xo1"].append(int(each['Number'])) 
            elif even == 15 and odd == 0:
                self.even_odd["e15xo0"].append(int(each['Number'])) 

    def more_often_dozen (self):
        """
        """
        for each in self.all_content:
            d = 0
            for el in each['Dozens']:
                d = utils.dozen(int(el))

                if d == 0:
                    self.doze['0x'].append(int(each['Number']))
                elif d == 1:       
                    self.doze['1x'].append(int(each['Number']))
                elif d == 2:       
                    self.doze['2x'].append(int(each['Number']))

if __name__ == '__main__':
    print('O arquivo agora é lotto.py')
