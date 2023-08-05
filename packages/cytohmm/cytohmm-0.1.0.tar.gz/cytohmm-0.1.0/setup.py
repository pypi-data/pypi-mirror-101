from setuptools import setup, Extension
from Cython.Build import cythonize

import numpy

numpy_inc = numpy.get_include()

extensions = [
	Extension("cytohmm.markov_chain",
			["src/cytohmm/markov_chain.pyx"],
		include_dirs = [numpy_inc],
		),
	Extension("cytohmm.likelihood",
			["src/cytohmm/likelihood.pyx"],
		include_dirs = [numpy_inc],
		),
#	Extension("cytohmm.sequence_segmenter",
#			["src/sequence_segmenter.py"],
#		),
	]

setup(
	package_dir={'cytohmm': 'src/cytohmm'},
	ext_modules = cythonize(extensions),
	setup_requires=['numpy','cython'],
	packages=['cytohmm',],
	zip_safe=False,
)

