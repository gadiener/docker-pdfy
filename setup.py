import codecs
import os
import re
from setuptools import setup, find_packages

def read(*parts):
	path = os.path.join(os.path.dirname(__file__), *parts)
	with codecs.open(path, encoding='utf-8') as fobj:
		return fobj.read()

def find_version(*file_paths):
	version_file = read(*file_paths)
	version_match = re.search(
		r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
	if version_match:
		return version_match.group(1)
	raise RuntimeError('Unable to find version string.')

setup(
	name='pdfy',
	version=find_version('src', '__init__.py'),
	packages=find_packages(),
	entry_points={
		'console_scripts':
			['pdfy = src.app:main']
	},
	include_package_data=True,
	author='Gabriele Diener',
	author_email='gabriele.diener@caffeina.com',
	description='Generate PDF from URL',
	license='MIT',
	keywords='docker api phantom pdf',
	url='http://caffeina.com/',
)
