#!/usr/bin/env python

import os
from gevent.wsgi import WSGIServer
from flask import Flask
from flask_restful import Api
from pdf_list import PdfList
from pdf_single import PdfSingle

app = Flask(__name__)
api = Api(app)

api.add_resource(PdfList, '/')
api.add_resource(PdfSingle, '/<string:name>', endpoint='pdf')

opt = {
	"host": os.getenv('HOST', '0.0.0.0'),
	"port": os.getenv('PORT', 8080)
}

def main():
	#WSGIServer((opt["host"], opt["port"]), application=app).serve_forever()
	app.run(host=opt["host"], port=opt["port"], debug=True)

if __name__ == '__main__':
	main()
