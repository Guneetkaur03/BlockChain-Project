# -*- coding: utf-8 -*-
"""
    Constants Module for the project
    Here all the constants have been listed
    that would be used all over the project

"""

from libs import *

# number of months
MONTH = 12

# year of the dataset
YEAR  = 2013

# path of the datasets
DATA_PATH = './data/edges' + str(YEAR) + '/'
UPDATED_DATA_PATH = DATA_PATH + 'updated/'
FEATURES_FOLDER = './data/features/'
RANSOM_ADDRESSES_FILE = './data/ransom_only.csv'

# plots folder
PLOTS = './plots/'

# logging file
LOG_FOLDER = './logs/'
# create an folder for logs 
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)
# Creating a Logger
logging.basicConfig(filename=LOG_FOLDER + 'logs.log',\
    level=logging.INFO, format='%(asctime)s |  %(levelname)s | %(message)s')

# set time limits
START_DAY = datetime(YEAR, 1, 1)
UNIXTIMESTAMP_START = int((START_DAY - datetime(1970,1,1)).total_seconds())

# for a complete year the upper bound would be 
# first day of the next year
if MONTH == 12:
    END_DAY = datetime(YEAR+1,1,1)
else:
    END_DAY = datetime(YEAR,MONTH+1,1)
UNIXTIMESTAMP_END = int((END_DAY - datetime(1970,1,1)).total_seconds())

# 24hr unix time
TIMEFRAME_24HR = 24 * 60 * 60

# number of address nodes reqd
ADDRESS_NODES_LIMIT = 200

# buid a complete network
BUILD_NETWORK = True

#get network info
GET_NETWORK_INFO = False