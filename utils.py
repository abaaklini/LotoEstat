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
        with codecs.open(data_file, 'r', 'latin-1') as data:
            return (data.read())
    
    except IOError as err:
        print ("File error: " + str(err))

if __name__ == '__main__':
    print('utils.py')

