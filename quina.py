#! /usr/bin/python3
# -*- coding: iso-8859-15 -*-
"""
    TODO: 
        - DONE store the date on database.
        - DONE show the last time a number was raffled;
        - DONE show if a group of dozens has been raffle and in which date;
        - DONE show the statistics for the 2X3 rule;
        - DONE check which frequency a dozen arise (ex. 0x, 1x, 2x, 3x, ..., 80)
        - DONE check which frequency a unit arise (ex. x0, x1, x2, x3, ..., x9))
        - DONE suggest great numbers based on this statistics
        - DONE create a local Mercurial repository on a Dropbox folder;
        - DONE clean up the ParserPage class, striping the methods that dont belog to it;
        - DONE FOR PICKLE store database in a pickle file or JSON file;
        - DONE group common code in functions;
        - NOT DONED Implement Fatorial function. Use math.factorial();
        - Choose a better structure for memory data;
        - Find the average a number arise; ("More")
        - Find the deviation by de media; ("More")
        - Positioning the number in the quartiles; ("More")
        - Find the average a number delay; ("Delay")
        - Find the deviation by de media; ("Delay")
        - Positioning the number in the quartiles; ("Delay")
        - Calculate the probabilitty of a number been raffled, based upon it's score;("Sugm/Sugl")
        - create unit test;
        - create package;
        - adapt to Mega-Sena
        - adapt to Dupla-Sena
        - adapt to Lotomania
        - adapt to Lotofacil
        - standardize names like Python Style Standard (PEP8?)
        - uses NCurses;
        - uses i18n;
        - upload to pyPI;
        - create an GUI interface;
        - adapt to an US or UK lottery;
        - make this app in a Web App;
        - make the Web App in an Android App;
        - make money with it;
"""
from html.parser import HTMLParser 
import pdb
import operator
import os
import pickle

def ret_unit(num):
    """
    """
    return round((num/10)%1*10)

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
        with open('D_QUINA.HTM', encoding='latin-1') as data:
            return (data.read())
    
    except IOError as err:
        print ("File error: " + str(err))

def test ():
    """
    """
    quina = QuinaStats()
    quina.screen_interf()

class ParsePage(HTMLParser): 
    """
    """
    def __init__(self):
        """
        """
        HTMLParser.__init__(self)
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
        self.doze = {"0x": 0, "1x": 0, "2x": 0, "3x": 0, "4x": 0, "5x": 0, "6x": 0, "7x": 0, "8x": 0}
        self.unit = {"x0": 0, "x1": 0, "x2": 0, "x3": 0, "x4": 0, "x5": 0, "x6": 0, "x7": 0, "x8": 0, "x9": 0}
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
            self.all_stat.append({"More": 0, "Last": 0, "Average": 0, "Worst": 0, "Occur": [], 'Delay': []})

    def prepare_to_print(self, key):
        """
        """
        di ={} 
        for num in range(1,81):
            if num < 10:
                el = '0' + str(num)
            else:
                el = str(num)
            di[str(el)] = self.all_stat[num - 1][key]

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_list)

    def print_full_data(self):
        """
        """
        for el in self.all_content:
            print(el)

    def print_occurency(self):
        """
        """
        di ={} 
        for num in range(1,81):
            if num < 10:
                el = '0' + str(num)
            else:
                el = str(num)
            di[str(el)] = self.all_stat[num - 1]['Occur']

        print(di)

    def print_more_often_num(self):
        """
        """
        self.prepare_to_print('More')

    def more_often_num(self):
        """
        """
        for each in self.all_content:
            for el in each["Dozens"]:
                self.all_stat[int(el) - 1]['Occur'].append(int(each['Number']))

        for num in range(1,81):
            self.all_stat[num - 1]['More'] = len(self.all_stat[num - 1]['Occur'])

    def print_last_time(self):
        """
        """
        self.prepare_to_print('Last')

    def last_time(self):
        """
        """
        for num in range(1,81):
            self.all_stat[num - 1]['Last'] = int(self.all_content[-1]['Number']) - self.all_stat[num - 1]['Occur'][-1] - 1

    def print_most_delay_average(self):
        """
        """
        self.prepare_to_print('Average')

    def print_most_delay_worst(self):
        """
        """
        self.prepare_to_print('Worst')

    def most_delay(self):
        """
        """
        for el in self.all_stat:
            for val in range(1, len(el['Occur'])):
                el['Delay'].append( el['Occur'][val] - el['Occur'][val - 1] - 1)

            el['Worst'] = max(el['Delay'])
            el['Average'] = round(sum(el['Delay'])/len(el['Delay']))
        
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

    def print_more_often_dozen (self):
        """
        """
        sorted_list = sorted(self.doze.items(), key=operator.itemgetter(1), reverse=True)
        for each in sorted_list:
            print(each)

    def more_often_dozen (self):
        """
        """
        for each in self.all_content:
            d = 0
            for el in each["Dozens"]:
                d = dozen(int(el))

                if d == 0:
                    self.doze["0x"] += 1
                elif d == 1:
                    self.doze["1x"] += 1
                elif d == 2:
                    self.doze["2x"] += 1
                elif d == 3:
                    self.doze["3x"] += 1
                elif d == 4:
                    self.doze["4x"] += 1
                elif d == 5:
                    self.doze["5x"] += 1
                elif d == 6:
                    self.doze["6x"] += 1
                elif d == 7:
                    self.doze["7x"] += 1
                elif d == 8:
                    self.doze["8x"] += 10 #Value modified due lack of dozens

    def print_more_often_unit (self):
        """
        """
        sorted_list = sorted(self.unit.items(), key=operator.itemgetter(1), reverse=True)
        for each in sorted_list:
            print(each)

    def more_often_unit (self):
        """
        """
        for each in self.all_content:
            d = 0
            for el in each["Dozens"]:
                u = ret_unit(int(el))

                if u == 0:
                    self.unit["x0"] += 1
                elif u == 1:
                    self.unit["x1"] += 1
                elif u == 2:
                    self.unit["x2"] += 1
                elif u == 3:
                    self.unit["x3"] += 1
                elif u == 4:
                    self.unit["x4"] += 1
                elif u == 5:
                    self.unit["x5"] += 1
                elif u == 6:
                    self.unit["x6"] += 1
                elif u == 7:
                    self.unit["x7"] += 1
                elif u == 8:
                    self.unit["x8"] += 1
                elif u == 9:
                    self.unit["x9"] += 1

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
            # TODO: Test the numbers with the statistics
            print ('Dozens not founded')

    def suggest_num(self, more_recently=True):
        """
        """

        result = {}
        st = 'x'
        for num in range(1,81):
            if num < 10:
                el = '0' + str(num)
            else:
                el = str(num)

            if more_recently:
                result[el] = self.all_stat[num - 1]['More']*2 - self.all_stat[num - 1]['Last'] # Weight 2
            else:
                result[el] = self.all_stat[num - 1]['More']*2 + self.all_stat[num - 1]['Last'] # Weight 2

            doz = dozen(num)
            result[el] += self.doze[str(doz)+st]/2 #Weight 1/2

            uni = ret_unit(num)
            result[el] += self.unit[st+str(uni)]/2 #Weight 1/2

        print('##################### MORE OFTEN #####################')
        self.print_more_often_num()
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
            print ("occu : print the list of occurency of a number during the raffles.")
            print ("rule : show the most common combination of even and odds")
            print ("show : show all data in memory.")
            print ("sugl : Suggest the numbers with best statistics and arises less recently")
            print ("sugm : Suggest the numbers with best statistics and arises more recently")
            print ("unit : show the most common units over all raffles")
            print ("wors : show the worst delay between raffles")
            print ('')
            cmd = input('\033[92m' + "Enter a command: " + '\033[0m')
            print ('')

            if cmd == "more":
                self.print_more_often_num()

            elif cmd == "last" :
                self.print_last_time()

            elif cmd == "aver" :
                self.print_most_delay_average()

            elif cmd == "wors" :
                self.print_most_delay_worst()

            elif cmd == "show" :
                self.print_full_data()
    
            elif cmd == "rule":
                self.print_rule_3_by_2()

            elif cmd == "doze":
                self.print_more_often_dozen()

            elif cmd == "unit":
                self.print_more_often_unit()

            elif cmd == "look" :
                self.look_up_num()

            elif cmd == "sugm":
                self.suggest_num()

            elif cmd == "sugl":
                self.suggest_num(more_recently=False)

            elif cmd == "occu" :
                self.print_occurency()

            elif cmd == "done" :
                done = True
        
            else :
                print ("I don't understand the command " + cmd)
    

if __name__ == '__main__': test()


