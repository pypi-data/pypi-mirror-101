from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: End Users/Desktop',
  'Operating System :: Unix',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pyls_smart',
  version='0.0.1',
  description='A command to list directory',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/vickyrv2206/python_project',  
  author='Vignesh Ramesh',
  author_email='vickyvignesh2206@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='list-directory', 
  packages=[
        'pyls_smart',
    ],
  install_requires=[''] 

)
