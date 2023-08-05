"""Module for setting up system and respective pine configurations"""

# imports - third party imports
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('pine.config'))
