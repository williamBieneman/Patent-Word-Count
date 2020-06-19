##  patent search -- the goal here is simply to direct the user to the appropriate USPTO page for their query

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
## ⫸this doesn't work because I lacked any amount of forsight required (aka I didn't know about /robots.txt yet)⫷ ##
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

import requests

stopwords = ['a', 'accordance', 'according', 'all', 'also', 'an', 'and', 'another', 'are', 'as', 'at', 'be', 'because', 'been', 'being', 'by', 'claim', 'comprises', 'corresponding', 'could', 'described', 'desired', 'do', 'does', 'each', 'embodiment', 'fig', 'figs', 'for', 'from', 'further', 'generally', 'had', 'has', 'have', 'having', 'herein', 'however', 'if', 'in', 'into', 'invention', 'is', 'it', 'its', 'means', 'not', 'now', 'of', 'on', 'onto', 'or', 'other', 'particularly', 'preferably', 'preferred', 'present', 'provide', 'provided', 'provides', 'relatively', 'respectively', 'said', 'should', 'since', 'some', 'such', 'suitable', 'than', 'that', 'the', 'their', 'then', 'there', 'thereby', 'therefore', 'thereof', 'thereto', 'these', 'they', 'this', 'those', 'thus', 'to', 'use', 'various', 'was', 'were', 'what', 'when', 'where', 'whereby', 'wherein', 'which', 'while', 'who', 'will', 'with', 'would']
# ⬆︎ words found on the USPTO database -- they do not yield results when searched
fields = {"Abstract":"ABST", "130(b) Affetmation Flag":"AFFF", "130(b) Affirmation Statement":"AFFT",
          "Applicant City":"AACI", "Applicant Country":"AACO", "Applicant Name":"AANM", "Applicant State":"AAST", "Applicant Type":"AAAT",
          "Application Date":"APD", "Application Serial Number":"APN", "Application Type":"APT",
          "Assignee City":"AC", "Assignee Country":"ACN", "Assignee State":"AS",
          "Assistant Examiner":"EXA", "Attorney or Agent":"LREP",
          "Certificates: Certificate of Correction":"COFC", "Certificates: PTAB Trial Certificate":"PTAB", "Certificates: Re-Examination Certificate":"REEX", "Certificates: Supplemental Examination Certificate":"SEC",
          "Claim(s)":"ACLM",
          "Cooperative Patent Classification":"CPC", "Current CPC Classification Class":"CPCL",
          "Description/Specification":"SPEC",
          "Foreign Priority":"PRIR", "Foreign References":"FREF",
          "Geovernment Interest":"GOVT",
          "International Classification":"ICL", "Hague International Filing Date":"ILFD", "International Registration Date":"ILRD", "International Registration Number":"ILRN", "International Registration Publication Date":"ILPD",
          "Inventor City":"IC", "Inventor Name":"IN", "Inventor State":"IS", "Issue Date":"ISD",
          "Other References":"OREF", "Parent Case Information":"PARN",
          "Patent Family ID":"FMID", "Patent Number":"PN",
          "PCT Information":"PCT", "PCT 371c124 Date":"PT3D", "PCT Filing Date":"PTAD",
          "Primary Examiner":"EXP",
          "Prior Published Document Date":"PPPD", "Priority Filing Date":"PRAD",
          "Reissue Data":"REIS", "Reissued Patent Application Filing Date":"RPAF",
          "Related US Application Data":"RLAP", "Related Application Filing Date":"RLFD",
          "Title":"TTL",
          "Current US Classification":"CCL",
          "Referenced By":"REF"}
# ⬆︎ fields that are searchable. the left is the title, the right is the shortener used by the USPTO database
# ⬇︎ various other modifiers used by the USPTO
date_range = "->"
truncation = "$"

Query = ''
print('generate a search!')
field = '.'
while field not in fields:
    field = input('which field? ')
query = input('query? ')

## ⬆︎ finds the correct shortener, and then ⬇︎ concatonates them and formats it for the URL

print("generating...")
Query = fields[field] + "/" + query
print("parsing...")
Query = Query.replace("/","%2F").replace(" ","+").replace('"',"%22").replace("'","%22")

## ⬇︎ this site's /robots.txt prohibits all bots from accessing all directories, so this whole code is useless.
url = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query="+Query+"&d=PTXT"
print("accessing: ",url,sep='')

with requests.get(url) as response:
    print(response.status_code)
