# -*- coding: utf-8 -*-
"""
    Feature Extraction Module for the project
    This file defines the methods to for feature extracton steps
    All the arguments are type hinted to avoid logical inconsistencies
    Arguments are explained in (Args:)
    Return types are explained in (Returns:)

"""

# import libs for typehinting
from libs import *

def get_income(g: Graph, addresses: List[str]) -> List[int]:
    """
        This module is used to generate income feature
        of the address.
        Income of an address *u* is calculated as the 
        sum amount of all coins output to *u*.

        Args:
            g (graph)       : graph object
            addresses (list): list of id of addresses

        Returns:
            (list): income amounts
    """
    address_income = []

    for address in addresses:
        # find all the predecessor for address
        all_predeccesors = list(g.predecessors(address))

        # loop over all predecessors to compute the incoming sum amount to an address
        # using the weight of incoming edges
        # it generates list of all incoming amounts
        incomes = [g.es[g.get_eid(predecessor,address)]["weight"]\
                   for predecessor in all_predeccesors]

        # store the sum of incoming amount
        address_income.append(sum(incomes))

    return address_income
    

def get_expenditure(g: Graph, addresses: List[str]) -> List[int]:
    """
        This module is used to generate expenditure feature of the addresses.
        Expenditure of an address *u* is calculated as the total amount of 
        coins output from *u*.

        Args:
            g (graph)       : graph object
            addresses (list): list of id of addresses

        Returns:
            (list): expenditure amounts 
    """
    address_expenditure = []

    for address in addresses:

        # find all the successors for address
        all_successors = list(g.successors(address))

        # loop over all successors to compute the expenditure using 
        # the weight of outgoing edges
        # list of all outgoing amounts is generated
        expenditures = [g.es[g.get_eid(address,successor)]["weight"]\
                        for successor in all_successors]

        # store the sum of outgoing amount
        address_expenditure.append(sum(expenditures))

    return address_expenditure


def get_neighbors(g: Graph, addresses: List[str]) -> List[int]:
    """
        This module is used to extract the neighbors feature of an address.
        Neighbors of an address *u* is the number of transactions that
        have *u* as one of its output addresses

        Args:
            g (graph)       : graph object
            addresses (list): list of id of addresses

        Returns:
            (list): list of neighbors
    """
    address_neighbors = []

    for address in addresses:

        # list of all neighbors
        neighbors = [1 for p in g.predecessors(address) \
                    if g.vs[p]['label'] == "transaction"]

        # store the count of neighbors
        address_neighbors.append(len(neighbors))

    return address_neighbors


def get_starter_trx(g: Graph, transactions: List[int]) -> List[int]:
    """
        This module is used to get all the starter transactions in a graph
        These are the set of transactions that do not receive outputs from any 
        previous transaction.

        Args:
            g (graph)          : graph object
            transactions (list): list of transactions

        Returns:
            (list): list of starter transactions
    """

    # if a transaction has no predecessor, 
    # list the transaction as the starter transaction
    starter_trx = [ transaction for transaction in transactions\
                    if not g.predecessors(transaction) ]

    return starter_trx


def get_length_count_loop(g: Graph, address: str, starter_trxs: List[int]) -> Tuple[int, int, int]:
    """
        This function calculates the length, count and loop feature for the given address
        
        Length(*Lu*) of an address *u*, is the number of non-starter transactions
        on its longest chain starting from starter transaction to address

        Count(*Cu*) of an address *u*, is the number of starter transactions 
        which are connected to *u* through a chain

        Loop(*Ou*) of an address *u*, is the number of starter transactions
        which are connected to *u* with more than one directed path

        Args:
            g (graph)          : graph object
            address (str)      : id of address
            starter_trxs (list): list of starter transactions

        Returns:
            (tuple): containing the length, count and loop for given address
    """

    length = 0
    count = 0
    loop = 0

    max_paths = []

    # looping over all starter transactions
    for trx in starter_trxs:
        
        # get all simple paths
        all_paths = g.get_all_simple_paths(trx, address)

        if all_paths != []:

            # increment count as  >=1 paths exist
            count += 1

            # get the maximum length path 
            max_len_path = max(all_paths, key=lambda x: len(x))

            # counting number of non starter transactions existing in
            # the max length chain
            temp = [1 for node in max_len_path \
                        if g.vs[node]['label'] == "transaction"\
                            if node not in starter_trxs ]

            max_paths.append(len(temp))
            
        # if more than one path, increment the loop
        if len(all_paths) > 1: loop += 1

    # get maximum path length
    if max_paths != []:
        length = max(max_paths)

    return (length, count, loop)