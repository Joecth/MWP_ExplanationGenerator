"""
data20.py,
stores the data structures
"""
from enum import Enum
from surface_realizer import *
import os

global ID ## in <Unit ID="">  tag
DBG = False
DBG_OUTPUT = False
IS_CHINESE_VERSION = False
if "EG_Chinese" in os.environ :
    IS_CHINESE_VERSION = True

verb_list = []
global is_UnitID_defined
is_UnitID_defined = False
global has_UnitID_made_up
has_UnitID_made_up = False
global tree_trans_str  ## Transform the tree from horizontal to (Mul(A|B)) format
global ID
ID = ""

class NodeType(Enum):
    root = 1
    value_node = 2
    op_node = 3
# class NodeType: ### This is exactly the enum
#     root, value_node, op_node = range(3)
# >>> print Materials.Matte
# 3
# print(NodeType.op_node)

# class Operators(Enum):
#     OP_Sum            = 1
#     OP_Multiplication = 2
#     OP_CommonDiv      = 3

OP_dict = {"OP_Sum":1, "OP_Multiplication":2, "OP_CommonDiv":3, "OP_UnitTrans":4,
           "OP_FloorDiv":5, "OP_Subtraction":6, "OP_Addition":7, "OP_CeilDiv":8, "OP_Surplus":9,
           "OP_TVQ_Addition":10, "OP_TVQ_Subtraction":11}

#####
#     Map to the required template, in surface_realizer.py
#####
OP_func_map = {"OP_Sum"             :sr_Sum,
               "OP_Multiplication"  :sr_Mul,
               "OP_CommonDiv"       :sr_CommonDiv,
               "OP_UnitTrans"       :sr_UnitTrans,
               "OP_FloorDiv"        :sr_FloorDiv,
               "OP_Subtraction"     :sr_Subtraction,
               "OP_Addition"        :sr_Addition,
               "OP_CeilDiv"         :sr_CeilDiv,
               "OP_Surplus"         :sr_Surplus,
               "OP_TVQ_Addition"    :sr_Addition,
               "OP_TVQ_Subtraction" :sr_TVQSubtraction
               }

level2nodes_dict = {}  ## NOT used after last...
vowels = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}

if (__name__ == "__main__"):
    print ("Hello data20.py")

