"""
tree.py: build Explanation Tree
"""
from data20 import *

from node import Node
(_ROOT, _DEPTH, _BREADTH) = range(3)

class Tree:
    def __init__(self):
        self.__nodes = {}

    @property
    def getNodes(self):
        return self.__nodes

    # def add_node(self, node_id, parent_id=None, chunk_id=0, level=0,
    #                       node_type = None, chunk = None):
    def add_node(self, node):
        # node = Node(chunkdata, parent, chunk_id, level)
        node_id = node.get_node_id()
        self[node_id] = node                 ## TODO w/ __setitem__

        dummy_parent_id = node.get_parent_id()
        if dummy_parent_id is not None:
            # self[dummy_parent_id].add_child(node_id)  ## TODO w/ __getitem__
            self[dummy_parent_id].add_child(node)  ## TODO w/ __getitem__

        # return node

    def display(self, node_id, depth=_ROOT): ## chunkdta is name in our reg. testing
        obje = self[node_id]
        children = obje.get_children  ## no need "()" in func call, TODO w/ __getitem__

        data = str(node_id)
        chunk_str = str(obje.get_chunk())
        if None != obje.get_chunk():
            data = str(node_id) + "__" + chunk_str

        if depth == _ROOT:
            print("{0}".format(data))
        else:
            print("\t"*depth, "{0}".format(data))

        tree_trans_str = "("

        ### for Local Testing
        if chunk_str == 'None':
            chunk_str = data

        tree_trans_str += chunk_str

        depth += 1
        for child in children:
            tree_trans_str += self.display(child.get_node_id(), depth) #recursive call
            tree_trans_str += ")"

        return tree_trans_str

    def traverse(self, chunkdata, mode=_BREADTH):
        yield chunkdata
        queue = self[chunkdata].get_children

        while queue:
            yield queue[0]
            expansion = self[queue[0]].get_children
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item

    def get_nodes(self):
        return self.__nodes

if ( __name__ == "__main__"):

    print ("Hello tree.py!")
    tree = Tree()
    tree.add_node(Node("Harry"))  # root node
    tree.add_node(Node("Jane", "Harry"))
    tree.add_node(Node("Bill", "Harry"))
    tree.add_node(Node("Joe", "Jane"))
    tree.add_node(Node("Diane", "Jane"))
    tree.add_node(Node("George", "Diane"))
    tree.add_node(Node("Mary", "Diane"))
    tree.add_node(Node("Jill", "George"))
    tree.add_node(Node("Carol", "Jill"))
    tree.add_node(Node("Grace", "Bill"))
    tree.add_node(Node("Mark", "Jane"))

    # global tree_trans_str
    tree_trans_str = tree.display("Harry")
    print("tree_trans_str:  ", tree_trans_str)
    print("***** DEPTH-FIRST ITERATION *****")
    # temp = tree.traverse("Harry")

    print("***** BREADTH-FIRST ITERATION *****")
    # for node in tree.traverse("Harry", mode=_BREADTH):
    #     print(node)
