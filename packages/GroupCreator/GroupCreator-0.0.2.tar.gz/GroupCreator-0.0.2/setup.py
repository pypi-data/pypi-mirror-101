from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 2 - Pre-Alpha',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='GroupCreator',
  version='0.0.2',
  description='A package that creates groups for you.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://picstreme.com/',
  author='DefaultGamingChannel',
  author_email='info@picstreme.com',
  license='MIT',
  classifiers=classifiers,
  keywords='groups',
  packages=find_packages(),
  install_requires=['']
)
