
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='stevenpackagetest',
  version='1.0.0',
  description='A test',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Steven Livingston',
  author_email='therealenny1@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='test', 
  packages=find_packages(),
  install_requires=[''] 
)