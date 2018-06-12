import os
import re
import subprocess
import requests
from shutil import move
from PyPDF2 import PdfFileMerger
from selenium import webdriver

class Utils():
	def __init__(self):
		self.paths = {
			"tmp": os.getenv('TMP_PATH', '/tmp'),
			"storage": os.getenv('STORAGE_PATH', '/storage'),
			"localstorage": os.getenv('LOCALSTORAGE_PATH', '/localstorage')
		}

		self.driver = webdriver.PhantomJS(
			'phantomjs', service_args=["--local-storage-path=" + self.paths["localstorage"]])

	def multiDownload(self, urls, path, orientation, paper_format):
		count = 1
		tmp_files = []

		for url in urls:
			file_path = self.download(url, path + '/' + str(count) + '.pdf', orientation, paper_format)
			if not os.path.isfile(file_path):
				raise OSError("System can't create file " + self.paths["tmp"])
			count += 1
			tmp_files.append(file_path)

		return tmp_files

	def download(self, url, target_path, orientation, paper_format):
		status_code = requests.get(url).status_code
		if status_code != 200:
			raise IOError("Request to url '" + url +
			              "' return http code " + str(status_code))

		self.driver.get(url)

		# hack while the python interface lags
		self.driver.command_executor._commands['executePhantomScript'] = (
			'POST', '/session/$sessionId/phantom/execute')
		if paper_format in ['A4','A3','A5','Legal','Letter','Tabloid']:
			page_format = 'this.paperSize = {{ format: \"{}\", orientation: \"{}\" }};'.format(paper_format, orientation)
		else:
			paper_format = paper_format.split('x')
			page_format = 'this.paperSize = {{ width: \"{}\", height: \"{}\" }};'.format(paper_format[0], paper_format[1])


		self.driver.execute('executePhantomScript', {
		                    'script': page_format, 'args': []})

		render = 'this.render("{}")'.format(target_path)
		self.driver.execute('executePhantomScript', {'script': render, 'args': []})
		return target_path

	def countPdfPages(self, filename):
		try:
			file_stream = file(filename, "rb")
			return len(re.compile(r"$\s*/Type\s*/Page[/\s]", re.MULTILINE | re.DOTALL).findall(file_stream.read()))
		finally:
			file_stream.close()

	def pdfMerge(self, input_files, output_path):
		merger = PdfFileMerger()
		try:
			for input_file in input_files:
				merger.append(open(input_file, 'rb'))

			with open(output_path, 'wb') as fout:
				merger.write(fout)

			return output_path
		finally:
			merger.close()

	def pdfCompress(self, input_path, output_path):
		try:
			compressed_path = input_path + '.tmp'
			subprocess.call(["pdfsizeopt", input_path, compressed_path])

			move(compressed_path, output_path)

			return output_path
		except subprocess.CalledProcessError, e:
			raise OSError(e)

	def countFile(self, pdf_path):
		if not os.path.isdir(pdf_path):
			return 0

		return len([name for name in os.listdir(pdf_path) if os.path.isfile(os.path.join(pdf_path, name))])

	def deleteAllFileInDir(self, dir):
		if not os.path.isdir(dir):
			return False

		for root, dirs, files in os.walk(dir, topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))

		return True

	def listAllFileInDir(self, dir):
		if not os.path.isdir(dir):
			return False

		return [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
