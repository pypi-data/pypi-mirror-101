from distutils.core import setup
from setuptools import find_packages

setup(
  name = 'shannonca', 
  packages = find_packages(exclude=['data']),  
  version = '0.0.4',   
  license='MIT',       
  description = 'Informative Dimensionality Reduction via Shannon Component Analysis',   
  author = 'Benjamin DeMeo',                   
  author_email = 'bdemeo@g.harvard.edu',      
  url = 'https://github.com/bdemeo/shannonca',  
  download_url =  'https://github.com/bendemeo/shannonca/archive/refs/tags/0.0.1.tar.gz',
  keywords = ['Shannon', 'Information', 'Dimensionality','reduction', 'single-cell','RNA'], 
  install_requires=[           
          'sklearn',
          'scipy',
          'numpy',
          'matplotlib',
          'pandas',
          'seaborn',
          'scanpy'
      ]
    )
