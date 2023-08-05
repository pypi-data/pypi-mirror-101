"""setuptools setup module for granary.

Docs:
https://packaging.python.org/en/latest/distributing.html
https://setuptools.readthedocs.io/

Based on https://github.com/pypa/sampleproject/blob/master/setup.py
"""
from setuptools import setup, find_packages


setup(name='granary',
      version='3.1',
      description='The social web translator',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/snarfed/granary',
      packages=find_packages(),
      include_package_data=True,
      author='Ryan Barrett',
      author_email='granary@ryanb.org',
      license='Public domain',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Environment :: Web Environment',
          'License :: OSI Approved :: MIT License',
          'License :: Public Domain',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='social facebook flickr github instagram twitter activitystreams html microformats2 meetup mf2 atom rss jsonfeed',
      install_requires=[
          'beautifulsoup4~=4.8',
          'brevity>=0.2.17',
          'feedgen~=0.9',
          'google-cloud-ndb~=1.2',
          'html2text>=2019.8.11',
          'humanfriendly>=4.18,<10.0',
          'jinja2~=2.10',
          'mf2util>=0.5.0',
          'oauth-dropins>=3.1',
          'praw>=6.5,<8.0',
          'python-dateutil~=2.8',
          'requests~=2.22',
      ],
      tests_require=['mox3>=0.28,<2.0'],
)
