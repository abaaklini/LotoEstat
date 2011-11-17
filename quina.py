#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
    TODO: 
        - Fix the Unicode problem on all_content
        - Find the average a number arise; ("More")
        - Find the deviation by de media; ("More")
        - Positioning the number in the quartiles; ("More")
        - Find the deviation by de media; ("Delay")
        - Positioning the number in the quartiles; ("Delay")
        - Calculate the probability of a number been raffled, based upon it's score;("Sugm/Sugl")
        - create unit test;
        - create package;
        - adapt to Mega-Sena
        - adapt to Dupla-Sena
        - adapt to Lotomania
        - adapt to Lotofacil
        - standardize names like Python Style Standard (PEP8?)
        - split the code to different files
        - uses NCurses;
        - uses i18n;
        - upload to pyPI;
        - create an GUI interface;
        - adapt to an US or UK lottery;
        - make this app in a Web App;
        - make the Web App in an Android App;
        - make money with it;
"""
from lottery import Lottery
import pdb
import os
import pickle
import matplotlib.pyplot as plt
import utils
import numpy as np
from parsepage import ParsePage
import operator

class QuinaStats (Lottery):
    """
    """
    def __init__(self, data_file):
        """
        """
        Lottery.__init__(self)
        if os.path.exists('quina.pickle'):
            if os.path.getmtime('quina.pickle') > os.path.getmtime(data_file):
                try:
                    with open('quina.pickle', 'rb') as data_bin:
                        self.all_content = pickle.load(data_bin)

                except IOError as err:
                    print ("File error: " + str(err))
        else:
            p = ParsePage() 
            p.feed(utils.get_content(data_file))
            self.all_content = p.get_full_data()
            try:
                with open('quina.pickle', 'wb') as data_bin:
                    pickle.dump(self.all_content, data_bin)

            except IOError as err:
                print ("File error: " + str(err))

        self.init_stat_table()
        self.even_odd = {"e0xo5": [], "e1xo4": [], "e2xo3": [], "e3xo2": [], "e4xo1": [], "e5xo0": []}
        self.doze = {"0x": [], "1x": [], "2x": [], "3x": [], "4x": [], "5x": [], "6x": [], "7x": [], "8x": []}
        self.more_often_num()
        self.last_time()
        self.most_delay()
        self.rule_even_by_odd()
        self.more_often_dozen()
        self.more_often_unit()

    def init_stat_table(self):
        """
        """
        for num in range(1,81):
            self.all_stat.append({"More": 0, "Last": 0, "Average": 0, "Worst": 0, "Occur": []})

    def print_rule_even_by_odd(self):
        """
        """
        di = {'e0xo5': len(self.even_odd['e0xo5']),
              'e1xo4': len(self.even_odd['e1xo4']),
              'e2xo3': len(self.even_odd['e2xo3']),
              'e3xo2': len(self.even_odd['e3xo2']),
              'e4xo1': len(self.even_odd['e4xo1']),
              'e5xo0': len(self.even_odd['e5xo0'])}

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


    def print_more_often_dozen (self):
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
              '8x': len(self.doze['8x'])}

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
                elif d == 7:       
                    self.doze['7x'].append(int(each['Number']))
                elif d == 8:       
                    self.doze['8x'].append(int(each['Number']))

    def look_up_num(self):
        """
        """
        print ('Enter with 5 numbers:')
        dozens = []
        for el in range(5):
            num = input('Dozen number ' + str(el + 1) + ':')
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
                print ('Dozens founded :')
                print ('Date : ' + each['Date'])
                print ('Accumulated : ' + each['Accumulated'])

        if not founded:
            # TODO: Test the numbers with/against the statistics
            print ('Dozens not founded')


if __name__ == '__main__':
    print('O arquivo agora é lotto.py')
