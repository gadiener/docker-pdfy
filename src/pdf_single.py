import os
from flask_restful import Resource, abort
from utils import Utils

class PdfSingle(Resource):
	def __init__(self):
		self.utils = Utils()

		super(PdfSingle, self).__init__()

	def get(self, name):
		path = self.utils.paths["storage"] + '/' + name + '.pdf'

		if not os.path.isfile(path):
			abort(404)

		return {
			"status": 'exist',
			"name": name + '.pdf',
			"path": path
		}

	def delete(self, name):
		try:
			path = self.utils.paths["storage"] + '/' + name + '.pdf'

			if not os.path.isfile(path):
				abort(404)

			os.remove(path)

			if os.path.isfile(path):
				raise OSError("System can't delete file " + path)

			return {
				"status": "deleted",
				"name": name + '.pdf',
				"path": path
			}
		except OSError, ex:
			abort(400, message=str(ex))
