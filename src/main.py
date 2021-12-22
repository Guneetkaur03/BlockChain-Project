# -*- coding: utf-8 -*-
"""
    Main Module for the project
    This is the driver of the whole project,
    execution of all the steps is performed here
"""

from libs import *
from model import *
from feature_extraction import *
from helper_functions import *
from data_generator import *

def main():
    """
        This module is the driver method of the project.
        It performs the three macro steps assigned, which are
            Step1 : Building BlockChain Network
            Step2 : Extracting Features from the Graph
            Step3 : ML Model Training employing the extracted features

        Args:
            (None)
        Returns:
            (None)
    """

    #Step1 : Building BlockChain Network
    #for building the blockchain network, we need updated_dict(now named as whole_network_dict)
    logging.info('step-1 of building blockchain network')
    whole_network_dict = get_entire_network_details()
    logging.info('generated whole dictionary for the network')

    if BUILD_NETWORK:
        start_time = time.time()
        build_entire_network(whole_network_dict)
        end_time = time.time()
        logging.info("Time taken to construct the whole network is {:.2f}".format(end_time - start_time))
   
    # Step2 : Extracting Features from the Graph
    logging.info('step-2 of extracting features from the network')
    extract_address_features(whole_network_dict)

    # Step3 : Training employing the extracted features
    """[+] Step 3.1 Merge Dataframes if monthly features obtained"""
    combined_df = merge_monthly_datasets()
    #save the combined df
    combined_df.to_csv(FEATURES_FOLDER + 'features.csv')
    logging.info('step 3.1 - Dataset Merged')
    
    combined_df.label.value_counts().plot(kind = 'bar')
    plt.savefig(PLOTS + 'value-counts.png')

    """[+] Step 3.2 Model Training using expanding window"""
    model_training(combined_df)
    logging.info('step 3.2 - Model Trained and Scores Reported')

if __name__ == "__main__":
    # run main
    main()