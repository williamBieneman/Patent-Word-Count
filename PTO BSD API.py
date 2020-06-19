#USPTO Patent Grants and Applications Word Counter and Search, William Bieneman, April 18 2020

### THIS FILE FINDS ALL PATENTS OF WHICHEVER CRITERIA ARE ENTETERED.
### THE RETURNED VALUE IS A JSON DOCUMENT WITH VARIOUS ATTRIBUTES ABOUT
### DOCUMENTS MATCHING THE CRITERIA GIVEN.

import requests
import json
from requests.utils import quote

print('USPTO Patent Search\n')

## ⬇︎ asks for the fields that the user would like to search, then gets their query for it.
parameters={}
parIn = ''
while (parIn != '0') or (parIn != 'EXIT'):
    parIn = input('''Which parameter would you like to edit?
1. Application Number
2. Assignee
3. Applicant
4. Inventor
5. Other

0. Done

''')
    parIn = parIn.lower()
    if parIn == 'application number' or parIn == '1':
        appNumber = input('Application Number: ')
        parameters.update({'applicationNumber':appNumber})
    elif parIn == 'assignee' or parIn == '2':
        assignee = input('Assignee: ')
        parameters.update({'assignee':assignee})
    elif parIn == 'applicant' or parIn == '3':
        applicant = input('Applicant: ')
        parameters.update({'applicant':applicant})
    elif parIn == 'inventor' or parIn == '4':
        inventor = input('Inventor: ')
        parameters.update({'inventor':inventor})
    elif parIn == 'other' or parIn == '5':
        chosenField = input('Field: ')
        searchTerm = input('Search term/phrase: ')
        parameters.update({chosenField:searchTerm})
    elif parIn == 'done' or parIn == '0':
        break
    else:
        print('Choose a listed value.')

## ⬇︎ formats the parameters for a URL
for x in parameters:
    parameters[x]=quote(parameters[x])
parameters = ((((((str(parameters).replace('\', \'','&')).replace(': ','=')).replace('{','')).replace('}','')).replace('\'','')).replace(' ',''))

## ⬇︎ requests from the USPTO Bulk Search and Download API and returns the JSON
bulk_search = requests.get('https://developer.uspto.gov/ibd-api/v1/patent/application?',parameters)
bulk_search.raise_for_status
print(bulk_search.text)
print(bulk_search.url)
