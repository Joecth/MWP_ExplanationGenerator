"""
node.py,
the node structure
"""

class Node:
    def __init__(self, node_id, parent_id=None, chunk_id=0, level=0, node_type = None, chunk = None):
        # self.__identifier = identifier
        self.__node_id     = node_id
        self.__parent_id   = parent_id
        self.__chunk_id  = chunk_id
        self.__level    = level
        self.__node_type = node_type
        self.__chunk = chunk
        self.__children = [] ##TODO: may be changed to {}

    def __str__(self):
        ret_str = "Chunk:" + self.__node_id
        if None != self.__parent_id:
            ret_str += "\nParent: " + str(self.__parent_id)
        if 0 != self.__chunk_id:
            ret_str += "\nID: " + str(self.__chunk_id)
        if 0 != self.__level:
            ret_str += "\nLevel: " + str(self.__level)
        if None != self.__node_type:
            ret_str += "\nnode_type: " + str(self.__node_type)
        if self.__children: ## non_empty list
            ret_str += "\nChildren: " + str(self.__children)

            ## traverse Children lists (1st level) to print them all
            dummy_childId = 1
            str_children = "\n"
            for mm in self.__children:
                dummy_child_name = mm.get_node_id()
                str_children += "\tChild " + str(dummy_childId) + ": " + dummy_child_name + "\n"
                dummy_childId += 1

            ret_str += str_children

        return ret_str

    # def __repr__(self):
    #     return self.__children

    @property
    def get_identifier(self):
        return self.__identifier

    def get_node_id(self):
        return self.__node_id

    def get_parent_id(self):
        return self.__parent_id

    def get_chunk_id(self):
        return self.__chunk_id

    def get_level(self):
        return self.__level

    def get_node_type(self):
        return self.__node_type

    def get_chunk(self):
        return self.__chunk

    @property
    def get_children(self):
        return self.__children

    def add_child(self, node):
        self.__children.append(node)

if ( __name__ == "__main__"):
    n1 = Node("JJ")
    n2 = Node("OO")
    n3 = Node('EE')

    # print (n1)
    # print (n3)

    n1.add_child(n3)
    n1.add_child(n2)

    # n2.addChild(n1)
    # print (n2)
    print (n1)
