import random
import uuid
from Version2.Messages import DIO, DAO
from Version2.Node import Node
from Version2.Connection import Connection
import numpy as np
import math


class Network:
    # constructor
    def __init__(self, env, no_of_nodes: int, neighbor_radius: float, network_type: str):
        self.noOfNodes: int = no_of_nodes
        self.env = env
        self.nodes: [] = self.__define_nodes_in_network(no_of_nodes, network_type)
        self.neighbourRadius: float = neighbor_radius
        self.connections = self.__initialize_neighbours()
        self.removedNodes: [] = []
        self.removedConnections: [] = []
        self.dao_messages: {} = dict()
        self.priority_dao = 'rank'  # First priority of objective function

    def source(self, amountOfMessages, interval):
        """Source generates messages randomly"""
        for i in range(amountOfMessages):
            # make a random node from the network send a random messgage.
            for node in self.nodes:
                # Request the node : wait for the node to become available
                with node.request() as req:
                    yield req
                    booleans: [] = [True, False]
                    boolean = random.choice(booleans)
                    # Now, whether the message is DAO or DIO is selected at random.
                    if boolean:
                        self.env.process(self.send_message_DIO(node, i))
                    else:
                        self.env.process(self.send_message_DAO(node))
            t = interval
            yield self.env.timeout(t)  # wait time 't' before sending a new message.

    # Send a DIO message
    def send_message_DIO(self, node, message_number: int):
        # Create new DIO message
        message = DIO(node.get_rank(), message_number)
        yield self.env.timeout(np.random.randint(1, 10))  # it takes between 1 and 10  seconds to create a dio.

        # Send DIO to each neighbour
        neighbors = self.__find_neighbours(node.get_ID()).copy()
        for neighbor in neighbors:  # get all neighbors

            # Remove node from DODAG if it has no battery power left
            if neighbor.get_battery_power() <= 0:
                self.remove_node_from_network(neighbor)
                # Run local repair for children
                children = self.find_children(neighbor)
                self.local_repair(children)
                continue

            # request neighboring Node from the environment!
            with neighbor.request() as req:
                # Say: Get the node before we timeout!
                results = yield req | self.env.timeout(3)  ## renege after timeout time.
                if req in results:
                    # if this is not None => We got the node!!
                    self.__get_connection_between(node, neighbor).successful_transmission()

                    # We now send out, by calling the Nodes "receive_message" method:

                    yield self.env.process(neighbor.receive_message(message))



                else:
                    # We  did not succesfully get a node before timeout! => reneged
                    self.__get_connection_between(node, neighbor).failed_transmission()

    # Send DAO message
    def send_message_DAO(self, node: Node):
        # Check for Node rank.
        if node.get_rank() is None:
            pass  # if Node doesnt have a rank, it does not know who to send to, as no parents are present.
        else:
            message = DAO(node.get_rank(), node.get_ID())
            yield self.env.timeout(np.random.randint(1, 10))  # it takes between 1 and 10  seconds to create a DAO.
            # determine who to sent to based on objective function in Connection:
            best_neighbor: Node = self.objective_function(node, priority=self.priority_dao)
            if best_neighbor is not None:
                yield self.env.process(best_neighbor.receive_message(message))
                self.dao_messages.update(
                    {node: [best_neighbor, self.__get_connection_between(node, best_neighbor)]})  # For visualization

            else:
                pass

    # Decide which objective function
    def objective_function(self, node, priority: str) -> Node:
        if priority == 'ETX':
            return self.objective_function_ETX(node)
        if priority == 'rank':
            return self.objective_function_rank(node)

    # Implementation of objective function that prioritizes rank. Returns the best parent.
    def objective_function_rank(self, node) -> Node:
        neighbor_nodes: [] = self.__find_neighbours(node.get_ID())
        min_ETX = None  # of type 'float'
        best_neighbor = None  # of type 'Node'
        for neighbor in neighbor_nodes:
            # first routing metric
            if neighbor.get_rank() is not None and node.get_rank() > neighbor.get_rank():  # does neighbor have smaller rank.
                # second routing metric.
                neighbor_connection = self.__get_connection_between(node, neighbor)
                if min_ETX is None or neighbor_connection.get_ETX() < min_ETX:  # Match on ETX
                    min_ETX = neighbor_connection.get_ETX()
                    best_neighbor = neighbor
                else:
                    pass  # neighbor connection has higher ETX and is not best neighbor.
            else:
                pass  # neighbor has higher rank and is not parent.
        return best_neighbor

    # Implementation of objective function that prioritizes ETX. Returns the best parent.
    def objective_function_ETX(self, node) -> Node:
        siblings = self.find_siblings(node)
        parents = self.find_parents(node)
        eligible_nodes = siblings + parents
        min_ETX = None  # of type 'float'
        best_neighbor = None  # of type 'Node'
        for neighbor in eligible_nodes:
            neighbor_connection = self.__get_connection_between(node, neighbor)
            neighbor_ETX = neighbor_connection.get_ETX()
            if min_ETX is None or neighbor_ETX < min_ETX:  # Match on ETX
                best_neighbor = neighbor
                min_ETX = neighbor_ETX
        if node.get_last_transmitter_ID() is not None and best_neighbor is not None:
            if node.get_last_transmitter_ID() == best_neighbor.get_ID():
                return self.objective_function_rank(node)
        return best_neighbor



    ### HELPER METHODS

    # returns a list of nodes containing neighbors.
    def __find_neighbours(self, node_id: uuid) -> []:
        all_connections = self.connections
        neighbours = []
        for connection in all_connections:
            if connection.get_node_from().get_ID() == node_id:
                neighbours.append(connection.get_node_to())
        return neighbours

    def find_children(self, node: Node) -> []:
        children = []
        neighbours = self.__find_neighbours(node.get_ID())
        if len(neighbours) > 0:
            for neighbour in neighbours:
                if neighbour.get_rank() is not None:
                    if neighbour.get_rank() > node.get_rank():
                        children.append(neighbour)
        return children

    def find_parents(self, node: Node) -> []:
        parents = []
        for neighbour in self.__find_neighbours(node.get_ID()):
            if neighbour.get_rank() is not None and node.get_rank() is not None:
                if neighbour.get_rank() < node.get_rank():
                    parents.append(neighbour)
        return parents

    def find_siblings(self, node: Node) -> []:
        siblings = []
        for neighbour in self.__find_neighbours(node.get_ID()):
            if neighbour.get_rank() is not None and node.get_rank() is not None:
                if neighbour.get_rank() == node.get_rank():
                    siblings.append(neighbour)
        return siblings

    # Creates nodes and places them in a 2d grid.
    def __define_nodes_in_network(self, no_of_nodes, network_type) -> []:
        if network_type == 'rand':
            return self.__define_random_network(no_of_nodes)
        elif network_type == 'grid':
            return self.__define_grid_network(no_of_nodes)
        elif network_type == 'tree':
            return self.__define_tree_network()

    # assign each node a random position and rank in the network
    def __define_random_network(self, no_of_nodes) -> []:
        nodelist = []
        for i in range(no_of_nodes):
            x = round(np.random.uniform(0, 10), 1)
            y = round(np.random.uniform(0, 10), 1)  # round(i / (no_of_nodes / 10))
            rank = None
            max_capacity = 1
            node = Node(self.env, max_capacity, rank, x, y)
            nodelist.append(node)
        nodelist[0].set_rank(0)  # define node 0 to be root
        return nodelist

    # assign each node on a grid.
    def __define_grid_network(self, no_of_nodes) -> []:
        nodelist = []
        for x in range(10):
            for y in range(10):
                rank = None
                max_capacity = 1
                node = Node(self.env, max_capacity, rank, x, y)
                nodelist.append(node)
        nodelist[0].set_rank(0)  # define node 0 to be root
        return nodelist

    # assign each node in a tree structure
    def __define_tree_network(self) -> []:
        nodelist = []
        xs = [5, 4, 6, 2.5, 5, 7.5, 2, 4, 6, 8, 1, 3, 5, 7, 9]
        ys = [1, 3, 3, 5, 5, 5, 7, 7, 7, 7, 9, 9, 9, 9, 9]
        for i in range(len(xs)):
            rank = None
            max_capacity = 1
            node = Node(self.env, max_capacity, rank, xs[i], ys[i])
            nodelist.append(node)
        nodelist[0].set_rank(0)  # define node 0 to be root
        return nodelist

    # Neighbour finding algorithm
    def __initialize_neighbours(self) -> []:
        connections = []
        nodes = self.nodes
        for i in nodes:
            for j in nodes:
                if i.get_ID() == j.get_ID():
                    continue
                dist = math.sqrt((i.get_X() - j.get_X()) ** 2 + (i.get_Y() - j.get_Y()) ** 2)
                if dist <= self.neighbourRadius:
                    connection = Connection(node_from=i, node_to=j)
                    connections.append(connection)
        return connections

    def __find_nodes_with_rank(self, rank: int):
        nodes_with_rank = []
        for i in self.nodes:
            if i.get_rank() == rank:
                nodes_with_rank.append(i)
        return nodes_with_rank

    def __find_nodes_with_id(self, node_ID: uuid):
        for node in self.get_nodes():
            if node.get_ID() == node_ID:
                return node
        return

    def __get_connection_between(self, node1: Node, node2: Node) -> Connection:
        for connection in self.connections:
            node1IsFrom = connection.get_node_from().get_ID() == node1.get_ID()
            node1IsTo = connection.get_node_to().get_ID() == node1.get_ID()
            node2IsFrom = connection.get_node_from().get_ID() == node2.get_ID()
            node2IsTo = connection.get_node_to().get_ID() == node2.get_ID()
            if node1IsFrom and node2IsTo:
                return connection
            elif node2IsFrom and node1IsTo:
                return connection

    def remove_node_from_network(self, node):
        for connection in self.connections:
            if (connection.get_node_from().get_ID() is node.get_ID()) or (
                    connection.get_node_to().get_ID() is node.get_ID()):
                self.removedConnections.append(
                    connection) if connection not in self.removedConnections else self.removedConnections
        self.removedNodes.append(node) if node not in self.removedNodes else self.removedNodes

    # local repair runs recursively until no rank inconsistencies are present.
    def local_repair(self, nodes: [Node]):
        for node in nodes:
            # Does node have another parent?
            alive_parents = []
            for parent in self.find_parents(node):
                if parent.get_battery_power() > 0:
                    alive_parents.append(parent)
            has_parents = len(alive_parents) > 0
            if has_parents:
                continue  # If it has a parent we are good - no local repair needed.

            # It does not have parents? Then, increment rank and do local repair on children.
            alive_children = []
            for child in self.find_children(node):
                if child.get_battery_power() > 0:
                    alive_children.append(child)

            # Find rank of new parent
            neighbour_ranks = []
            alive_neighbours = []
            for neighbour in self.__find_neighbours(node.get_ID()):
                if neighbour.get_battery_power() > 0:
                    alive_neighbours.append(neighbour)
            for neighbour in alive_neighbours:
                neighbour_ranks.append(neighbour.get_rank())
            new_parent_rank = min(neighbour_ranks)
            node.set_rank(new_parent_rank + 1)
            self.local_repair(alive_children)

    def get_nodes(self) -> list:
        return self.nodes

    def get_nr_of_nodes(self) -> int:
        return self.noOfNodes

    def get_connections(self) -> list:
        return self.connections

    def get_removed_nodes(self) -> list:
        return self.removedNodes

    def get_removed_connections(self) -> list:
        return self.removedConnections

    def get_env(self):
        return self.env

    def get_dao_messages(self):
        return self.dao_messages

    def change_priority_dao(self, priority: str):
        self.priority_dao = priority
