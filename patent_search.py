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
    # Will print the fields if search_for({'fields'}) is entered.
    if 'fields' in criteria:
        return fields
    # Checks the quality of the criteria entered.
    for criterion in criteria:
        if criterion not in fields:
            print(criterion,':',criteria[criterion],''' has been removed from \
            the search terms as it is not a permitted search term.''', sep='')
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
    print(num_found, 'results found!')
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
        print('Recieved ', str(start), ' of ', str(num_found), ' - ',
              str(int((start/num_found)*100)), '% complete.', sep='')
        start += 100
    print('Complete!')
    return results

def get_numbers(criteria={}):
    """Returns a list of application numbers for the given criteria."""
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
def get_patent(*, patent_number=None, document_ID=None):
    """Enter either a patent_number OR document_ID as a keyword argument
    to get the matching patent page from Google Patents. If you enter both,
    or neither, nothing will happen."""
    # These if statements decide how to format the url, as patent get_numbers
    # and document IDs require different formats. If both are entered it
    # *prints* an error message, and if no input is entered it does nothing.
    patent = []
    if (patent_number != None) and (document_ID == None):
        url = 'https://patents.google.com/patent/US'
        full_url = url + patent_number
    elif (document_ID != None) and (patent_number == None):
        url = 'https://patents.google.com/patent/'
        full_url = url + document_ID
    elif (document_ID != None) and (patent_number != None):
        print('Only enter patent_number OR document_ID.')
        return
    else:
        return
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
    for property in properties:
        property_contents = patent_soup.find(property).contents
        patent.append((property[1]['itemprop'], property_contents))
    patent.append(patent_soup.find(class_='abstract').contents[0])
    for y in patent_soup.find(class_='description').descendants:
    	patent.append(y.string)
    for result in patent_soup(class_='claim-text'):
    	for i in result.contents:
    		print(i.string, end='')
    	patent.append('\n')
    return patent
