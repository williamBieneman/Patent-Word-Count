# patent_search.py created by William Bieneman, June 2020
"""This module defines functions for finding patent numbers from given
criteria, patents from patent numbers, and more.
"""
import requests
from bs4 import BeautifulSoup
import json
from requests.utils import quote

## (adapted from PTO BSD API.py)
def search_for(criteria={}):
    """Returns JSON from the matching the given criteria.
    Entering {"fields"} will return a list of fields."""

    fields = ['searchText', 'criteriaSearchText', 'documentType',
              'applicationType', 'publicationFromDate', 'publicationToDate',
              'documentId', 'applicationNumber', 'applicationFromDate',
              'applicationToDate', 'title', 'patentNumber', 'assignee',
              'applicant', 'inventor']
              # (also:) 'start', 'rows', 'sortField', 'sortOrder']
    parameters = {}
    # Checks the quality of the criteria entered.
    if type(criteria) is dict:
        pass
    elif type(criteria) is set:
        if criteria != {'fields'}:
            raise TypeError("You must enter a dictionary, or \"{'fields'}\"!")
    else:
        raise TypeError("You must enter a dictionary or \"{'fields'}\"!")
    # Will print the fields if search_for({'fields'}) is entered.
    if 'fields' in criteria:
        return fields
    for criterion in criteria:
        if criterion not in fields:
            print(criterion,':',criteria[criterion], 'has been removed from \
             the search terms as it is not a permitted search term.', sep='')
        elif criterion in fields:
            parameters.update({fields.pop(fields.index(criterion)):
                                criteria[criterion]})
    for x in parameters:
        parameters[x] = quote(parameters[x])
    parameters = str(parameters).replace('\', \'','&').replace(': ','=')\
                                .replace('{','').replace('}','')\
                                .replace('\'','').replace(' ','')
    start = 0
    rows = 0
    # Finds the number of results matching the criteria.
    url = 'https://developer.uspto.gov/ibd-api/v1/patent/application?'\
            +parameters+'&start='+str(start)+'&rows='+str(rows)
    print('Accessing...')
    search_results = requests.get(url)
    search_results.raise_for_status()
    num_found = json.loads(search_results.text)['response']['numFound']
    # Estimates the time it will take - very rough!
    est_hou, est_min, est_sec = 0, 0, 0
    est_sec = int((num_found/100)* 1.2)
    if est_sec > 60:
        est_min = int(est_sec/60)
        est_sec = int(est_sec%est_min)
    if est_min > 60:
        est_hou = int(est_min/60)
        est_min = int(est_min%est_hou)
    print(f'{num_found} results found! Estimated time: ',\
          f'{est_hou:0>2}:{est_min:0>2}:{est_sec:0>2}', sep='')
    results = []
    rows = 100
    # Accesses the API repeatedly until every result has been recieved.
    while start < num_found:
        search_results = requests.get(
                'https://developer.uspto.gov/ibd-api/v1/patent/application?'
                +parameters+'&start='+str(start)+'&rows='+str(rows)
                )
        search_results.raise_for_status()
        search_results = json.loads(search_results.text)
        for item in search_results['response']['docs']:
            results.append(item)
        print(f'Recieved {start} of {num_found} -',\
              f'{int((start/num_found)*100)}% complete.')
        start += 100
    print(f'Recieved {num_found} of {num_found} - 100% complete!')
    return results

def get_numbers(criteria={}):
    """Returns a list of application numbers for the given criteria.
    Entering {"fields"} will return a list of fields."""
    results = search_for(criteria)
    numbers = []
    for item in results:
        numbers.append(item['documentId'])
    return numbers

def get_numbers_from(results):
    """The same as get_numbers() except the argument instead must be a
     decoded JSON document or a Python list of dictionaries with a
     "documentId" key."""
    numbers = []
    for item in results:
        numbers.append(item['documentId'])
    return numbers

## (adapted from GooglePatents.py)
def get_patent(*, patent_number=None, document_ID=None, return_fields=False):
    """Enter either a patent_number OR document_ID as a keyword argument
    to get the matching patent page from Google Patents. If you enter both,
    or neither, nothing will happen.
    Data will be returned as a dictionary.
    Enter return_fields = True to get a list of returned values."""
    patent = {
              'title' : None,
              'publicationNumber' : None,
              'applicationNumber' : None,
              'inventor' : None,
              'assigneeCurrent' : None,
              'assigneeOriginal' : None,
              'filingDate' : None,
              'abstract' : None,
              'description' : None,
              'claims' : None
              }
    if return_fields == True:
        return patent.keys()
    # These if statements decide how to format the url, as patent get_numbers
    # and document IDs require different formats. If both are entered or if
    # nothing is entered, it raises a ValueError.
    if (patent_number != None) and (document_ID == None):
        url = 'https://patents.google.com/patent/US'
        full_url = url + patent_number
    elif (document_ID != None) and (patent_number == None):
        url = 'https://patents.google.com/patent/'
        full_url = url + document_ID
    elif (document_ID != None) and (patent_number != None):
        raise ValueError('Only enter patent_number OR document_ID.')
        return
    else:
        raise ValueError('Enter a patent_number or document_ID!')
        return
    # Gets the page, checks for 200 response.
    patent_page = requests.get(full_url)
    patent_page.raise_for_status()
    ## parses the returned page
    patent_soup = BeautifulSoup(patent_page.text,'html.parser')
    properties = [
                  ('span', {'itemprop':'title'}),
                  ('dd', {'itemprop':'publicationNumber'}),
                  ('dd', {'itemprop':'applicationNumber'}),
                  ('dd', {'itemprop':'inventor'}),
                  ('dd', {'itemprop':'assigneeCurrent'}),
                  ('dd', {'itemprop':'assigneeOriginal'}),
                  ('time', {'itemprop':'filingDate'}),
                  ('time', {'itemprop':'publicationDate'})
                  ]
    # This adds various metadata (as seen above in properties).
    for property in properties:
        property_contents = patent_soup.find(property).contents
        patent.update({property[1]['itemprop']:property_contents})
    # Adds the abstract.
    patent.update({'abstract':patent_soup.find(class_='abstract').contents[0]})
    # Adds the description (which is split into many elements in the HTML).
    description = ''
    for y in patent_soup.find(class_='description').descendants:
        if y.string is None:
            continue
        description += str(y.string).replace('\n','') + ' '
    patent.update({'description':description})
    # And finally, adds the claims.
    claims = ''
    for result in patent_soup(class_='claim-text'):
        for i in result.contents:
            claims += str(i.string).replace('\n','') + ' '
        claims += '\n'
    patent.update({'claims':claims})
    return patent

## (adapted from basic word counter.py)
def count_words(text: str, /, min_return = 0):
    """Counts the number of words in the text, and counts the number of
    instances of each word. min_return sets the minimum number of occurances
    of a word to be recorded and returned."""
    if type(text) != str:
        raise TypeError("Your text must be a string!")
    # Takes the entered text and reformats it to be easier to count.
    fixed_text = text.lower()
    punctuation = [
                    '.', ',', '?', '/', '<', '>', ':', ';', '"', "'", '[',\
                    ']', '{', '}', "\\", '|', '!', '@', '#', '$', '%', '^',\
                    '&', '*', '(', ')', '-', '_', '+', '=', '~', '`'
                    ]
    for i in punctuation:
        fixed_text=fixed_text.replace(i,'')
    # Makes a list of every word.
    word_list = fixed_text.split(' ')
    length = len(word_list)
    n = 0
    word_counts = {}
    counted_words = []
    # Counts each word in the list
    for n in range(0,length):
        word = word_list[n]
        if counted_words.count(word) == 0:
            count = word_list.count(word)
            word_counts.update({word : count})
            counted_words.append(word)
    word_counts.update({'Total words':n})
    # This sorting was cleaner when word_counts was a list of tuples,
    # but I think having it be a dictionary is worth the comlications.
    sorted_word_counts = {}
    for x in sorted(word_counts, reverse = True):
        sorted_word_counts.update({x: word_counts[x]})
    word_counts = sorted_word_counts
    # This line made more sense when word_counts was a list of tuples,
    # but now it is just finding the first key of word_counts (skipping the
    # total), and finding the value associated with it.
    most_counted_word = word_counts[list(word_counts.keys())[1]]
    # Similarly, this just finds the highest number
    most_counted_number = list(word_counts.keys())[1]
    uncounted = []
    if min_return == 0:
        return word_counts
    elif min_return < 0:
        raise ValueError("min_return must be more than 0.")
    elif min_return > 0:
        for word in word_counts:
            if word_counts[word] >= min_return:
                pass
            elif word_counts[word] < min_return:
                uncounted.append(word)
    for word in uncounted:
        word_counts.pop(word)
    # I just realized that since the most counted word, its count, and the
    # list of uncouted words aren't returned, setting them is kinda useless,
    # but they may be used in the future, so I'm keeping them in for now.
    return word_counts
