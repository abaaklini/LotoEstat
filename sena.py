#! /usr/bin/python
# -*- coding: iso-8859-15 -*-

from lottery import Lottery
import pdb
import os
import pickle
import utils
from parsepage import ParsePage
import operator

class SenaStats (Lottery):
    """
    """
    def __init__(self, data_file):
        """
        """
        self.num_dozens = 60
        self.doz_by_raffle = 6

        Lottery.__init__(self)
        if os.path.exists('sena.pickle'):
            if os.path.getmtime('sena.pickle') > os.path.getmtime(data_file):
                try:
                    with open('sena.pickle', 'rb') as data_bin:
                        self.all_content = pickle.load(data_bin)

                except IOError as err:
                    print ("File error: " + str(err))
        else:
            p = ParsePage(self.doz_by_raffle) 
            p.feed(utils.get_content(data_file))
            self.all_content = p.get_full_data()
            try:
                with open('sena.pickle', 'wb') as data_bin:
                    pickle.dump(self.all_content, data_bin)

            except IOError as err:
                print ("File error: " + str(err))

        self.init_stat_table()
        self.even_odd = {"e0xo6": [], "e1xo5": [], "e2xo4": [], "e3xo3": [], "e4xo2": [], "e5xo1": [], "e6xo0": []}
        self.doze = {"0x": [], "1x": [], "2x": [], "3x": [], "4x": [], "5x": [], "6x": []}
        self.more_often_num()
        self.last_time()
        self.most_delay()
        self.rule_even_by_odd()
        self.more_often_dozen()
        self.more_often_unit()

    def print_rule_even_by_odd(self):
        """
        """
        di = {'e0xo6': len(self.even_odd['e0xo6']),
              'e1xo5': len(self.even_odd['e1xo5']),
              'e2xo4': len(self.even_odd['e2xo4']),
              'e3xo3': len(self.even_odd['e3xo3']),
              'e4xo2': len(self.even_odd['e4xo2']),
              'e5xo1': len(self.even_odd['e5xo1']),
              'e6xo0': len(self.even_odd['e6xo0'])}

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        for each in sorted_list:
            print(each)

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

            if even == 0 and odd == 6:
                self.even_odd["e0xo6"].append(int(each['Number']))
            elif even == 1 and odd == 5:
                self.even_odd["e1xo5"].append(int(each['Number'])) 
            elif even == 2 and odd == 4:
                self.even_odd["e2xo4"].append(int(each['Number'])) 
            elif even == 3 and odd == 3:
                self.even_odd["e3xo3"].append(int(each['Number'])) 
            elif even == 4 and odd == 2:
                self.even_odd["e4xo2"].append(int(each['Number'])) 
            elif even == 5 and odd == 1:
                self.even_odd["e5xo1"].append(int(each['Number'])) 
            elif even == 6 and odd == 0:
                self.even_odd["e6xo0"].append(int(each['Number'])) 


    def print_more_often_dozen (self):
        """
        """
        di = {'0x': len(self.doze['0x']),
              '1x': len(self.doze['1x']),
              '2x': len(self.doze['2x']),
              '3x': len(self.doze['3x']),
              '4x': len(self.doze['4x']),
              '5x': len(self.doze['5x']),
              '6x': len(self.doze['6x'])}

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        for each in sorted_list:
            print(each)

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
                elif d == 3:       
                    self.doze['3x'].append(int(each['Number']))
                elif d == 4:       
                    self.doze['4x'].append(int(each['Number']))
                elif d == 5:       
                    self.doze['5x'].append(int(each['Number']))
                elif d == 6:       
                    self.doze['6x'].append(int(each['Number']))

if __name__ == '__main__':
    print('O arquivo agora é lotto.py')
