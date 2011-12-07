#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
    TODO: 
"""
import math
import codecs

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

def get_content (data_file):
    """
    """
    try:
        with open(data_file, 'r') as data:
            return (data.read())
    
    except IOError as err:
        print ("File error: " + str(err))

def print_option_menu (menu_goes_up_to):
    """
    """
    print ('')
    print ('\033[92m' + "Choose an option:" + '\033[0m')
    print ('')
    for ind in range(menu_goes_up_to + 1):
        print (str(ind))
    print ("done  : exit the program")
    print ('')
    cmd = raw_input('\033[92m' + 'Enter an option (or done): ' + '\033[0m')
    print ('')
    return cmd

def print_main_menu ():
    """
    """
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
    return cmd

def print_second_menu():
    """
    """
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
    return cmd

if __name__ == '__main__':
    print('utils.py')

