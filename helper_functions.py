import os
import csv
import time
import pandas as pd
from igraph import *
import networkx as nx
from tqdm import tqdm
from constants import *
from datetime import datetime
from helper_functions import *
from feature_extraction import *
from joblib import Parallel, delayed

def get_all_hashes_set(file_type):
    """
        This module is used to get all the hashes across all months

        Args:
            file_type (str): "inputs" if dealing with input file, else "outputs"

        Returns:
            (set): set of all hashes
    """
    hashes = set()
    hashes_inp = Parallel(n_jobs=-1)(delayed(get_hashes)(file_type, i) for i in tqdm(range(MONTH)))
    
    for inp in hashes_inp:
        for hash in inp:
            hashes.add(hash)

    return hashes

def update_all_files(file_type, hash_mappings):
    """
        This module is used to update all the files of given type

        Args:
            file_type (str): "inputs" if dealing with input file, else "outputs"
            hash_mappings (dict): dictionary storing hash:id mapping
    """

    #create a updated folder if doesn't exist to store the updated text files
    if not os.path.exists(UPDATED_DATA_PATH):
        os.makedirs(UPDATED_DATA_PATH)

    #loop over all the months
    for month in tqdm(range(MONTH)):
        update_files(file_type, month, hash_mappings)


def get_hashes(file_type, month):
    """
        This module is used to unique hashes for a given month

        Args:
            file_type (str): "inputs" if dealing with input file, else "outputs"
            month (int): value for month
        Returns:
            (set): set of hashes for given month
    """
    hashes = set()

    #reading of files depending on the type and month of data
    filename = DATA_PATH + file_type + str(YEAR) + "_{}.txt".format(str(month+1))

    with open(filename) as file:

        for line in file:

            #split by tab char to get the details present
            details = line.split("\t")

            other_hashes = details[2:]

            #hash present at the second value
            hashes.add(details[1])
            
            #looping over other hashes
            for i in range(0, len(other_hashes), 2):
                hashes.add(other_hashes[i])
    
    return hashes


def update_files(file_type, month, hash_mappings):
    """
        This module is used to update file for given month

        Args:
            file_type (str): "inputs" if dealing with input file, else "outputs"
            month (int): value for month
            hash_mappings (dict): dictionary storing hash:id mapping
    """

    #read files
    filename = DATA_PATH + file_type + str(YEAR) + "_{}.txt".format(str(month+1))
    updated_filename = UPDATED_DATA_PATH + file_type + str(YEAR) + "_{}.txt".format(str(month+1))

    file = open(filename, 'r')
    updated_file = open(updated_filename, 'w')

    contents = file.readlines()

    for line in contents:

        details = line.split("\t")

        #update the details
        updated_details = [str(hash_mappings.get(item, item))  for item in details]
    
        #write in updated file
        updated_file.write('\t'.join(updated_details))
    
    #closing
    file.close()
    updated_file.close()


def form_dictionaries(file_type):
    """
        This module is used to create dictionaries for all month

        Args:
            file_type (str): "inputs" if dealing with input file, else "outputs"
            month (int): value for month

        Returns:
            (dict): complete dictionary containing details for all months
    """
    details = dict()
    inputs = Parallel(n_jobs=-1)(delayed(extract_transaction_details)(file_type, i) for i in tqdm(range(MONTH)))
    for inp in inputs:
        details.update(inp)
    return details


def extract_transaction_details(file_type, month):
    """
        This module is used to extract the transaction details

        Args:
            file_type (str): "inputs" if dealing with input file, else "outputs"
            month (int): value for month

        Returns:
            (dict): nested dictionary containing transaction details with 
                    key as the hash and values as dictonary containing inputs, outputs and time 
    """
    #create a dictionary to store the transaction_details
    trx_details = dict()

    #reading of files depending on the type and month of data
    filename = UPDATED_DATA_PATH + file_type + str(YEAR) + "_{}.txt".format(str(month+1))

    with open(filename) as file:

        #iterating over lines
        for line in file:

            #split tab character to get details
            line = line.replace('\n', '')
            details = line.split("\t")

            #adding details in the dictionary
            hash_of_trx = details[1]
            trx_details[hash_of_trx] = dict()

            #add input details
            if file_type == "inputs":
                trx_details[details[1]]["input"] = details[2:]

            #add output details
            if file_type == "outputs":
                trx_details[details[1]]["output"] = details[2:]
                trx_details[details[1]]["time"] = details[0]

    return trx_details

# def construct_entire_network():

def get_all_24_hrs_window(details):
    """
        This module is used to form daily batches of 24hr timeframe

        Args:
            details (dict): contains network details in timely order

        Returns:
            (dict): 24hr window batches
    """
    batches_24_hr = dict()

    #loop over 24hr timeframe
    for day, unixtimestamp in tqdm(enumerate(range(UNIXTIMESTAMP_START, UNIXTIMESTAMP_END, TIMEFRAME_24HR))):
        
        u_start = unixtimestamp
        u_end = unixtimestamp + TIMEFRAME_24HR

        batches_24_hr[day] = dict()

        for key, value in details.items():     
            if int(value['time']) >= u_start and int(value['time']) <= u_end:
                batches_24_hr[day][key] = value

    return batches_24_hr


def get_features(batches_24_hr, updated_dict):
    """
    This module is used to extract features from 24hr windows

    Args:
        batches_24_hr (dict): batches of 24hr windows
        updated_dict (dict): sorted dictionary containing all details
    """

    # open the file in the write mode
    f = open(FEATURES_CSV_FILE, 'w')

    # create the csv writer
    writer = csv.writer(f)
    #header row
    writer.writerow(['day', 'address', 'income', 'expenditure', 'neighbors', 'lengths', 'counts', 'loops', 'label'])

    day = 0

    ransom_addresses = get_ransom_addresses()

    for m_key, m_value in tqdm(batches_24_hr.items()):

        day += 1
        details = m_value

        #create graph
        g = nx.DiGraph()

        label_list = []
    
        non_address_set = set()
    
        for key, value in details.items():
            
            hash_of_transc = key

            input_details_of_hash_of_transc  = value["input"]

            #print("Transaction input details {}".format(input_details_of_hash_of_transc))
            #print("Transaction output details {}".format(output_details_of_hash_of_transc))

            #going over all input details
            for i in range(0, len(input_details_of_hash_of_transc), 2):
                input_hash   = input_details_of_hash_of_transc[i]
                output_index = input_details_of_hash_of_transc[i+1]
            
                if input_hash not in updated_dict.keys():
                    pass
                else:
                    #get output details of that input transaction
                    get_amounts = updated_dict[input_hash]["output"]

                    address = get_amounts[2*int(output_index)]
                    amount  = get_amounts[2*int(output_index)+1]
                    
                    if address not in ransom_addresses:
                        if len(non_address_set) < ADDRESS_NODES_LIMIT and address not in non_address_set:
                            non_address_set.add(address)
                            label_list.append(0) #append white
                        else:
                            continue
                    else:
                        #print("Ransomware found")
                        label_list.append(1) #append dark

                    #add input transaction node
                    g.add_node(input_hash, s='s', label='transaction', color="r", time=time)
                                
                    #add address node
                    g.add_node(address, s ='s', label='address', color="b")

                    #add output transaction node
                    g.add_node(hash_of_transc, s='o', label='transaction', color="r", time=time)
                    
                    #add edge between input transaction and address
                    g.add_edge(input_hash, address, weight=int(amount))

                    #add edge between address and output transaction
                    g.add_edge(address, key, weight=int(amount))
                

        #convert to igraph for faster computations
        ig = Graph.from_networkx(g)
    
        #pick address nodes
        addr_list  = [node for node in ig.vs.indices if ig.vs[node]['label'] == "address"]

        #pick only transaction nodes 
        trans_list = [node for node in ig.vs.indices if ig.vs[node]['label'] == "transaction"]

        #get incomes feature
        income_list = get_income(ig, addr_list)

        #get expenditure feature
        expenditure_list = get_expenditure(ig, addr_list)

        #get starter transactions
        starter_trx = get_starter_trx(ig, trans_list)

        #get neighbors
        neighbor_list = get_neighbors(ig, addr_list)

        #get length, loop and count
        length_list  = []
        count_list = []
        loops_list = []
        inp = Parallel(n_jobs=-1)(delayed(get_length_count_loop)(ig, addr, starter_trx) for addr in addr_list)
        for d in inp:
            length_list.append(d[0])
            count_list.append(d[1])
            loops_list.append(d[2])
        
        for i in range(len(addr_list)):
            print("appending")
            #append row in features file
            writer.writerow([day, ig.vs[addr_list[i]]["_nx_name"], income_list[i], \
                         expenditure_list[i], neighbor_list[i], length_list[i], \
                         count_list[i], loops_list[i], label_list[i]])
                         
def get_ransom_addresses():
    """
    This module is used to get the list of ransom addresses

    Returns:
        (list) : ransomware addresses
    """
    filepath = UPDATED_DATA_PATH + 'ransom_only.csv'
    df_ransom = pd.read_csv(filepath)

    return list(df_ransom.address.values)

def get_truncated_address_list(g, addresses, n = 1000):
    """
        This module checks the addresses in the list and picks all the
        ransoms. For non-ransoms it trancates it to n entries
        Args:
            g (graph) : graph object
            addresses (list) : list of addresses
            n (int) : number of entries for non ransom addresses
        Returns:
            (list): list of truncated addresses
    """
    ransom           = []
    non_ransom       = []
    ransom_addresses = get_ransom_addresses()

    for address in addresses:
        if g.vs[address]["_nx_name"] in ransom_addresses:
            ransom.append(address)
        else:
            non_ransom.append(address)

    if len(ransom) > 0:
        print(len(ransom))

    all_addresses = non_ransom[:n]
    all_addresses.extend(ransom)

    return all_addresses
