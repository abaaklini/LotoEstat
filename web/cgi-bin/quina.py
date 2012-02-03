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

from lottery import Lottery
import pdb
import os
import pickle
import utils
from parsepage import ParsePage
import operator

class QuinaStats (Lottery):
    """
    """
    def __init__(self, data_file, sub_table = 0):
        """
        """
        self.num_dozens = 80
        self.doz_by_raffle = 5

        Lottery.__init__(self)
        if os.path.exists('data/quina.pickle'):
            if os.path.getmtime('data/quina.pickle') > os.path.getmtime(data_file):
                try:
                    data_bin = open('data/quina.pickle', 'rb')
                    self.all_content = pickle.load(data_bin)
                    if sub_table > 0:
                            self.all_content = self.all_content[:sub_table]
                except IOError, err:
                    print ("File error: " + str(err))
                else:
                    data_bin.close()

        else:
            p = ParsePage(self.doz_by_raffle) 
            p.feed(utils.get_content(data_file))
            self.all_content = p.get_full_data()
            if sub_table > 0:
                self.all_content = self.all_content[:sub_table]
            try:
                data_bin = open('../data/quina.pickle', 'wb')
                pickle.dump(self.all_content, data_bin)
            except IOError, err:
                print ("File error: " + str(err))
            else:
                data_bin.close()

        self.init_stat_table()
        self.even_odd = {"e0xo5": [], "e1xo4": [], "e2xo3": [], "e3xo2": [], "e4xo1": [], "e5xo0": []}
        self.doze = {"0x": [], "1x": [], "2x": [], "3x": [], "4x": [], "5x": [], "6x": [], "7x": [], "8x": []}
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
    def print_more_often_dozen (self, for_print=True):
        """
        """
        di = {'0x': len(self.doze['0x']),
              '1x': len(self.doze['1x']),
              '2x': len(self.doze['2x']),
              '3x': len(self.doze['3x']),
              '4x': len(self.doze['4x']),
              '5x': len(self.doze['5x']),
              '6x': len(self.doze['6x']),
              '7x': len(self.doze['7x']),
              '8x': len(self.doze['8x']) * 10}

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        if for_print:
            print(sorted_list)
        else:
            return sorted_list

    def print_rule_even_by_odd(self, for_print=True):
        """
        """
        di = {'e0xo5': len(self.even_odd['e0xo5']),
              'e1xo4': len(self.even_odd['e1xo4']),
              'e2xo3': len(self.even_odd['e2xo3']),
              'e3xo2': len(self.even_odd['e3xo2']),
              'e4xo1': len(self.even_odd['e4xo1']),
              'e5xo0': len(self.even_odd['e5xo0'])}

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        if for_print:
            for each in sorted_list:
                print(each)
        else:
            return sorted_list

    ##### Methods for Computing #####
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
                elif d == 7:       
                    self.doze['7x'].append(int(each['Number']))
                elif d == 8:       
                    self.doze['8x'].append(int(each['Number']))

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

            if even == 0 and odd == 5:
                self.even_odd["e0xo5"].append(int(each['Number']))
            elif even == 1 and odd == 4:
                self.even_odd["e1xo4"].append(int(each['Number'])) 
            elif even == 2 and odd == 3:
                self.even_odd["e2xo3"].append(int(each['Number'])) 
            elif even == 3 and odd == 2:
                self.even_odd["e3xo2"].append(int(each['Number'])) 
            elif even == 4 and odd == 1:
                self.even_odd["e4xo1"].append(int(each['Number'])) 
            elif even == 5 and odd == 0:
                self.even_odd["e5xo0"].append(int(each['Number'])) 

def _test():
    pass

if __name__ == '__main__': _test()
