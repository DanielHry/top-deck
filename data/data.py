import os
import pandas as pd


DIR = os.path.dirname(__file__)
DATA_ALL_DECKS = pd.read_csv(DIR + "/data_decs.csv")
