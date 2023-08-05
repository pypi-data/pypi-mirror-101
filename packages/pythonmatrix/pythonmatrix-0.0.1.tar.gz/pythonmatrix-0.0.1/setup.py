import setuptools
from setuptools import setup

with open('README.md','r') as fh:
	long_description = fh.read()

setup(
	name='pythonmatrix',
	version='0.0.1',
	author='Tejaswi Kompella',
	author_email='tejakompella@gmail.com',
	description='This is a small Matrix Library.',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/Deadpool4099/pymat',
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=['numpy','scipy'],
	license='MIT'
)