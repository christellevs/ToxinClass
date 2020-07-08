import Bio as bio
import csv
import importlib
import io
import numpy as np
import os
import pandas as pd
import pickle
import random
import re
import statistics

from typing import List, Dict

from Bio import SeqIO
from Bio.SeqIO.FastaIO import SimpleFastaParser
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit


# module imports
import config as cfg
import protein as prot

# COMMON FUNCIONS
# -----------------------------------------------------------------------------
# writes or reads data to/from a binary file
def pickle_method(fname:str, method:str, context):
  """Pickles/unpickles a file."""
  if method == 'wb':
      return pickle.dump(context, open(fname, method))
  elif method == 'rb':
      return pickle.load(open(fname, method))
    
def write_to_file(fname:str, context, function) -> None:
  """Writes to file."""
  with open(fname, 'w') as f:
    function(f, context)
  f.close()

def df_to_csv(df:pd.DataFrame, fname:str, sep:str) -> pd.DataFrame:
  """Converts a DataFrame to a .csv file."""
  return df.to_csv(fname, sep, encoding='utf-8')

def cvs_to_df(fname:str, col_idx:int):
  """Converts a .csv file to a DataFrame."""
  return pd.read_csv(fname, index_col=col_idx, encoding='utf-8')

def split_seq(sequence:str) -> List[str]:
  """Splits string qeuence returns list."""
  return [char for char in sequence]


# PRE-PROCESSING FUNCIONS
# -----------------------------------------------------------------------------

def crop_sequences(proteins):
  """Returns protein sequences that are less than the specified length."""
  return [p for p in proteins if p.length <= cfg.MAX_SEQ_LEN]

# opens fasta file, returns protein object list
def parse_fasta(path_fasta:str, is_toxic:int) -> List[str]:
  """Parses .fasta files into a list of Protein objects."""
  sequences = []
  with open(path_fasta) as fasta_file:
    for title, sequence in SimpleFastaParser(fasta_file):
      if not any(ele in sequence for ele in cfg.INVALID_AMINO):
        sequences.append( prot.Protein(title.split(None, 1)[0],
                                        is_toxic, len(sequence), split_seq(sequence)) )
  return sequences


# ATHCLEY VALUES
# ---------------------------------------

def get_atchley_values_list(aminos:List[str], idx:int) -> List[int]:
  """Returns all atchley values in a list for a specific amino acid."""
  return [float(cfg.DICT_ATCHLEY.get(i)[idx]) for i in aminos]

def get_atchley_values_raw(sequence, seq_dict_r):
  """Returns raw atchley values in a dictionary."""
  seq_dict_r['f1'] = get_atchley_values_list(sequence, 0)
  seq_dict_r['f2'] = get_atchley_values_list(sequence, 1)
  seq_dict_r['f3'] = get_atchley_values_list(sequence, 2)
  seq_dict_r['f4'] = get_atchley_values_list(sequence, 3)
  seq_dict_r['f5'] = get_atchley_values_list(sequence, 4)

# -----------------------------------------------

def get_change_list(atchley_list):
  """Calculates sequential change for single atchley value."""
  atchley_list.insert(0, 0)
  change_list = [i for i in (np.diff(atchley_list))]
  atchley_list.pop(0)
  return change_list

def get_atchley_diff(seq_dict_r, seq_dict_d):
  """Returns the sequential change for each atchley value as a dictionary."""
  seq_dict_d['f1_d'] = get_change_list(seq_dict_r.get('f1'))
  seq_dict_d['f2_d'] = get_change_list(seq_dict_r.get('f2'))
  seq_dict_d['f3_d'] = get_change_list(seq_dict_r.get('f3'))
  seq_dict_d['f4_d'] = get_change_list(seq_dict_r.get('f4'))
  seq_dict_d['f5_d'] = get_change_list(seq_dict_r.get('f5'))
  
def append_atchley_values(proteins_list):
  """Appends the atchley values to the dictionary of a ProteinSequence object."""
  for protein in proteins_list:
    get_atchley_values_raw(protein.sequence, protein.seq_dict_raw)
    get_atchley_diff(protein.seq_dict_raw, protein.seq_dict_diff)
    

# MATRICES VALUES
# ---------------------------------------

def get_matrix_values(seq_dict):
  """Returns matrix from input dictionary."""
  return np.array([seq_dict[i] for i in seq_dict.keys()])


def update_matrices(protein_seq_list):
  """Updates both matrices."""
  for protein in protein_seq_list:
    protein.matrix_raw = get_matrix_values(protein.seq_dict_raw)
    protein.matrix_diff = get_matrix_values(protein.seq_dict_diff)
    
def append_proteins(proteins):
  """Appends Atchley values to the Protein object matrices."""
  append_atchley_values(proteins)
  update_matrices(proteins)
  pickle_method(cfg.f_train_proteins, 'wb', proteins)
  

def proteins_to_df(proteins):
  """Returns a DataFrame from a list of proteins."""
  df = pd.DataFrame.from_records([p.to_dict() for p in proteins])
  pickle_method(cfg.f_train_df, 'wb', df)
  return df
  


# SPLTITING FUNCIONS
# -----------------------------------------------------------------------------

def get_kfold_splits(fname, x_features, y_labels):
  """Returns stratified shuffle cross validation splits from training dataset."""
  fold_dict = {}
  i = 1
  sss = StratifiedShuffleSplit(n_splits=cfg.K_FOLDS, test_size=cfg.VAL_SIZE,
                               random_state=cfg.RANDOM_SEED)
  print(sss)
  print(f'Number of k-fold splits: {sss.get_n_splits()}')
  for train_idx, val_idx in sss.split(x_features, y_labels):
    x_train, x_val = x_features.iloc[train_idx], x_features.iloc[val_idx]
    y_train, y_val = y_labels.iloc[train_idx], y_labels.iloc[val_idx]
    fold_dict[str(i)] = [x_train, x_val, y_train, y_val]
    i += 1
  pickle_method(fname, 'wb', fold_dict)
  return fold_dict