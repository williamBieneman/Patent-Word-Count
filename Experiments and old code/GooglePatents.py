import requests
from bs4 import BeautifulSoup

url = 'https://patents.google.com/patent/US'
patent_number = input("Number: ")

full_url = url + patent_number

trys = 0
status_code = 0
while (status_code != 200) and (trys < 5):
    patent_page = requests.get(full_url)
    status_code = patent_page.status_code
    trys += 1
if status_code != 200:
    error = 'An error occured connecting to the web.\n      Status code: ' + str(status_code) + '. URL: ' + str(patent_page.url)
    raise RuntimeError(error).with_traceback(None)

## ⬆︎ gets the patents.google.com page for the relevant patent
## ⬇︎ parses it

patent_soup = BeautifulSoup(patent_page.text,'html.parser')

properties = [('span', {'itemprop':'title'}), ('dd', {'itemprop':'publicationNumber'}), ('dd', {'itemprop':'applicationNumber'}),
              ('dd', {'itemprop':'inventor'}), ('dd', {'itemprop':'assigneeCurrent'}), ('dd', {'itemprop':'assigneeOriginal'}),
              ('time', {'itemprop':'filingDate'}), ('time', {'itemprop':'publicationDate'})]

for property in properties:
    property_contents = patent_soup.find(property).contents
    print(property[1]['itemprop'], property_contents, sep=': ')

print(patent_soup.find(class_='abstract').contents[0])

for y in patent_soup.find(class_='description').descendants:
	print(y.string, end='')

for result in patent_soup(class_='claim-text'):
	for i in result.contents:
		print(i.string, end='')
	print('\n')
