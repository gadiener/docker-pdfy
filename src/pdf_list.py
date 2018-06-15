import os
from flask_restful import Resource, reqparse, inputs, abort
from utils import Utils

class PdfList(Resource):
	def __init__(self):
		self.utils = Utils()

		self.opt = {
			"strict": os.getenv('STRICT', None) == "true"
		}

		self.parser = reqparse.RequestParser()
		self.parser.add_argument(
			'urls',
			action='append',
			help='Input URLs are invalid',
			required=True
		)
		self.parser.add_argument(
			'name',
			type=inputs.regex('^[0-9a-zA-Z-_]+$'),
			help='File name is invalid',
			required=True
		)
		self.parser.add_argument(
			'orientation',
			choices=('portrait', 'landscape'),
			help='The orientation field must be portrait or landscape',
			default='portrait',
			store_missing=True
		)
		self.parser.add_argument(
			'paper',
			type=inputs.regex('^(A4|A3|A5|Legal|Letter|([0-9]+\.?[0-9]*(mm|cm|in|px))X([0-9]+\.?[0-9]*(mm|cm|in|px)))$'),
			help='The paper field must be one of the following A3, A4, A5, Legal, Letter or page size in mm, cm, in or px',
			default='A4',
			store_missing=True
		)
		self.parser.add_argument(
			'fit',
			type=inputs.regex('^(false|0|A4|A3|A5|Legal|Letter|([0-9]+\.?[0-9]*(mm|cm|in|pt))X([0-9]+\.?[0-9]*(mm|cm|in|pt)))$'),
			help='The fit field must be one of the following A3, A4, A5, Legal, Letter or page size in mm, cm, in or pt. Set it to false to disable this feature.',
			default='false',
			store_missing=True
		)
		# Not implemented
		self.parser.add_argument(
			'path',
			type=inputs.regex('^[0-9a-zA-Z-_\/]+$'),
			help='Path is invalid',
			required=False
		)

		super(PdfList, self).__init__()

	def get(self):
		return {
			"files": self.utils.listAllFileInDir(self.utils.paths["storage"])
		}

	def post(self):
		try:
			tmp_files = []
			status = "created"

			args = self.parser.parse_args()
			path = self.utils.paths["tmp"] + '/' + args.name
			final_path = self.utils.paths["storage"] + '/' + args.name + '.pdf'

			if os.path.isfile(final_path):
				if self.opt["strict"]:
					abort(409)
				status = "replaced"

			if self.utils.deleteAllFileInDir(path):
				os.rmdir(path)

			tmp_files = self.utils.multiDownload(
				args.urls,
				path,
				args.orientation,
				args.paper
			)

			temp_path = self.utils.pdfMerge(
				tmp_files,
				path + '/merged.pdf'
			)

			if not (args.fit == 'false' or args.fit == '0'):
				temp_path = self.utils.pdfScaleToFit(
					temp_path,
					path + '/fitted.pdf',
					args.fit,
					args.orientation
				)

			final_path = self.utils.pdfCompress(temp_path, final_path)

			return {
				"status": status,
				"name": args.name + '.pdf',
				"path": final_path,
				"urls": args.urls
			}
		except OSError, ex:
			abort(400, message=str(ex))
		except IOError, ex:
			abort(400, message=str(ex))
		finally:
			if 'path' in locals() and self.utils.deleteAllFileInDir(path):
				os.rmdir(path)

	def delete(self):
		try:
			path = self.utils.paths["storage"]

			if not self.utils.deleteAllFileInDir(path):
				raise OSError("System can't delete file " + path)

			return {
				"status": "deleted",
				"path": path
			}
		except OSError, ex:
			abort(400, message=str(ex))
