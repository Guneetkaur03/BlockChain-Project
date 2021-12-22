# -*- coding: utf-8 -*-
"""
    Helper Fuctions Module for the project
    This file defines the methods to aid for hashes extraction
    and retrival and feature extaction
    Arguments are explained in (Args:)
    Return types are explained in (Returns:)

"""

from libs import *
from constants import *
from feature_extraction import *


#method definitions

def get_entire_network_details() -> Dict[str, Dict[str, str]]:
    """
        Step-1
        This module extracts all details for the network

        Args:
            (None)
        Returns:
            (dict) : containing details of the network        
    """

    """[+] Step 1.1 Extracting hashes"""
    # get all the hashes from the input file as it contains transaction hashes
    hashes = get_all_hashes_set("inputs")
    logging.info('step 1.1 - Hashes Obtained')

    
    """[+] Step 1.2 Creating Mappings"""
    hash_mappings = {hash : id for id, hash in enumerate(hashes)}
    logging.info('step 1.2 - Mappings Created')

    
    """[+] Step 1.3 Updating Files"""
    update_input_output_files(hash_mappings)
    logging.info('step 1.3 - Files Updated')

    
    """[+] Step 1.4 Making Input and Output Dictionaries"""
    input_details, output_details = form_input_output_dictionaries()
    logging.info('step 1.4 - Dictionaries formed')

    
    # log size of the input and output dictionaries
    logging.info("total details in input dict is: {}".format(len(input_details)))
    logging.info("total details in output dict is: {}".format(len(output_details)))

    
    """[+] Step 1.5 Merging in one"""
    start_time = time.time()
    for key, value in output_details.items():
        input_dict = input_details[key]
        output_details[key]["input"] = input_dict["input"]
    end_time = time.time()
    logging.info("data linked in {:.2f} seconds".format(end_time - start_time))

    
    """[+] Step 1.6 Sort the Dictionary wrt time""" 
    updated_dict = dict(sorted(output_details.items(), key=lambda item: item[1]['time']))
    logging.info('step 1.6 - Dictionary sorted')

    return updated_dict


def form_input_output_dictionaries() -> Tuple[Dict[str, Dict[str, str]],  Dict[str, Dict[str, str]]]:
    """
        This module is used to form both input and output dictionaries

        Args:
            (None)
        Returns:
            (tuple): input and output details dictionaries
            
    """

    # gathering input details
    start_time = time.time()
    input_details = form_dictionaries("inputs")
    end_time = time.time()
    logging.info('input file data read in {:.2f} seconds'.format(end_time - start_time))

    # gathering output details
    start_time = time.time()
    output_details = form_dictionaries("outputs")
    end_time = time.time()
    logging.info('output file data read in {:.2f} seconds'.format(end_time - start_time))

    return (input_details, output_details)



def update_input_output_files(hash_mappings: Dict[str, int]) -> None:
    """
        This module updates both input and output files

        Args:
            hash_mappings (dict): hash to id mapping
        Returns:
            (None)
    """

    # for inputs
    update_all_files("inputs", hash_mappings)

    # for outputs
    update_all_files("outputs", hash_mappings)



def get_all_hashes_set(file_type: str) -> Set[str]:
    """
        This module extracts all the hashes of all the months

        Args:
            file_type (str): "inputs/outputs" depending on the file

        Returns:
            (set): set of all hashes
    """
    hashes = set()
    # run the loop parallely 
    # setting jobs -1 to use all the CPUs
    print("\nExtracting hashes")
    hashes_inp = Parallel(n_jobs=-1)(delayed(get_hashes)(file_type, i)\
                                    for i in tqdm(range(MONTH)))
    
    # add them to the set
    for inp in hashes_inp:
        for hash in inp:
            hashes.add(hash)

    return hashes


def update_all_files(file_type: str, hash_mappings: Dict[str, int]) -> None:
    """
        This module updates all the files of a given type

        Args:
            file_type (str): "inputs/outputs" depending on the file
            hash_mappings (dict): hash to id mapping
       
        Returns:
            (None)
    """

    # create an updated folder if it doesn't exist 
    if not os.path.exists(UPDATED_DATA_PATH):
        os.makedirs(UPDATED_DATA_PATH)

    # loop over all the months
    print("\nUpdating {} files".format(file_type))
    for month in tqdm(range(MONTH)):
        update_files(file_type, month, hash_mappings)


def get_hashes(file_type: str, month: int) -> Set[str]:
    """
        This module creates unique hashes for a given month

        Args:
            file_type (str): "inputs/outputs" depending on the file
            month (int): enumerated value for a month
        Returns:
            (set): set of hashes for a given month
    """
    hashes = set()

    # read the file
    filename = DATA_PATH + file_type + str(YEAR) +\
                             "_{}.txt".format(str(month + 1))

    try:
        with open(filename) as file:
            for line in file:
                # split by tab char to get the details present
                details = line.split("\t")

                # get other hashes
                other_hashes = details[2:]

                # hash present at the second value
                hashes.add(details[1])
                
                # looping over other hashes
                for i in range(0, len(other_hashes), 2):
                    hashes.add(other_hashes[i])

    except Exception as e:
        logging.ERROR(e)
    
    return hashes



def update_files(file_type: str, month: int, hash_mappings: Dict[str, int]) -> None:
    """
        This module updates file for given month wherein hashes are replaced with id's

        Args:
            file_type (str): "inputs/outputs" depending on the file
            month (int): enumerated value for a month
            hash_mappings (dict): hash to id mapping
        Returns:
            (None)
    """

    # read the files
    filename = DATA_PATH + file_type + str(YEAR) + "_{}.txt".format(str(month+1))
    updated_filename = UPDATED_DATA_PATH + file_type + str(YEAR) + "_{}.txt".format(str(month+1))

    file = open(filename, 'r')
    updated_file = open(updated_filename, 'w')

    contents = file.readlines()

    for line in contents:

        details = line.split("\t")

        # update the details
        updated_details = [ str(hash_mappings.get(item, item))\
                            for item in details ]
    
        # write it in an updated file
        updated_file.write('\t'.join(updated_details))
    
    # close the files
    file.close()
    updated_file.close()


def form_dictionaries(file_type: str) -> Dict[str, Dict[str, str]]:
    """
        This module creates dictionaries for all the months

        Args:
            file_type (str): "inputs/outputs" depending on the file
            month (int): enumerated value for a month
        Returns:
            (dict): complete dictionary containing details for all months
    """
    details = dict()
    print("\nCreating {} dictionaries".format(file_type))
    inputs  = Parallel(n_jobs=-1)( delayed(extract_transaction_details)(file_type, i)\
                                   for i in tqdm(range(MONTH)))
    for inp in inputs:
        details.update(inp)
    return details

def build_entire_network(whole_network_dict):

    #create a directed graph
    g = nx.DiGraph()

    print("\nBuilding Network")
    for key, value in tqdm(whole_network_dict.items()):

        hash_of_transc = key
        
        input_details_of_hash_of_transc = value["input"]
        
        #going over all input transactions
        for i in range(0, len(input_details_of_hash_of_transc), 2):
            
            input_hash = input_details_of_hash_of_transc[i]
            output_index = input_details_of_hash_of_transc[i+1]
            
            if input_hash not in whole_network_dict.keys():
                pass
            else:

                get_amounts = whole_network_dict[input_hash]["output"]
                
                address = get_amounts[int(output_index)]
                amount = get_amounts[2*int(output_index)+1]
                
                #add input transaction node
                g.add_node(input_hash, s='o', label='transaction', color="r")
                
                #add address node
                g.add_node(address, s ='s', label='address', color="b")
                
                #add output transaction node
                g.add_node(hash_of_transc, s='o', label='transaction', color="r")
                
                #add edge between input transaction and address
                g.add_edge(input_hash, address, weight=int(amount))
                
                #add edge between address and output transaction
                g.add_edge(address, key, weight=int(amount))


    if GET_NETWORK_INFO:
        print("\nGraph information is")
        graph_info = StellarGraph.from_networkx(g)
        print(graph_info.info())

    #plot the network
    plot_network(g)


def extract_address_features(whole_network_dict):
    """
        This module divides the network in 24 hr windows and extracts features

        Args:
            file_type (str):  "inputs/outputs" depending on the file
            month (int): enumerated value for a month
        Returns:
            (dict): nested dictionary with transaction details 
                    [hash, dictonary(keys: inputs, outputs, time)] 
    """

    """[+] Step 2.1 Divide the network""" 
    # divide the network into 24 hr windows
    start_time    = time.time()
    batches_24_hr = get_all_24_hrs_window(whole_network_dict)
    end_time      = time.time()
    logging.info("step 2.1 network divided into 24hr windows in {:.2f} seconds".format(end_time - start_time))

    """[+] Step 2.2 Extracting Features"""
    # extract features and write in file
    start_time = time.time()
    get_features(batches_24_hr, whole_network_dict)
    end_time = time.time()
    logging.info("step 2.2 features extracted in {:.2f} seconds".format(end_time - start_time))


def extract_transaction_details(file_type: str, month: int) -> Dict[str, Dict[str, str]]:
    """
        This module extracts the transaction details

        Args:
            file_type (str):  "inputs/outputs" depending on the file
            month (int): enumerated value for a month
        Returns:
            (dict): nested dictionary with transaction details 
                    [hash, dictonary(keys: inputs, outputs, time)] 
    """
    # create a dictionary to store the transaction_details
    trx_details = dict()

    # read the file
    filename = UPDATED_DATA_PATH + file_type + str(YEAR) + "_{}.txt".format(str(month+1))

    with open(filename) as file:

        # iterating over lines
        for line in file:

            # split tab character to get details
            line = line.replace('\n', '')
            details = line.split("\t")

            # adding details in the dictionary
            hash_of_trx = details[1]
            trx_details[hash_of_trx] = dict()

            # add input details
            if file_type == "inputs":
                trx_details[details[1]]["input"]  = details[2:]

            # add output details
            if file_type == "outputs":
                trx_details[details[1]]["output"] = details[2:]
                trx_details[details[1]]["time"]   = details[0]

    return trx_details


def get_all_24_hrs_window(details: Dict[str, Dict[str, str]]) -> Dict[int, Dict[str, str]]:
    """
        This module divides the data into batches of 24hr enteries

        Args:
            details (dict): contains network details in timely order
        Returns:
            (dict): 24hr window batches
    """
    batches_24_hr = dict()

    # loop over 24hr timeframe
    print("\nDividing the data into 24hr windows")
    for day, unixtimestamp in tqdm(enumerate(range(UNIXTIMESTAMP_START, UNIXTIMESTAMP_END, TIMEFRAME_24HR))):
        
        u_start = unixtimestamp
        u_end   = unixtimestamp + TIMEFRAME_24HR

        batches_24_hr[day] = dict()

        # add an entry to that day if the start/end time lies in the limits
        for key, value in details.items():     
            if int(value['time']) >= u_start and int(value['time']) <= u_end:
                batches_24_hr[day][key] = value
        
    return batches_24_hr



def get_features(batches_24_hr: Dict[int, Dict[str, str]], updated_dict: Dict[str, Dict[str, str]]) -> None:
    """
    This module extracts features from 24hr windows

    Args:
        batches_24_hr (dict): batches of 24hr windows
        updated_dict (dict): sorted dictionary containing all details
    Returns:
            (None)
    """

    # create an folder for features data if it doesn't exist 
    if not os.path.exists(FEATURES_FOLDER):
        os.makedirs(FEATURES_FOLDER)

    # log 
    logging.info('step 2.2.1 - created features folder')

    # open the file to write
    features_filename = FEATURES_FOLDER + 'features_' + str(YEAR) + ".csv"
    f = open(features_filename, 'w')

    # create the csv writer
    writer = csv.writer(f)
    # write the header row
    writer.writerow(['day', 'address', 'income', 'expenditure', 'neighbors', 'lengths', 'counts', 'loops', 'label'])
    # log 
    logging.info('step 2.2.2 - created features csv')

    day = 0

    ransom_addresses = get_ransom_addresses()

    # loop for each day
    print("\nExtracting feature daywise")
    for m_key, m_value in tqdm(batches_24_hr.items()):

        day += 1
        details = m_value

        #create netwrokx graph
        g = nx.DiGraph()
        
        # maintains the labels (0: white 1: rest)
        label_list = []
    
        non_address_set = set()

        # loop in dictionary of a day
        for key, value in details.items():
            
            hash_of_transc = key

            input_details_of_hash_of_transc = value["input"]

            #print("Transaction input details {}".format(input_details_of_hash_of_transc))
            #print("Transaction output details {}".format(output_details_of_hash_of_transc))

            # looping over all input details
            for i in range(0, len(input_details_of_hash_of_transc), 2):
                input_hash   = input_details_of_hash_of_transc[i]
                output_index = input_details_of_hash_of_transc[i+1]
                
                # do nothing
                if input_hash not in updated_dict.keys():
                    pass
                else:
                    # get output details of that input transaction
                    get_amounts = updated_dict[input_hash]["output"]

                    address = get_amounts[2*int(output_index)]
                    amount  = get_amounts[2*int(output_index)+1]
                    
                    # if not a ransom address
                    if address not in ransom_addresses:
                        if len(non_address_set) < ADDRESS_NODES_LIMIT and address not in non_address_set:
                            non_address_set.add(address)
                            label_list.append(0) #append white
                        else:
                            continue
                    else:
                        label_list.append(1) #append dark

                    # add input transaction node
                    g.add_node(input_hash, s='s', label='transaction', color="r", time=time)
                                
                    # add address node
                    g.add_node(address, s='s', label='address', color="b")

                    # add output transaction node
                    g.add_node(hash_of_transc, s='o', label='transaction', color="r", time=time)
                    
                    # add edge between input transaction and address
                    g.add_edge(input_hash, address, weight=int(amount))

                    # add edge between address and output transaction
                    g.add_edge(address, key, weight=int(amount))
                

        # convert to igraph for faster computations
        ig = Graph.from_networkx(g)
    
        # pick only address nodes
        addr_list  = [node for node in ig.vs.indices if ig.vs[node]['label'] == "address"]

        # pick only transaction nodes 
        trans_list = [node for node in ig.vs.indices if ig.vs[node]['label'] == "transaction"]

        # get incomes feature
        income_list = get_income(ig, addr_list)

        # get expenditure feature
        expenditure_list = get_expenditure(ig, addr_list)

        # get starter transactions
        starter_trx = get_starter_trx(ig, trans_list)

        # get neighbors
        neighbor_list = get_neighbors(ig, addr_list)

        # get length, loop and count
        length_list  = []
        count_list = []
        loops_list = []
        inp = Parallel(n_jobs=-1)(delayed(get_length_count_loop)(ig, addr, starter_trx)\
                                 for addr in addr_list)
        # segregate lists
        for d in inp:
            length_list.append(d[0])
            count_list.append(d[1])
            loops_list.append(d[2])
        
        for i in range(len(addr_list)):
            # append rows in features file
            writer.writerow([day, ig.vs[addr_list[i]]["_nx_name"], income_list[i], \
                         expenditure_list[i], neighbor_list[i], length_list[i], \
                         count_list[i], loops_list[i], label_list[i]])

        # log after completion of 30 days
        if day % 30 == 0:
            logging.info('step 2.2.3 - features extracted for {} days'.format(day))
    
    # log 
    logging.info('step 2.2.4 - populated features csv')


def get_ransom_addresses() -> List[str]:
    """
        This module returns the list of ransom addresses

        Args:
            (None)
        Returns:
            (list) : ransomware addresses
    """
    df_ransom = pd.read_csv(RANSOM_ADDRESSES_FILE)

    return list(df_ransom.address.values)


def get_truncated_address_list(g: Graph, addresses: List[int], n: int = 1000) -> List[int]:
    """
        This module checks the addresses in the list and picks all the
        ransoms. For non-ransoms it trancates it to n entries

        Args:
            g (graph) : iGraph object
            addresses (list) : list of addresses
            n (int) : number of entries for non ransom addresses
        Returns:
            (list): list of truncated addresses
    """
    ransom           = []
    non_ransom       = []
    ransom_addresses = get_ransom_addresses()
    
    # loop around the address nodes
    for address in addresses:
        # check if the address is a ransom
        if g.vs[address]["_nx_name"] in ransom_addresses:
            ransom.append(address)
        else:
            non_ransom.append(address)

    if len(ransom) > 0:
        print(len(ransom))

    # truncate non_ransom and pick all ransoms
    all_addresses = non_ransom[:n]
    all_addresses.extend(ransom)

    return all_addresses


def plot_network(g):
    """
        This module is used to plot and save network graph

        Args:
            g (graph): graph object
        Returns:
            (None)
    """
    plt.figure(figsize=(20, 10))

    nodePos = nx.layout.spring_layout(g)

    nodeShapes = set((aShape[1]["s"] for aShape in g.nodes(data = True)))

    for aShape in nodeShapes:
        nx.draw_networkx_nodes(g,nodePos, node_shape = aShape, nodelist = [sNode[0]\
                            for sNode in filter(lambda x: x[1]["s"]==aShape,g.nodes(data = True))])

    #draw the edges between the nodes
    nx.draw_networkx_edges(g,nodePos)

    #draw labels
    nx.draw_networkx_labels(g, nodePos)
    
    plt.savefig(PLOTS + 'network.png')

