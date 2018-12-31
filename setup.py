from setuptools import setup

setup(name='delaware_legislation_tracker',
      version='0.1',
      description='Tracks Delaware state assembly bills as they go through the legislative process',
      url='https://github.com/jrusselllewis/delaware-legislation-tracker',
      author='J. Russell Lewis',
      author_email='',
      license='MIT',
      packages=['legislation_tracker'],
      install_requires=[
        'feedparser','glob2'
      ])
