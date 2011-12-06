#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
    TODO: 
"""
from __future__ import print_function
import operator
import matplotlib.pyplot as plt
import utils
import pdb
import numpy as np

class Lottery ():
    """
    """
    def __init__(self):
        """
        """
        self.all_stat = []
        self.even_odd = {}
        self.doze = {}
        self.unit = {"x0": [], "x1": [], "x2": [], "x3": [], "x4": [], "x5": [], "x6": [], "x7": [], "x8": [], "x9": []}

    def init_stat_table(self):
        """
        """
        for num in range(1, self.num_dozens + 1):
            self.all_stat.append({"More": 0, "Last": 0, "Average": 0, "Worst": 0, "Occur": []})

    def prepare_to_print(self, key):
        """
        """
        di ={} 
        for ind, val in enumerate(self.all_stat):
            num = ind + 1
            if num < 10:
                el = '0' + str(num)
            else:
                el = str(num)
            di[str(el)] = val[key]

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_list)

    def print_full_data(self):
        """
        """
        for el in self.all_content:
            print(el)
        #    for k, v in el.items():
        #        print(k + ':' + repr(v))

    def plot_more_often(self):
        """
        """
        num = int(raw_input('\033[92m' + 'Enter a number to plot (or 0 for none): ' + '\033[0m'))
        if num == 0:
            return

        delay = []
        aver = []
        value = self.all_stat[num - 1]['Occur']
        for ind in range(len(value) - 1):
            delay.append(value[ind + 1] - value[ind])
            aver.append(self.all_stat[num - 1]['Average'])

        plt.plot(delay, label='Delay')
        plt.plot(aver, label='Average') 
        plt.title('Delay for number ' + str(num))
        plt.xlabel('Times raffled')
        plt.ylabel('Delay between raffles')
        plt.legend()
        plt.show()

    def more_often_num(self):
        """
        """
        for each in self.all_content:
            for el in each["Dozens"]:
                self.all_stat[int(el) - 1]['Occur'].append(int(each['Number']))

        for ind, val in enumerate(self.all_stat):
            val['More'] = len(val['Occur'])

    def last_time(self):
        """
        """
        for ind, val in enumerate(self.all_stat):
            val['Last'] = int(self.all_content[-1]['Number']) - val['Occur'][-1]

    def most_delay(self):
        """
        """
        for el in self.all_stat:
            dic = {'Delay':[]}
            for val in range(1, len(el['Occur'])):
                dic['Delay'].append( el['Occur'][val] - el['Occur'][val - 1] - 1)

            el['Worst'] = max(dic['Delay'])
            el['Average'] = sum(dic['Delay'])/len(dic['Delay'])


    def plot_unit (self):
        """
        """
        done = False
        
        while not done :
        
            print ('')
            print ('\033[92m' + "The following commands are available: " + '\033[0m')
            print ('')
            print ("pie   : show the data plotted on a pie chart")
            print ("bar   : show the data plotted on a bar chart")
            print ("line  : show the data plotted on a line chart")
            print ("delay : show the delay over the raffles, plus the average delay")
            print ("freq  : show the frequency of delays")
            print ("done  : exit the program")
            print ('')
            cmd = raw_input('\033[92m' + 'Enter a command: ' + '\033[0m')
            print ('')

            if cmd == 'pie' :
                #Pie chart
                vals = []
                keys = []
                for i, k in enumerate(self.unit):
                    vals.append(len(self.unit[k]))
                    keys.append(k)

                plt.figure(figsize=(6,6))
                plt.pie(vals, labels=keys, autopct='%1.1f%%')
                plt.show()

            elif cmd == 'line' :
                vals = []
                keys = []
                dic = {}
                for k, v in self.unit.items():
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
                for i, k in enumerate(self.unit):
                    plt.bar(i, len(self.unit[k]))

                plt.xticks(np.arange(len(self.unit)) + 0.4, self.unit.keys())
                plt.show()

            elif cmd == 'delay' :
                done = False
                
                while not done :
                
                    print ('')
                    print ('\033[92m' + "Choose the unit number:" + '\033[0m')
                    print ('')
                    print ("0", end='\t')
                    print ("1")
                    print ("2", end='\t')
                    print ("3")
                    print ("4", end='\t')
                    print ("5")
                    print ("6", end='\t')
                    print ("7")
                    print ("8", end='\t')
                    print ("9")
                    print ("done  : exit the program")
                    print ('')
                    cmd = raw_input('\033[92m' + 'Enter a unit (or done): ' + '\033[0m')
                    print ('')

                    if cmd == 'done' :
                        break

                    delay = []
                    v = self.unit['x' + cmd]
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    plt.plot(delay, label='x' + cmd)
                    print (delay)
                    plt.title('Delay')
                    plt.xlabel('Times raffled')
                    plt.ylabel('Delay between raffles')
                    plt.legend()
                    plt.show()

            elif cmd == 'freq' :
                done = False
                
                while not done :
                
                    print ('')
                    print ('\033[92m' + "Choose the unit number:" + '\033[0m')
                    print ('')
                    print ("0", end='\t')
                    print ("1")
                    print ("2", end='\t')
                    print ("3")
                    print ("4", end='\t')
                    print ("5")
                    print ("6", end='\t')
                    print ("7")
                    print ("8", end='\t')
                    print ("9")
                    print ("done  : exit the program")
                    print ('')
                    cmd = raw_input('\033[92m' + 'Enter a unit (or done): ' + '\033[0m')
                    print ('')

                    if cmd == 'done' :
                        break

                    delay = []
                    v = self.unit['x' + cmd]
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    delay.sort()
                    plt.plot(delay, label='x' + cmd)
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

    def print_more_often_unit (self):
        """
        """
        di = {'x0': len(self.unit['x0']),
              'x1': len(self.unit['x1']),
              'x2': len(self.unit['x2']),
              'x3': len(self.unit['x3']),
              'x4': len(self.unit['x4']),
              'x5': len(self.unit['x5']),
              'x6': len(self.unit['x6']),
              'x7': len(self.unit['x7']),
              'x8': len(self.unit['x8']),
              'x9': len(self.unit['x9'])}

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        for each in sorted_list:
            print(each)

    def more_often_unit (self):
        """
        """
        for each in self.all_content:
            d = 0
            for el in each['Dozens']:
                u = utils.ret_unit(int(el))

                if u == 0:
                    self.unit['x0'].append(int(each['Number']))
                elif u == 1:                                  
                    self.unit['x1'].append(int(each['Number']))
                elif u == 2:                                  
                    self.unit['x2'].append(int(each['Number']))
                elif u == 3:                                  
                    self.unit['x3'].append(int(each['Number']))
                elif u == 4:                                  
                    self.unit['x4'].append(int(each['Number']))
                elif u == 5:                                  
                    self.unit['x5'].append(int(each['Number']))
                elif u == 6:                                  
                    self.unit['x6'].append(int(each['Number']))
                elif u == 7:                                  
                    self.unit['x7'].append(int(each['Number']))
                elif u == 8:                                  
                    self.unit['x8'].append(int(each['Number']))
                elif u == 9:       
                    self.unit['x9'].append(int(each['Number']))

    def suggest_num(self, more_recently=True):
        """
        """

        result = {}
        st = 'x'
        for ind, val in enumerate(self.all_stat):
            num = ind + 1
            if num < 10:
                el = '0' + str(num)
            else:
                el = str(num)

            if more_recently:
                result[el] = val['More']*2 - val['Last'] # Weight 2
            else:
                result[el] = val['More']*2 + val['Last'] # Weight 2

            doz = utils.dozen(num)
            result[el] += len(self.doze[str(doz)+st])/2 #Weight 1/2

            uni = utils.ret_unit(num)
            result[el] += len(self.unit[st+str(uni)])/2 #Weight 1/2

        print('##################### MORE OFTEN #####################')
        self.prepare_to_print('More')
        print('################## MORE OFTEN DOZENS #####################')
        self.print_more_often_dozen()
        print('################## MORE OFTEN UNITS #####################')
        self.print_more_often_unit()
        print('################# SUGGESTED NUMBERS #####################')
        sorted_list = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_list)

    def look_up_num(self):
        """
        """
        print ('Enter with ' + str(self.doz_by_raffle) + ' numbers:')
        dozens = []
        for el in range(self.doz_by_raffle):
            num = raw_input('Dozen number ' + str(el + 1) + ':')
            if int(num) < 10 and len(num) < 2:
                num = '0' + str(num)
            else:
                num = str(num)
            dozens.append(num)
        dozens.sort()

        founded = False
        for each in self.all_content:
            if dozens == each["Dozens"]:
                founded = True
                print ('')
                print ('\033[92m' + 'Dozens founded :' + '\033[0m')
                print ('Date : ' + each['Date'])
                print ('Accumulated : ' + each['Accumulated'])

        if not founded:
            # TODO: Test the numbers with/against the statistics
            print ('Dozens not founded')

    def screen_interf (self):
        """
        """
        done = False
        
        while not done :
        
            print ('')
            print ('\033[92m' + "The following commands are available: " + '\033[0m')
            print ('')
            print ("aver : show the average delay between raffles")
            print ("done : exit the program")
            print ("doze : show the most common dozens over all raffles")
            print ("last : show the last time a numbers arises.")
            print ("look : look up for a given group of 5 dozens.")
            print ("more : show the numbers more often arises.")
            print ("occu : print the list of occurrence of a number during the raffles.")
            print ("rule : show the most common combination of even and odds")
            print ("show : show all data in memory.")
            print ("sugl : Suggest the numbers with best statistics and arises less recently")
            print ("sugm : Suggest the numbers with best statistics and arises more recently")
            print ("unit : show the most common units over all raffles")
            print ("wors : show the worst delay between raffles")
            print ('')
            cmd = raw_input('\033[92m' + 'Enter a command: ' + '\033[0m')
            print ('')

            if cmd == 'more' :
                self.prepare_to_print('More')
                self.plot_more_often()

            elif cmd == 'last' :
                self.prepare_to_print('Last')

            elif cmd == 'aver' :
                self.prepare_to_print('Average')

            elif cmd == 'wors' :
                self.prepare_to_print('Worst')

            elif cmd == 'show' :
                self.print_full_data()
    
            elif cmd == 'rule' :
                self.print_rule_even_by_odd()
                self.plot_rule()

            elif cmd == 'doze' :
                self.print_more_often_dozen()
                self.plot_doze()

            elif cmd == 'unit' :
                self.print_more_often_unit()
                self.plot_unit()

            elif cmd == 'look' :
                self.look_up_num()

            elif cmd == 'sugm' :
                self.suggest_num()

            elif cmd == 'sugl' :
                self.suggest_num(more_recently=False)

            elif cmd == 'occu' :
                self.prepare_to_print('Occur')

            elif cmd == 'done' :
                done = True

            elif cmd == 'test' :
                print('#### MORE ####')
                self.prepare_to_print('More')
                print('#### LAST ####')
                self.prepare_to_print('Last')
                print('#### DELAY AVERAGE####')
                self.prepare_to_print('Average')
                print('#### WORST DELAY ####')
                self.prepare_to_print('Worst')
                print('#### RULE 3 by 2 ####')
                self.print_rule_even_by_odd()
                print('#### DOZE ####')
                self.print_more_often_dozen()
                print('#### UNIT ####')
                self.print_more_often_unit()
        
            else :
                print ("I don't understand the command " + cmd)
    
if __name__ == '__main__':
    print('lottery.py')
