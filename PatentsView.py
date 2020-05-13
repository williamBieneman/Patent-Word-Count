  #    Basic test of PatentsView API using a 'Queries' Class

import json
import requests

class Criterion:

    def __init__(self, Field, Values, *, _eq = False, _neq = False, _gt = False, _gte = False, _lt = False, _lte = False,
                 _begins = False, _contains = False,
                 _text_all = False, _text_any = False, _text_phrase = False,
                 _not = False, _and = False, _or = False):

        self.Field = Field
        self.Values = Values
        self.vals = {str(self.Field):self.Values}

        #        Creates query for search (eg for Criterion('patent_date', '2007-01-04'),
        #    the output of self.SearchFor will be: {"patent_date":"2007-01-04"}

        mods = ["_eq", "_neq", "_gt", "_gte", "_lt", "_lte",
                "_begins", "_contains",
                "_text_all", "_text_any", "_text_phrase",
                "_not", "_and", "_or"]

        args = [_eq, _neq, _gt, _gte, _lt, _lte,
                _begins, _contains,
                _text_all, _text_any, _text_phrase,
                _not, _and, _or]

        self.modList = []
        self.SearchFor = {}

        for mod in mods:
            arg = args[mods.index(mod)]
            if arg is True:
                self.modList.append(mod)
                self.SearchFor = {mod:self.vals}
                break

        if self.SearchFor == {}:
            self.SearchFor = self.vals

        self.SearchFor = str(self.SearchFor).replace("'",'"')


    def search(self):
        """Searches the field specified in when the class was created"""
        print('patentsview.org/api/v1/patents/query?q=',self.SearchFor)

class Search:

    def __init__(self, fields):
        self.fields = [fields]
        self.SearchFor = []

    def all(self):

        if len(self.fields) == 1:
            self.SearchFor = self.fields[0]
        else:
            for f in self.fields:
                self.SearchFor.append(f.SearchFor)

        print('patentsview.org/api/patents/query?q='+str(self.SearchFor))

# I think the issue here was it was the wrong endpoint, but regardless this API fails to return useful information

##        response = requests.get('patentsview.org/api/v1/patents/query?q='+self.SearchFor)
##        print(response.url)
##        print(response.status_code)
##        print(response)
