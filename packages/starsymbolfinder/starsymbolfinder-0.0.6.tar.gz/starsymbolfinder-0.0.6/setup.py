from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='starsymbolfinder',
  version='0.0.6',
  description='A package that finds a star symbol for a specified date.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://picstreme.com/',
  author='DefaultGamingChannel',
  author_email='info@picstreme.com',
  license='MIT',
  classifiers=classifiers,
  keywords='starsymbol',
  packages=find_packages(),
  install_requires=['']
)
