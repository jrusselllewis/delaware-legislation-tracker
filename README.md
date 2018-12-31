# Delaware Legislation Tracker

## Prerequisites
### Python 3
`brew install python3`

### Required Modules
Use the setup file to install required modules:

`python3 setup.py install`

## Using the script:
To execute the script:
`python3 pull.py`

This will download the latest version of the delaware legislation rss feed, compare it against the last version, and output a csv file with the legislation information and changes flagged.
