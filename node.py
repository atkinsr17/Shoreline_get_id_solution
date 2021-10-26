import random
import time
import math



# function that gets the current time since the epoch in ms
def timestamp():
    return math.floor(time.time() * 100)

# Class created to simulate a node.
# The my_id field simulates what the node's id would be.
# The unique_id_suffix is initalized to the last suffix of the node plus one, 
#   or the last four digits of the current timestamp (if system is starting up), modulo 10000. 
#   Upon each successful call to get_id(), the unique_id_suffix is incremented by one,
#   enabling that any one node to create up to 10,000 unique ids per ms, or 10,000,000 ids per sec
class Node:
    def __init__(self, last_suffix):
        self.my_id = random.randint(0, 1024)
        if(last_suffix == None):
            self.unique_id_suffix = timestamp() % 10000
        else:
            self.unique_id_suffix = last_suffix + 1 % 10000

    def node_id(self):
        return self.my_id

    def get_unique_id_suffix(self):
        curr_suffix =  self.unique_id_suffix
        self.unique_id_suffix = self.unique_id_suffix + 1
        return curr_suffix % 10000

    # My get_id uses the current timestamp (in ms), the id of the node 
    #   generating the id, and a four digit suffix that is related to the timestamp
    #   of the system startup and the number of ids that a node has generated

    # id (20 digits) broken down into following sections:
    #   - timestamp (ms): first 12 digits
    #   - node id: next 4 digits 
    #   - suffix: last 4 digits
    #
    # Given the clear breakdown of the fields that go into my id generation, isolating 
    #   and solving a software defect should be fairly simple. 
    # 
    # The timestamp portion of the ids gurantees uniqueness for every ms of get_id() calls.
    # The node id gurantees uniqueness between the 1025 nodes for each ms of get_id() calls.
    # The id suffix gurantees uniqueness for up to 10,000 ids per ms (10,000,000 ids/sec) per node:
    #     - The id suffix is in the range [0000, 9999] and is initialized to the last four digits 
    #           of the timestamp of the system startup. After each successful call to a node's get_id(), the 
    #           suffix is incremented by one.
    #     - When a node crashes and a new one is spun up, the last id suffix of the crashed node is passed into
    #           the construction of the new node, where it is incremented to ensure uniqueness. 
    #  
    # My get_id() function gurantees uniqueness after the system fails and restarts if one of the 
    #    folowing hold: 
    #        * The time it takes for the system to restart >= 1 ms, in which case the timestamp portion of 
    #            my get_id() function ensures uniqueness 
    #        * (The number of ids generated by a given node % 10000) != (ms that system has been running % 10000).
    #            This holds becuase of the way the id suffix is initiated and maintained.
    #
    def get_id(self):
        unique_id = 0

        # timestamp is occupies the first portion of the id, 
        #   so shift to the left 8 decimal places
        timestamp_multiplier = 100000000

        # the node's id occupies the second portion of the id,
        #   so shift to the left 4 decimal places
        node_id_multiplier = 10000

        timestamp_portion = timestamp() * timestamp_multiplier
        node_id_portion = self.node_id() * node_id_multiplier
        suffix_portion = self.get_unique_id_suffix()

        # aggregate portions to get the final unique id
        unique_id = timestamp_portion + node_id_portion + suffix_portion

        return unique_id




        
        

# Used for testing - test successful
if __name__ == '__main__':
    nodes = []
    for i in range(0, 10):
        new_node = Node(None)
        nodes.append(new_node)

    ids = set()

    num_tests = 100000

    for i in range (0, num_tests):
        for j in range(0, 10):
            curr_node = nodes[j]
            curr_id = curr_node.get_id()
            if(curr_id in ids):
                print('DUPLICATE ID: ' + str(curr_id))
            else:
                ids.add(curr_id)
                
    print('Done')
