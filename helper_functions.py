from constants import *
from libraries import *

def get_all_hashes_set(file_type):
    """
        This function is used to get all the hashes across all months

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
        This function is used to update all the files of given type

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
        This function is used to unique hashes for a given month

        Args:
            file_type (str): "inputs" if dealing with input file, else "outputs"
            month (int): value for month
        Returns:
            (set): set of hashes for given month
    """
    hashes = set()

    #reading of files depending on the type and month of data
    filename = DATA_PATH + file_type + YEAR + "_{}.txt".format(str(month+1))

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
        This function is used to update file for given month

        Args:
            file_type (str): "inputs" if dealing with input file, else "outputs"
            month (int): value for month
            hash_mappings (dict): dictionary storing hash:id mapping
    """

    #read files
    filename = DATA_PATH + file_type + YEAR + "_{}.txt".format(str(month+1))
    updated_filename = UPDATED_DATA_PATH + file_type + YEAR + "_{}.txt".format(str(month+1))

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
        This function is used to create dictionaries for all month

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
        This function is used to extract the transaction details

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
    filename = UPDATED_DATA_PATH + file_type + YEAR + "_{}.txt".format(str(month+1))

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

def get_all_24_hrs_window():
    