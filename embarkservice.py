#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 
'''
iiif_fixer.py: Consumes the CCMA IIIF object manifest, corrects paths and image heights
'''
import requests, json, argparse, os.path

class EmbarkError(Exception):
  # properties for report payload
  def __init__(self,msg,resource = None):
    self.args = [msg]
    self.resource = resource

class KioskQuery():
  # TODO: Test verifies embark_args is made for valid query,layout,fmt, max_recs, rec_type; for default terms; for invalid terms

  def __init__(self, query =  "" , layout = "ccma_objects", fmt = "shtml", max_recs = 1, rec_type = "objects_1"):
    self.query = query
    self.layout = layout
    self.fmt = fmt
    self.max_recs = max_recs
    self.rec_type = rec_type

  @property
  def embark_args(self):
    return {"layout" : self.layout , "format" : self.fmt, "maximumRecords": self.max_recs, "recordType": self.rec_type, "query": self.query}

class IIIFQuery(KioskQuery):
  # TODO: Test verifies embark_args is made for valid query,layout,fmt, max_recs, rec_type; for default terms; for invalid terms
  # TODO: Make with illegal id, etc

  def __init__(self, portfolio = 1):
    query = "[Portfolios]_ID=" + portfolio
    super().__init__(query , layout = "iiif_portfolio", fmt = "shtml", max_recs = -1, rec_type = "objects_1")

  def __init__(self, collection = True):
    query = "_ID>1"
    super().__init__( query , layout = "iiif_collection", fmt = "shtml", max_recs = -1, rec_type = "objects_1")

  def __init__(self, embark_id = 1):
    query = "_ID=" + str(embark_id)
    super().__init__( query , "iiif_imgs", "shtml", 1, "objects_1")

class EmbarkService():
  # TODO: Test verifies if URLs are made successfully
  # TODO: Mock response with valid/invalid JSON

  @property
  def url(self):
    return self.host + self.path

  def __init__(self, host = "http://embark.colby.edu", path = "/results.html"): 
    self.path = path
    self.host = host

  def fetch_json(self, query):
    # Takes a KioskQuery object and returns a JSON object with results or raise an error with a JSON report for the problem

    r = requests.get(self.url,params=query.embark_args)
    
    if r.status_code == 200:
      # Hack: Strip control chars
      # FIXME: Should replace carriage returns in strings w/ </br>
      result = r.content.decode(r.encoding)
      fixed = result.replace('\t','    ').replace('\n','').replace('\r','')
      
      try: 
        results = json.loads(fixed)
        return results
      except json.JSONDecodeError as e:
        # FIXME: do stuff with e to make report
        raise EmbarkError("EmbarkError: received JSON decode error on response from " + r.url)
    else:
      raise EmbarkError("EmbarkError: Received status code " + r.status_code + "for " + r.url)
    
  def fetch_csv(self, query):
    print('TODO: Verify CSV and return (for Excel, WebCSV export')

  def fetch_id_json(self, layout, rec_type, id_num):
    # Returns JSON for a particular layout, table, and ID num (for grabbing/testing/validating layouts) 
    s = "_ID=" + str(id_num)
    query = KioskQuery(query  = s, layout = layout, rec_type = rec_type)
    return fetch_json(query)