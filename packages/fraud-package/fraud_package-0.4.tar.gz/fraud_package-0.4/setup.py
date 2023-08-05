import os
from setuptools import setup
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='fraud_package',
	long_description=long_description,
	long_description_type='text/markdown',
      version='0.4',
      description='Fraud detection Feature Engineering Pipeline',
      packages=['Feature_Engineering_Pipeline'],
      zip_safe=False)

