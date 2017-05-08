#!/usr/local/bin/python3
'''
iiif_fixer.py: Consumes the CCMA IIIF object manifest canvas and image heights
'''
import requests, json, argparse, urllib, os.path

from tattler import Tattler, ManifeistyError
from embarkservice import EmbarkService, IIIFQuery, EmbarkError
from iiif_prezi.loader import ManifestReader, SerializationError 
from iiif_prezi.factory import StructuralError, RequirementError, DataError

class IIIFFixer():

  def __init__(self, report_path = "./iiif_report.json"):
    self.reporter = Tattler(report_path) 

  def log_error(self,e):
    self.reporter.log_error(e)

  def make_report(self):
    self.reporter.make_report()

  def fix_sizes(self,manifest):
    # Checks canvas heights and widths in an IIIF manifest, returns a corrected object
    for sequence in manifest.sequences:
      for canvas in sequence.canvases:
        for image in canvas.images:
          if image.resource.service:
            iiif_id = image.resource.service.id
            info_response = requests.get(iiif_id)
          
            if info_response.status_code == 200:
              iiif_info = json.loads(info_response.content)
              canvas.height = iiif_info['height']
              canvas.width = iiif_info['width']
            else:
              self.log_error(ManifeistyError("Got status code " + str(info_response.status_code) + "for image " + info_response.url))
    
    return manifest

  def fix_manifest(self,json):
    
    reader = ManifestReader(json)
    manifest = reader.read()
    
    if manifest is None:
      return None

    fixed = self.fix_sizes(manifest)

    # Some canvases have empty labels...
    for sequence in fixed.sequences:
      for canvas in sequence.canvases:
        if canvas.label == "":
          canvas.label = "Image"

    return manifest

  def write_manifest(self,manifest,path):
    as_string = manifest.toString(compact=False)
    with open(path,'w') as f:
      f.write(as_string)

def parse_args():
  # Returns vars of processed command line arguments
  parser = argparse.ArgumentParser(description="Fix an IIIF manifest made from Embark")
  parser.add_argument('embark_server', help = "URL of the embark server, default: http://embark.colby.edu",  default="http://embark.colby.edu")
  parser.add_argument('-n','--id', type = int, help = "Object ID")
  parser.add_argument('-o','--output', help = "Output file")
  # input json
  parser.add_argument('-i','--input_json', help = "Input JSON: expects a dict { 'objects' : [ { 'embark_ID' : N , ..}, ... ] }")
  # output dir
  parser.add_argument('-d', '--directory', help = "Directory for output (filename: N.json)", default = "./")
  # FIXME: Wire in bad image reporting
  parser.add_argument('-r', '--report', help = "Generate a JSON report for bad manifests and 404/500/etc images")
  args = vars(parser.parse_args())
  return args

def main():
  args = parse_args()
  fixer = IIIFFixer()
  
  # If input JSON, convert JSON to list of IDs
  id_nums = []
  if args["input_json"]:
    
    with open(args["input_json"]) as f:
      input_json = json.load(f)
      
    id_nums = [obj["embark_ID"] for obj in input_json["objects"] if len(obj["Images"]) > 0]
  elif args["id"]:
    # Else use id_num arg
    id_nums = [ int(args["id"]) ]

  embark = EmbarkService( host = args["embark_server"] )  
  
  for num in id_nums:
    # Make query
    query = IIIFQuery(embark_id = num)
    try:
      results = embark.fetch_json(query)
    except EmbarkError as e:
      fixer.log_error(e)

    # Make manifest from the results (catch error)
    manifest = fixer.fix_manifest(results)
    if manifest:
      path = os.path.join(args["directory"], str(num) + ".json")
      try:
        fixer.write_manifest(manifest, path)
      except Exception as e:
        fixer.log_error(e)

  fixer.make_report()

if __name__ == "__main__":
  main()
