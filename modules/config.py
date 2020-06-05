# File to define global variables

# links
# TOXIFY: https://github.com/tijeco/toxify
# ToxClassifier: https://github.com/rgacesa/ToxClassifier

import random


RANDOM_SEED = 273

# pre-processing
INVALID_AMINO = ['B', 'J', 'O', 'U', 'X', 'Z']
MAX_SEQ_LEN = 500

# splitting
K_FOLDS = 5
VAL_SIZE = 0.20


# FILEPATHS
# -----------------------------------------------------------------------------

# common paths
PATH_DATA_TRAIN = 'data/datasets/training_data'
PATH_DATA_BENCH = 'data/datasets/benchmark_data'
PATH_DATA_TEST = 'data/datasets/testing_data'
PATH_DATA_REFS = 'data/data_refs'


# MAIN DATA
# -------------------------------------

# training data
f_train_toxic_fasta = PATH_DATA_TRAIN + '/pre.venom.fasta'
f_train_atoxic_fasta = PATH_DATA_TRAIN + '/pre.NOT.venom.fasta'

# benchmark data
f_test_toxic_fasta = PATH_DATA_TRAIN + '/post.venom.fasta'
f_test_atoxic_fasta = PATH_DATA_TRAIN + '/post.NOT.venom.fasta'

#testing data

# processed main data
f_train_proteins = PATH_DATA_TRAIN + '/train_proteins.pickle'
f_train_df = PATH_DATA_TRAIN + '/train_df.pickle'


# REFERENCE DATA
# -------------------------------------
f_aminoacid = PATH_DATA_REFS + '/aminoacids.csv'
f_atchley = PATH_DATA_REFS + '/atchley.txt'

# processed ref data
f_atchley_dict = PATH_DATA_REFS + '/atchley_dict.pickle'
f_atchley_df = PATH_DATA_REFS + '/atchley_df.pickle'


# DATASET SPLITTING
# -------------------------------------

# # k-fold cross validation dictionaries
# f_5_fold_p10 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/5_fold_p10.pickle'
# f_5_fold_p15 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/5_fold_p15.pickle'
# f_5_fold_p20 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/5_fold_p20.pickle'

# f_10_fold_p10 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/10_fold_p10.pickle'
# f_10_fold_p15 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/10_fold_p15.pickle'
# f_10_fold_p20 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/10_fold_p20.pickle'

# f_15_fold_p10 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/15_fold_p10.pickle'
# f_15_fold_p15 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/15_fold_p15.pickle'
# f_15_fold_p20 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/15_fold_p20.pickle'

# f_20_fold_p10 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/20_fold_p10.pickle'
# f_20_fold_p15 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/20_fold_p15.pickle'
# f_20_fold_p20 = PATH_TO_FOLDER + '/pre_processing_files/data_splits/20_fold_p20.pickle'

# MODELS
# -------------------------------------
# f_m_linear_sgd = PATH_TO_FOLDER + '/models/m_linear_sgd.pickle'
# f_m_random_forest = PATH_TO_FOLDER + '/models/m_random_forest.pickle'
# f_m_decision_tree = PATH_TO_FOLDER + '/models/m_decision_tree.pickle'