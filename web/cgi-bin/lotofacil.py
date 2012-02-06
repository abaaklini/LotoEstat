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
from time import ctime

class LotoFacilStats (Lottery):
    """
    """
    def __init__(self, data_file, sub_table = 0):
        """
        """
        self.num_dozens = 25
        self.doz_by_raffle =15 
        self.updated = ctime(os.path.getmtime(data_file))

        Lottery.__init__(self)
        if os.path.exists('data/facil.pickle'):
            self.updated = os.path.getmtime(data_file)
            if os.path.getmtime('data/facil.pickle') > os.path.getmtime(data_file):
                try:
                    data_bin = open('../data/facil.pickle', 'rb')
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
                data_bin = open('../data/facil.pickle', 'wb')
                pickle.dump(self.all_content, data_bin)

            except IOError, err:
                print ("File error: " + str(err))
            else:
                data_bin.close()

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
    def print_more_often_dozen (self, for_print=True):
        """
        """
        di = {'0x': len(self.doze['0x']),
              '1x': len(self.doze['1x']),
              '2x': len(self.doze['2x']) * 6.0/10}

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        if for_print:
            for each in sorted_list:
                print(each)
        else:
            return sorted_list

    def print_rule_even_by_odd(self, for_print=True):
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
        if for_print:
            for each in sorted_list:
                print(each)
        else:
            return sorted_list

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
