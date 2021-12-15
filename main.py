from libraries import *
from helper_functions import *

#gathering input details
start_time = time.time()
input_details = form_dictionaries("inputs")
end_time = time.time()
print("Time taken to read the input file data is {}".format(end_time - start_time))

#gathering output details
start_time = time.time()
output_details = form_dictionaries("outputs")
end_time = time.time()
print("Time taken to read the output file data is {}".format(end_time - start_time))

#total details present in input and output dictionary
print("Total details in input dict is: {}".format(len(input_details)))
print("Total details in output dict is: {}".format(len(output_details)))

#merge input and output dictionary
start_time = time.time()
for key, value in output_details.items():
    input_dict = input_details[key]
    output_details[key]["input"] = input_dict["input"]
end_time = time.time()
print("Time taken to link the data is {}".format(end_time - start_time))

#sorted dictionary in order of time
updated_dict = dict(sorted(output_details.items(), key=lambda item: item[1]['time']))


def main():

    #get all the hashes from the input file as it contains transaction hashes
    hashes = get_all_hashes_set("inputs")

    #create mappings
    hash_mappings = {hash : id for id, hash in enumerate(hashes)}

    #update the files using hash_mappings
    #for inputs
    update_all_files("inputs", hash_mappings)

    #for outputs
    update_all_files("outputs", hash_mappings)

    # if CONSTRUCT_ENTIRE_NETWORK:
    #     start_time = time.time()
    #     #construct entire network 
    #     construct_entire_network()
    #     end_time = time.time()
    #     print("Time taken to construct the whole network is {}".format(end_time - start_time))

    #divide the network in 24 hr windows
    get_all_24_hrs_window()

if __name__ == "__main__":
  main()