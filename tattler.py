import json
from embarkservice import EmbarkError
from iiif_prezi.factory import PresentationError, MetadataError, ConfigurationError, StructuralError, RequirementError, DataError
from iiif_prezi.loader import SerializationError

class ManifeistyError(Exception):

    def __init__(self, msg):
        self.args = [msg]

class Tattler():

    def __init__(self, filepath):
        self.filepath = filepath
        self.errors = []

    def log_error(self, e):
        self.errors.append(e)

    def make_report(self):

        report = {}

        print("Making error report with " + str(len(self.errors)) + " errors")
        # Filter errors by type
        report["embark_error"] = [e.args for e in self.errors if e is EmbarkError]
        report["iiif_error"] = [{"resource": e.resource.id, "message": e.args} for e in self.errors if isinstance(e, PresentationError) ]
        report["image_error"] = [e.args for e in self.errors if e is ManifeistyError]

        with open(self.filepath, 'w') as f:
            j = json.dumps(report)
            f.write(j)
