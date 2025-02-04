from itertools import count, product
from os import remove
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import re
URL = "https://appbrewery.github.io/Zillow-Clone/"
webpage = requests.get(URL)

soup = BeautifulSoup(webpage.content, "html.parser")

