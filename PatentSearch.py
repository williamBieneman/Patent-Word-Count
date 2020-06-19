# package to search for patent numbers based on criteria

import requests
import json
from requests.utils import quote

class Search:
    def __init__(self):
        self.fields = {"Abstract":"ABST", "130(b) Affetmation Flag":"AFFF", "130(b) Affirmation Statement":"AFFT",
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
        self.parameters = ['searchText', 'criteriaSearchText', 'documentType', 'applicationType', 'publicationFromDate', 'publicationToDate',
                           'documentID', 'applicationNumber', 'applicationFromDate', 'applicationToDate', 'title',
                           'patentNumber', 'assignee', 'applicant', 'inventor', 'start', 'rows', 'sortField', 'sortOrder']
    def search_for(self, *, searchText=None, criteriaSearchText=None, docType=None, appType=None, pubFromDate=None, pubToDate=None, docID=None,
                   appNum=None, appFromDate=None, appToDate=None, title=None, patentNum=None, assignee=None, applicant=None, inventor=None):
        ## Searches the Bulk Data Search and Download API for the parameters you enter.
        function_parameters = [searchText, criteriaSearchText, docType, appType, pubFromDate, pubToDate, docID,
                               appNum, appFromDate, appToDate, title, patentNum, assignee, applicant, inventor]
        param_string='?'
        request_url = "https://developer.uspto.gov/ibd-api/v1/patent/application"
        n = 0
        for item in function_parameters:
            if item:
                if n > 0:
                    param_string += '&' + self.parameters[function_parameters.index(item)] + "=" + item
                else:
                    param_string += '?' + self.parameters[function_parameters.index(item)] + "=" + item
        param_string = quote(param_string, safe='?&=')
        request_url += param_string
        response = requests.get(request_url)
        print(response.text)
