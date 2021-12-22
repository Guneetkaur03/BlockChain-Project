# -*- coding: utf-8 -*-
"""
    Libs Module for the project
    One place for all the requirements and then 
    use it everywhere.
    This has all the libs to be used in the project
"""

import logging
from typing import *
import os, csv, time
from tqdm import tqdm
from datetime import datetime
from joblib import Parallel, delayed

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from igraph import *
import networkx as nx
from stellargraph import StellarGraph

import numpy as np
import pandas as pd
from numpy import testing

import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, accuracy_score,\
                            classification_report, confusion_matrix, f1_score,\
                            precision_recall_curve, PrecisionRecallDisplay
