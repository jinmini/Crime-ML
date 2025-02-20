from dataclasses import dataclass
from flask import json
import googlemaps
import pandas as pd

@dataclass
class Datareader:

    def __init__(self):
        self._context = "C:\\Users\\bitcamp\\Documents\\2025\\25ep_python(esg)\\Crimecity_250220\\com\\datas\\"
        self._fname = ""

    @property
    def context(self) -> str:
        return self._context
    
    @context.setter
    def context(self, context):
        self._context = context
    
    @property
    def fname(self) -> str:
        return self._fname
    
    @fname.setter
    def fname(self, fname):
        self._fname = fname

    def new_file(self)->str:
        return self._context + self._fname

    def csv_to_dframe(self) -> object:
        file = self.new_file()
        return pd.read_csv(file, encoding='UTF-8', thousands=',')

    def xls_to_dframe(self, header, usecols)-> pd.DataFrame:
        file = self.new_file()
        return pd.read_excel(file, header=header, usecols=usecols)

    def json_load(self):
        file = self.new_file()
        return json.load(open(file, encoding='UTF-8'))

    def create_gmaps(self):
        return googlemaps.Client(key='..')
 