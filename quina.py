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
import HTMLParser 
import pdb
import operator
import os
import pickle
import matplotlib.pyplot as plt
import math
import codecs
import numpy as np

def ret_unit(num):
    """
    """
    return int(round(math.fmod((float(num)/10.0),1)*10))

def dozen(num):
    """
    """
    return int((num/10)//1)

def isodd(num):
    """
    """
    return num & 1 and True or False

def get_content ():
    """
    """
    try:
        with codecs.open('D_QUINA.HTM', 'r', 'latin-1') as data:
            return (data.read())
    
    except IOError as err:
        print ("File error: " + str(err))

def test ():
    """
    """
    quina = QuinaStats()
    quina.screen_interf()

class ParsePage(HTMLParser.HTMLParser): 
    """
    """
    def __init__(self):
        """
        """
        HTMLParser.HTMLParser.__init__(self)
        self.inside_td = False
        self.counter = 0
        self.raffle = {"Number": 0, "Date": "00/00/00",  "Dozens": [], "Accumulated": 'Não'}
        self.all_content = []
        self.key = {"Number": 0, "Date": 1, "Dozens": 2, "Accumulated": 14}

    def handle_starttag(self, tag, attrs):  
        """
        """
        if tag == 'td':
            self.inside_td = True

    def handle_endtag(self, tag): 
        """
        """
        if tag == 'td':
            self.counter += 1
            self.inside_td = False
        elif tag == 'tr' and self.counter != 0:
            self.counter = 0
            self.raffle["Dozens"].sort()
            self.all_content.append(dict(self.raffle))
            self.raffle["Dozens"] = []

    def handle_data(self, data): 
        """
        """
        if self.inside_td and data:
            if self.counter in range(2, 7):
                self.raffle["Dozens"].append(data)
            elif self.counter == self.key["Number"]:
                self.raffle["Number"] = data
            elif self.counter == self.key["Accumulated"]:
                self.raffle["Accumulated"] = data
            elif self.counter == self.key["Date"]:
                self.raffle["Date"] = data

    def get_full_data (self):
        return (self.all_content)
    
class QuinaStats ():
    """
    """
    def __init__(self):
        """
        """

        if os.path.exists('quina.pickle'):
            if os.path.getmtime('quina.pickle') > os.path.getmtime('D_QUINA.HTM'):
                try:
                    with open('quina.pickle', 'rb') as data_bin:
                        self.all_content = pickle.load(data_bin)

                except IOError as err:
                    print ("File error: " + str(err))
        else:
            p = ParsePage() 
            p.feed(get_content())
            self.all_content = p.get_full_data()
            try:
                with open('quina.pickle', 'wb') as data_bin:
                    pickle.dump(self.all_content, data_bin)

            except IOError as err:
                print ("File error: " + str(err))

        self.all_stat = []
        self.init_stat_table()
        self.even_odd = {"e0xo5": [], "e1xo4": [], "e2xo3": [], "e3xo2": [], "e4xo1": [], "e5xo0": []}
        self.doze = {"0x": [], "1x": [], "2x": [], "3x": [], "4x": [], "5x": [], "6x": [], "7x": [], "8x": []}
        self.unit = {"x0": [], "x1": [], "x2": [], "x3": [], "x4": [], "x5": [], "x6": [], "x7": [], "x8": [], "x9": []}
        self.more_often_num()
        self.last_time()
        self.most_delay()
        self.rule_3_by_2()
        self.more_often_dozen()
        self.more_often_unit()

    def init_stat_table(self):
        """
        """
        for num in range(1,81):
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
            for k, v in el.items():
                print(k + ':' + repr(v))

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
        
    def plot_rule (self):
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
            print ("month : show the times the rule appear inside a month and the average")
            print ("year  : show the times the rule appear inside an year and the average")
            print ("done  : exit the program")
            print ('')
            cmd = raw_input('\033[92m' + 'Enter a command: ' + '\033[0m')
            print ('')

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
                delay = {}
                for k, v in self.even_odd.items():
                    delay[k] = []
                    for ind in range(len(v) - 1):
                        delay[k].append(v[ind + 1] - v[ind])
                    plt.plot(delay[k], label=k)
                    plt.title('Delay')
                plt.xlabel('Times raffled')
                plt.ylabel('Delay between raffles')
                plt.legend()
                plt.show()

            elif cmd == 'month' :
                pass
            elif cmd == 'year' :
                pass
            elif cmd == 'done' :
                done = True
            else :
                print ("I don't understand the command " + cmd)

    def print_rule_3_by_2(self):
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

    def rule_3_by_2(self):
        """
        """
        for each in self.all_content:
            even = 0
            odd = 0
            for el in each["Dozens"]:
                if isodd(int(el)):
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

    def plot_doze (self):
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
            print ("month : show the times the rule appear inside a month and the average")
            print ("year  : show the times the rule appear inside an year and the average")
            print ("done  : exit the program")
            print ('')
            cmd = raw_input('\033[92m' + 'Enter a command: ' + '\033[0m')
            print ('')

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
                delay = {}
                for k, v in self.doze.items():
                    delay[k] = []
                    for ind in range(len(v) - 1):
                        delay[k].append(v[ind + 1] - v[ind])
                    plt.plot(delay[k], label=k)
                    print delay[k]
                    plt.title('Delay')
                plt.xlabel('Times raffled')
                plt.ylabel('Delay between raffles')
                plt.legend()
                plt.show()

            elif cmd == 'month' :
                pass
            elif cmd == 'year' :
                pass
            elif cmd == 'done' :
                done = True
            else :
                print ("I don't understand the command " + cmd)

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
                d = dozen(int(el))

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
            print ("month : show the times the rule appear inside a month and the average")
            print ("year  : show the times the rule appear inside an year and the average")
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
                delay = {}
                for k, v in self.unit.items():
                    delay[k] = []
                    for ind in range(len(v) - 1):
                        delay[k].append(v[ind + 1] - v[ind])
                    plt.plot(delay[k], label=k)
                    print delay[k]
                    plt.title('Delay')
                plt.xlabel('Times raffled')
                plt.ylabel('Delay between raffles')
                plt.legend()
                plt.show()

            elif cmd == 'month' :
                pass
            elif cmd == 'year' :
                pass
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
                u = ret_unit(int(el))

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

            doz = dozen(num)
            result[el] += len(self.doze[str(doz)+st])/2 #Weight 1/2

            uni = ret_unit(num)
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
                self.print_rule_3_by_2()
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
                self.print_rule_3_by_2()
                print('#### DOZE ####')
                self.print_more_often_dozen()
                print('#### UNIT ####')
                self.print_more_often_unit()
        
            else :
                print ("I don't understand the command " + cmd)
    

if __name__ == '__main__': test()


