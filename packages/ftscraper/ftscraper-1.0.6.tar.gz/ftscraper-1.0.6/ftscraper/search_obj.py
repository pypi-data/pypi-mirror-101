import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import date
import time

import ftscraper.api as ft


class SearchObj(object):
    """Class which contains each search result when searching data in Financial Times.
    
    This class contains the search results of the ft.com search made with the function
    call `ftscraper.search(search)` which returns a :obj:`list` 
    of instances of this class with the formatted retrieved information.
    """

    def __init__(self, sec_name, symbol, sec_type, similarity_score):
        self.sec_name = sec_name
        self.symbol = symbol
        self.sec_type = sec_type
        self.similarity_score = similarity_score

    def get_summary(self):
        """
        Get summary of the fund
        """
        
        atts = ft.get_summary(sec_name=self.sec_name, symbol=self.symbol, sec_type=self.sec_type)

        return atts
    
    def get_historical(self):
        """
        Get historical prices of the fund
        """
        df = ft.get_historical(symbol=self.symbol)

        return df

    
