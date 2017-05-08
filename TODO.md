manifeisty.py TODO (5/5/2017):
===============================
	[X]Finish wiring in server/query classes
	[X]Clean up fix code, delete "fix url" if not used
	[ ]Tests!
	[ ]Output top-level collection manifest
	[ ]Take a portfolio ID arg?
	[ ]Take an object array size for large input json -> test
	[ ]Report flag
	[X]Reports! 
		[X]Errors:
			[X]Throw EmbarkError on JSONDecode issue
			[X]Catch EmbarkError from service calls
			[X]Catch errors from iiif_prezi
			[X]Raise errors from IIIFFixer on bad image returns
		[X]Tattle:
			[X]Make report from Error types
		[ ]Error classes:
			[ ]On log_error, into a TattlerError class to refactor make_report logic
	[ ]embarkservice:
		[ ]Take CSV