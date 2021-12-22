# -*- coding: utf-8 -*-
"""
    This module holds method to merge multiple
    months data into one

"""
from libs import *
from constants import *


def merge_monthly_datasets() -> pd.DataFrame:
    """
        This module merges monthly dataframes in one

        Args:
            (None)
        Returns:
            (dataframe) : pandas combined dataframe for entire year
    """

    # read the first dataframe as combined dataframe and merging with remaining
    combined_df = pd.read_csv(FEATURES_FOLDER + 'features-2013-1.csv', index_col=None)

    # drop addresss as it is not required for training
    combined_df = combined_df.drop(columns=['address'])

    # set index as day column
    combined_df = combined_df.set_index('day')

    # maintain a day count as we progress across months
    day_count = max(set(combined_df.index))

    # gather all csv_files month wise
    for month in range(1, MONTH):

        feature_csv_filepath = FEATURES_FOLDER + 'features-2013-' + str(month+1) + '.csv'
        df = pd.read_csv(feature_csv_filepath, index_col=None)

        # drop addresss as it is not required for training
        df = df.drop(columns=['address'])

        # set index as day column
        df = df.set_index('day')

        # increment its index by day_count
        df.index += day_count

        # merging 
        combined_df = pd.concat([combined_df, df], axis=0)

        # update day_count
        day_count = max(set(df.index))

    return combined_df