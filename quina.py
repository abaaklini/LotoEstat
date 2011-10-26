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
        - create unit test;
        - clean up the ParserPage class, striping the methods that dont belog to it;
        - create package;
        - create a Mercurial repository;
        - adapt to Mega-Sena
        - adapt to Dupla-Sena
        - adapt to Lotomania
        - adapt to Lotofacil
        - store database in a pickle file or JSON file;
        - standardize names like Python Style Standard (PEP8?)
        - group common code in functions;
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


class ParsePage(HTMLParser): 

    def __init__(self):
        HTMLParser.__init__(self)
        self.inside_td = False
        self.counter = 0
        self.raffle = {"Number": 0, "Date": "00/00/00",  "Dozens": [], "Accumulated": 'Não'}
        self.all_content = []
        self.key = {"Number": 0, "Date": 1, "Dozens": 2, "Accumulated": 14}

    def handle_starttag(self, tag, attrs):  
        if tag == 'td':
            self.inside_td = True

    def handle_endtag(self, tag): 
        if tag == 'td':
            self.counter += 1
            self.inside_td = False
        elif tag == 'tr' and self.counter != 0:
            self.counter = 0
            self.raffle["Dozens"].sort()
            self.all_content.append(dict(self.raffle))
            self.raffle["Dozens"] = []

    def handle_data(self, data): 
        if self.inside_td and data:
            if self.counter in range(2, 7):
                self.raffle["Dozens"].append(data)
            elif self.counter == self.key["Number"]:
                self.raffle["Number"] = data
            elif self.counter == self.key["Accumulated"]:
                self.raffle["Accumulated"] = data
            elif self.counter == self.key["Date"]:
                self.raffle["Date"] = data

    def full_data (self):
        for el in self.all_content:
            print (el)
    
    def more_often_num(self, interf=True):

        more_often = {}
        for each in self.all_content:
            for el in each["Dozens"]:
                if more_often.__contains__(el):
                    more_often[el] += 1
                else:
                    more_often[el] = 1

        ind = -1
        for el in more_often:
            ind += 1
            num = el
            reverted_list = self.all_content
            reverted_list.reverse()
            count = 0
            for rev_el in reverted_list:
                if num in rev_el["Dozens"]:
                    more_often[el] = (more_often[el],count)
                    break
                else:
                    count += 1

        sorted_dict = sorted(more_often.items(), key=operator.itemgetter(1), reverse=True)

        if not interf:
            return (more_often)

        for el in sorted_dict:
            print(el)

    def most_delay(self, interf=True):

        more_often = {}
        for num in range(1,81):
            if num < 10:
                el = '0' + str(num)
            else:
                el = str(num)
            more_often[el] = {"Count": 0, "Average": 0, "Worst": 0, "Parts": 0}

        for each in self.all_content:
            for num in range(1,81):
                if num < 10:
                    el = '0' + str(num)
                else:
                    el = str(num)

                if el in each["Dozens"]:
                    more_often[el]["Average"] +=  more_often[el]["Count"]
                    more_often[el]["Parts"] += 1
                    if more_often[el]["Count"] > more_often[el]["Worst"]:
                        more_often[el]["Worst"] = more_often[el]["Count"]
                    more_often[el]["Count"] = 0
                else:
                    more_often[el]["Count"] += 1

        if not interf:
            return (more_often)

        for el in more_often:
            print ('[' + el + ':', end=' ')
            print ("Average :" + str(round(more_often[el]["Average"]/more_often[el]["Parts"])), end=' ')
            print ("Worst :" + str(more_often[el]["Worst"]), end=' ')
            print (']')

    def rule_3_by_2(self, interf=True):

        even_odd = {"e0xo5": 0, "e1xo4": 0, "e2xo3": 0, "e3xo2": 0, "e4xo1": 0, "e5xo0": 0}
        total = 0
        for each in self.all_content:
            total += 1
            even = 0
            odd = 0
            for el in each["Dozens"]:
                if isodd(int(el)):
                    odd += 1
                else:
                    even += 1
            if even == 0 and odd == 5:
                even_odd["e0xo5"] += 1
            elif even == 1 and odd == 4:
                even_odd["e1xo4"] += 1
            elif even == 2 and odd == 3:
                even_odd["e2xo3"] += 1
            elif even == 3 and odd == 2:
                even_odd["e3xo2"] += 1
            elif even == 4 and odd == 1:
                even_odd["e4xo1"] += 1
            elif even == 5 and odd == 0:
                even_odd["e5xo0"] += 1

        sorted_dict = sorted(even_odd.items(), key=operator.itemgetter(1), reverse=True)

        if not interf:
            return (even_odd)

        for el in sorted_dict:
            print(el) 

        print('Total Raffles: ' + str(total))

    def more_often_dozen (self, interf=True):

        doze = {"0x": 0, "1x": 0, "2x": 0, "3x": 0, "4x": 0, "5x": 0, "6x": 0, "7x": 0, "8x": 0}
        total = 0
        for each in self.all_content:
            total += 1
            d = 0
            for el in each["Dozens"]:
                d = dozen(int(el))

                if d == 0:
                    doze["0x"] += 1
                elif d == 1:
                    doze["1x"] += 1
                elif d == 2:
                    doze["2x"] += 1
                elif d == 3:
                    doze["3x"] += 1
                elif d == 4:
                    doze["4x"] += 1
                elif d == 5:
                    doze["5x"] += 1
                elif d == 6:
                    doze["6x"] += 1
                elif d == 7:
                    doze["7x"] += 1
                elif d == 8:
                    doze["8x"] += 10 #Value modified due lack of dozens

        sorted_dict = sorted(doze.items(), key=operator.itemgetter(1), reverse=True)

        if not interf:
            return (doze)

        for el in sorted_dict:
            print(el) 

        print('Total Dozens: ' + str(total*5))

    def more_often_unit (self, interf=True):

        unit = {"x0": 0, "x1": 0, "x2": 0, "x3": 0, "x4": 0, "x5": 0, "x6": 0, "x7": 0, "x8": 0, "x9": 0}
        total = 0
        for each in self.all_content:
            total += 1
            d = 0
            for el in each["Dozens"]:
                u = ret_unit(int(el))

                if u == 0:
                    unit["x0"] += 1
                elif u == 1:
                    unit["x1"] += 1
                elif u == 2:
                    unit["x2"] += 1
                elif u == 3:
                    unit["x3"] += 1
                elif u == 4:
                    unit["x4"] += 1
                elif u == 5:
                    unit["x5"] += 1
                elif u == 6:
                    unit["x6"] += 1
                elif u == 7:
                    unit["x7"] += 1
                elif u == 8:
                    unit["x8"] += 1
                elif u == 9:
                    unit["x9"] += 1

        sorted_dict = sorted(unit.items(), key=operator.itemgetter(1), reverse=True)

        if not interf:
            return (unit)

        for el in sorted_dict:
            print(el) 

        print('Total Dozens: ' + str(total*5))

    def suggest_num(self, more_recently=True):

        more_often = self.more_often_num(interf=False)
        rule = self.rule_3_by_2(interf=False)
        dozen_dict = self.more_often_dozen(interf=False)
        unit_dict = self.more_often_unit(interf=False)

        result = {}
        for el in more_often:
            if more_recently:
                result[el] = more_often[el][0]*2 - more_often[el][1]# Weight 2
            else:
                result[el] = more_often[el][0]*2 + more_often[el][1]# Weight 2

        st = 'x'
        for el in result:
            doz = dozen(int(el))
            result[el] += dozen_dict[str(doz)+st]/2 #Weight 1/2

        for el in result:
            uni = ret_unit(int(el))
            result[el] += unit_dict[st+str(uni)]/2 #Weight 1/2

        print('##################### MORE OFTEN #####################')
        sorted_dict = sorted(more_often.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_dict)
        print('################## MORE OFTEN DOZENS #####################')
        sorted_dict = sorted(dozen_dict.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_dict)
        print('################## MORE OFTEN UNITS #####################')
        sorted_dict = sorted(unit_dict.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_dict)
        print('################# SUGGESTED NUMBERS #####################')
        sorted_dict = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_dict)

    def screen_interf (self):
        done = False
        
        while not done :
        
            cmd = input("Enter a command (or help): ")

            if cmd == "help" :
                print ("The following commands are available: ")
                print ("show : show all data in memory.")
                print ("rule : show the most common combination of even and odds")
                print ("doze : show the most common dozens over all raffles")
                print ("unit : show the most common units over all raffles")
                print ("more : show the numbers more often arises.")
                print ("look : look up for a given group of 5 dozens.")
                print ("sugm : Suggest the numbers with best statistics and arises more recently")
                print ("sugl : Suggest the numbers with best statistics and arises less recently")
                print ("dlay : show the worst delay between raffles")
                print ("help : show the command list")
                print ("done : exit the program")
        
            elif cmd == "more":
                self.more_often_num()

            elif cmd == "show" :
                self.full_data()
    
            elif cmd == "rule":
                self.rule_3_by_2()

            elif cmd == "doze":
                self.more_often_dozen()

            elif cmd == "unit":
                self.more_often_unit()

            elif cmd == "look" :
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

            elif cmd == "sugm":
                self.suggest_num()

            elif cmd == "sugl":
                self.suggest_num(more_recently=False)

            elif cmd == "dlay":
                self.most_delay()

            elif cmd == "done" :
                done = True
        
            else :
                print ("I don't understand the command " + cmd)
    
def ret_unit(num):
    return round((num/10)%1*10)

def dozen(num):
    return int((num/10)//1)

def isodd(num):
            return num & 1 and True or False

def get_content ():
    """
    """
    try:
        with open('D_QUINA.HTM', encoding='latin-1') as data:
            return (data.read())
    
    except IOError as err:
        print ("File error: " + str(err))

def teste ():
    
    p = ParsePage() 
    p.feed(get_content())
    p.screen_interf()

if __name__ == '__main__': teste()


