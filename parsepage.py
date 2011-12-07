#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
    TODO: 
"""
import HTMLParser 

class ParsePage(HTMLParser.HTMLParser): 
    """
    """
    def __init__(self, dozens):
        """
        """
        self.dozens = dozens
        HTMLParser.HTMLParser.__init__(self)
        self.inside_td = False
        self.counter = 0
        self.raffle = {"Number": 0, "Date": "00/00/00",  "Dozens": [], "Accumulated": 'Não'}
        self.all_content = []
        self.key = {"Number": 0, "Date": 1, "Dozens": 2, "Accumulated": 2 + self.dozens + 7}

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
            if self.counter in range(2, 2 + self.dozens):
                self.raffle["Dozens"].append(data)
            elif self.counter == self.key["Number"]:
                self.raffle["Number"] = data
            elif self.counter == self.key["Accumulated"]:
                self.raffle["Accumulated"] = data
            elif self.counter == self.key["Date"]:
                self.raffle["Date"] = data

    def get_full_data (self):
        return (self.all_content)
    
    def _test():
        import doctest
        doctest.testfile('test/parsepage_test.txt')

if __name__ == '__main__': _test()
