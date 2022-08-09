
import numpy as np
import pandas as pd
import seaborn as sns
#from .classify import Node

class Driver:

    def __init__(self, filepath):
        try:
            self.dataframe = pd.read_csv(filepath)
        except FileNotFoundError as e:
            print(e)

    def parse(self):
        self.dataAsDictFormat = {}
        for key in list(self.dataframe.columns):
            self.dataAsDictFormat[key.lower() + 's'] = set(list(self.dataframe[key]))
        return True

    def classifyData(self):
        self.classifiedDataAsDictFormat = {}
        root = Node()
        for key in list(self.dataframe.columns):
            root.add_child(Node(key))

        return

    def getData(self):
        return self.dataAsDictFormat

