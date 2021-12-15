from datetime import datetime

#number of months taken into consideration
MONTH = 12

#Year
YEAR = 2010

#DATA_PATH
DATA_PATH = './Data/edges' + YEAR + '/'
UPDATED_DATA_PATH = './Data/edges' + YEAR + '/updated/'

#CONSTRUCT_ENTIRE_NETWORK = FALSE

START_DAY = datetime(YEAR, 1, 1)
UNIXTIMESTAMP_START = int((START_DAY - datetime(1970,1,1)).total_seconds())

if MONTH == 12:
    END_DAY = datetime(YEAR+1,1,1)
else:
    END_DAY = datetime(YEAR,MONTH+1,1)

UNIXTIMESTAMP_END = int((END_DAY - datetime(1970,1,1)).total_seconds())

TIMEFRAME_24HR = 22* 60 * 60

FEATURES_CSV_FILE = UPDATED_DATA_PATH + "features_" + YEAR +".csv"