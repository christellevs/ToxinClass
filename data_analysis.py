# -*- coding: utf-8 -*-
"""data_analysis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13mL2Z_344bPsTwTJml1vy_BY3ANp59J1

# **Post Processing Data Analysis**

# **0. Setup**
"""

# mount Google drive
from google.colab import drive

drive.mount('/content/drive')

# -----------------------------------------------------------------------------
# IMPORTS
import csv
import io
import itertools as ite
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import os.path
import random
import re
import seaborn as sns
import sklearn
import statistics

RANDOM_SEED = 273
random.seed(RANDOM_SEED)

# Change below to path of source code folder
PATH_TO_FOLDER = '/content/drive/My Drive/UoS/Year3/COM3001/Submission/source_code'

# FILEPATHS
# -----------------------------------------------------------------------------

# processed data
f_train_proteins_list = PATH_TO_FOLDER + '/pre_processing_files/dataframes/train_proteins_list.pickle'
f_train_complete = PATH_TO_FOLDER + '/pre_processing_files/dataframes/train_complete.pickle'
f_train_atchley_means = PATH_TO_FOLDER + '/pre_processing_files/dataframes/train_atchley_mean.pickle'

f_train_atchley_raw = PATH_TO_FOLDER + '/pre_processing_files/dataframes/train_atchley_raw.pickle'
f_train_atchley_diff = PATH_TO_FOLDER + '/pre_processing_files/dataframes/train_atchley_diff.pickle'


# PROTEIN PROCESSING FUNCTIONS START
# -----------------------------------------------------------------------------

# PROTEIN CLASS
class ProteinSequence:
    def __init__(self, identifier, toxic, length, sequence):
        self.identifier = identifier
        self.toxic = toxic
        self.length = length
        self.sequence = sequence
        self.seq_dict_raw = {}
        self.seq_dict_diff = {}
        self.matrix_raw = np.zeros((5, length))
        self.matrix_diff = np.zeros((5, length))

    def to_dict_raw(self):
        return {'identifier': self.identifier,
                'toxic': self.toxic,
                'length': self.length,
                'sequence': self.sequence,
                'f1_raw': self.matrix_raw[0],
                'f2_raw': self.matrix_raw[1],
                'f3_raw': self.matrix_raw[2],
                'f4_raw': self.matrix_raw[3],
                'f5_raw': self.matrix_raw[4],
                'atchley_raw_avg': np.average(self.matrix_raw, axis=0)}

    def to_dict_diff(self):
        return {'identifier': self.identifier,
                'toxic': self.toxic,
                'length': self.length,
                'sequence': self.sequence,
                'f1_diff': self.matrix_diff[0],
                'f2_diff': self.matrix_diff[1],
                'f3_diff': self.matrix_diff[2],
                'f4_diff': self.matrix_diff[3],
                'f5_diff': self.matrix_diff[4],
                'atchley_diff_avg': np.average(self.matrix_diff, axis=0)}


# COMMON FUNCTIONS START
# -----------------------------------------------------------------------------

# for writing and reading data to/from a binary file
def pickle_method(fname, method, context):
    if method == 'wb':
        return pickle.dump(context, open(fname, method))
    elif method == 'rb':
        return pickle.load(open(fname, method))


# SUMMARY FUNCTIONS
def describe_df(df, decimal):
    return df.describe().T[['mean', 'std', 'max', 'min', '25%', '50%', '75%']].round(decimals=decimal)


# unpickling method
proteins = pickle_method(f_train_proteins_list, 'rb', '')

print(np.average(proteins[0].matrix_raw, axis=0).shape)

"""# **1. Data Analysis**"""

df_raw = pickle_method(f_train_atchley_raw, 'rb', '')
df_diff = pickle_method(f_train_atchley_diff, 'rb', '')

df_raw.head()

df_diff.head()

print(describe_df(df_raw, 2))
print(describe_df(df_diff, 2))