from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Datastructures_Algorithms',
  version='0.0.1',
  description='Implementation of data structures and algorithms in python',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/ayushsingh5941',  
  author='Ayush Singh',
  author_email='ayushsingh5941@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Data Structures, Algorithms', 
  packages=find_packages(),
  install_requires=[''] 
)