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
"""
    TODO: 
"""
import math
import codecs

def mean (x_list):
    r"""
        >>> mean([1,2,3,4,5,6,7])
        4.0
        
        >>> mean([1,2,3,4,5,6])
        3.5
    """
    return float(sum(x_list))/len(x_list)

def standard_deviation(x_list, x_mean):
    r"""
        Is a way of measuring spread, and it's the average of the distance
        of values from the mean

        >>> standard_deviation([1,2,3,4,5,6], mean([1,2,3,4,5,6]))
        1.707825127659933
        
        >>> standard_deviation([1,2,3,4,5,6,7], mean([1,2,3,4,5,6,7]))
        2.0
    """
    return math.sqrt((float(sum([ x**2 for x in x_list ]))/len(x_list)) - (x_mean ** 2))

def standard_score(x_elem, x_mean, x_stand_deviation):
    r"""
        Number of standard deviation from the mean.

        >>> standard_score(75,70,20)
        0.25
        
        >>> standard_score(55,40,10)
        1.5

        >>> standard_score(35,40,10)
        -0.5
    """
    return (float(x_elem - x_mean) / x_stand_deviation)

def ret_unit(num):
    r"""
        >>> ret_unit(int('01'))
        1
        >>> ret_unit(11)
        1
    """
    return int(round(math.fmod((float(num)/10.0),1)*10))

def dozen(num):
    r"""
        >>> dozen(int('01'))
        0
        >>> dozen(11)
        1
    """
    return int((num/10)//1)

def isodd(num):
    r"""
        >>> isodd(1)
        True
        >>> isodd(0)
        False
        >>> isodd(2)
        False
    """
    return num & 1 and True or False

def get_content (data_file):
    """
    """
    try:
        f = open(data_file, 'r')
        data = f.read()
        f.close()
        return (data)
    
    except IOError, err:
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
    print ("dela : show the number delay between raffles")
    print ("devi : show the standard deviation of the last delay")
    print ("done : exit the program")
    print ("doze : show the most common dozens over all raffles")
    print ("freq : show the frequency of each delay time")
    print ("last : show the last time a numbers arises.")
    print ("look : look up for a given group of dozens.")
    print ("more : show the numbers more often arises.")
    print ("occu : print the list of occurrence of a number during the raffles.")
    print ("rule : show the most common combination of even and odds")
    print ("scor : show the standard score of the last delay")
    print ("show : show all data in memory.")
    print ("sugl : Suggest the numbers with best statistics and arises less recently")
    print ("sugm : Suggest the numbers with best statistics and arises more recently")
    print ("sugs : Suggest the numbers with best statistics and are closer from the mean")
    print ("summ : Show the sum of each dozen, given a number to the whole raffle")
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

def _test():
    import doctest
    doctest.testmod()
    doctest.testfile("test/utils_test.txt")

if __name__ == '__main__': _test()
