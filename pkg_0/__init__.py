#!/usr/bin/env python3
#coding=utf-8

__author__ = 'JoeXPS13_AS'
import xml.sax
import re
import sys, getopt
from node import *
from tree import *
from data20 import *
from surface_realizer import *

## Define I/O file names as MACRO Vars
# FILE_INPUT_0          = ''
# FILE_INPUT_0        = 'input_0.xml'
# FILE_INPUT_0        = 'problems/english_qs/uwds-0001_changeunit.trace.xl'  ## try to get all from disk from shell
# FILE_INPUT_0        = 'problems/english_qs/uwds-0001_changeunit.trace.xml'  ## try to get all from disk from shell
# FILE_INPUT_0        = 'problems/online/crashcase/20160218102935.trace.xml'
# FILE_INPUT_0        = 'problems/tmp.trace.Sample-1.xml'  ## try to get all from disk from shell
# FILE_INPUT_0        = 'problems/tmp.trace.Sample-8.xml'  ## try to get all from disk from shell
# FILE_INPUT_0        = 'problems/20151209105638.trace.xml'  ## try to get all from disk from shell
FILE_OUTPUT_0       = 'output.xml'
FILE_OUTPUT_CORE    = 'out_core.xml'
FILE_RAW_TREE       = 'raw_tree.xml'             ## index from FILE_INPUT_0
FILE_BUILD_TREE_LOG = 'build_tree.log.xml'

# print("Print out all argvs for DBG: ")
# for i, arg in enumerate(sys.argv):
#     print(i, " ==> ", arg)

# try:
#     opts, args = getopt.getopt(sys.argv[1:], "hi:", ["input="])
# except getopt.GetoptError:
#     print ('No Input "trace" file!!! Please ask help from IE!')
#     # print ('python3 __init__.py -h, for more help')
#     sys.exit(2)

fp_o = open(FILE_OUTPUT_0, encoding='utf-8', mode='w+')  ## THE GENERAL OUTPUT!!!

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:")#, ["--help", "input=", "output="])
    # print ("argv[1] : ", sys.argv[1])
except getopt.GetoptError:  ## didn't get
    # print ('python3 __init__.py -i <inputfile> -o <outputfile>')
    # print ('python3 __init__.py -h, for more help')
    print ("Invalid Input file !!!")
    fp_o.write("Invalid Input File!!!")
    fp_o.close()
    sys.exit(2)

# try:
#     opts, args = getopt.getopt(sys.argv[1:], "hi:o:")#, ["--help", "input=", "output="])
#     print("argv[1] : ", sys.argv[1])
# except getopt.GetoptError:  ## didn't get
#     print ('python3 __init__.py -i <inputfile> -o <outputfile>')
#     print ('python3 __init__.py -h, for more help')
#     sys.exit(2)

# print ("opts : ", opts)
# print ("args : ", args)

for opt, arg in opts:
    if opt == '-h':
        print ('python3 __init__.py -i <inputfile> -o <outputfile>')
        print ('\tdefault inputfile: problems/tmp.trace.Sample-7.xml')
        print ('\tdefault outputfile: output.xml')
        sys.exit()
    elif opt in ("-i", "--ifile"):
        # inputfile = arg
        FILE_INPUT_0 = arg
        # print("aaaaa")
        if FILE_INPUT_0 == "":
            # print("aaa : ", FILE_INPUT_0 )
            sys.exit(2)
    elif opt in ("-o", "--ofile"):
        # outputfile = arg
        FILE_OUTPUT_0 = arg
        # print ("User defined output name!")
        fp_o.close()   ###  use User-Defined name
        fp_o = open(FILE_OUTPUT_0, encoding='utf-8', mode='w+')  ## THE GENERAL OUTPUT!!!
        # print ("aaaaaaa", FILE_OUPUT_0, "bbbb")

if DBG_OUTPUT:
    print ('Input file is "', FILE_INPUT_0)
    print ('Output file is "', FILE_OUTPUT_0)

# if len(sys.argv) < 2:
#     print("No Input File Name specified,\n"
#           "Adopt default file as Input:  ", FILE_INPUT_0)
#     # sys.exit()
# else:
#     if sys.argv[1].startswith('--'):
#         option = sys.argv[1][2:]
#         if option == 'help':
#             print('''
# This program is Explanation Generation.
# One file can be specified as input.
# Options include:
#   --version : Prints the version number
#   --help    : Display this help''')
#         elif option == 'version':
#             print("Version 1.0")
#         else:
#             print("Unknown option.")
#         sys.exit()
#     else:
#         FILE_INPUT_0 = sys.argv[1]

'''    ChunkHandler '''
class ChunkHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.tag = ''
        self.buffer = ''

    def startElement(self, name, attributes): ## in my input, there's no attributes
        self.tag = name
        if name == 'CHUNK':
            self.buffer = ''
        if name == 'Unit':
            global ID
            ID = attributes["ID"]
            print("ID :: ", ID)

    def endElement(self, name):
        pass

    def characters(self, data):
        global is_UnitID_defined
        if self.tag == 'CHUNK':
            # global is_UnitID_defined
            global has_UnitID_made_up
            if False == is_UnitID_defined and False == has_UnitID_made_up:
                has_UnitID_made_up = True
                # global ID, which equals to "" now, for <Unit ID="">
                EMPTY_Str = ""
                tmpStr = str('<') + str("Unit") + str(" ID=\"") + str(EMPTY_Str) + str("\">") + str('\n')
                print (tmpStr)
                fp.write(tmpStr)
            # if data != '{\t}*' and  data != '\n':
            if re.search('\w', data): ## regular expression to prune {\t}+ or \n
                # print ("data:", data)
                tmpStr =   str('<') + str(self.tag) + str(">") \
                           + str(data) \
                           + str('<') + str('/') + str(self.tag) + str('>')+ str('\n')
                # print (str(data))         ##Chinese issue
                # tmpStr_unit8 = str(tmpStr, 'unicode')
                fp.write(tmpStr)#_unit8)
            self.buffer += data
        elif self.tag == 'Unit':
            # global is_UnitID_defined
            is_UnitID_defined = True

            global ID
            tmpStr = str('<') + str(self.tag) + str(" ID=\"") + str(ID) + str("\">") + str('\n')
            print (tmpStr)
            fp.write(tmpStr)
        else:
            pass
'''
    ExpGenTreeBuilder, Actually, this is a redundant work after second review...
    dictionary can be built at the 1st stage and served as Golden directly
    This Class just helps to verify output: "raw_tree.xml" is utf-8 and readable
'''
class ExpGenTreeBuilder(xml.sax.ContentHandler):
    def __init__(self):
        self.tag = ''
        self.buffer = ''

    def startElement(self, name, attribute):
        self.tag = name
        if name != 'CHUNK' and name != 'root' and name != 'Unit':
            assert 0, 'Got a non-CHUNK tag!'
        # if name ==
        ## TODO add the ID of Unit tag into log file
        self.buffer = ''

    def endElement(self, name):
        if name != 'CHUNK':
            return

        # print ("nodes", self.buffer)
        tmp = self.buffer         ### tmp: 43seashell
        afterlama = tmp
        # if IS_ENGLISH_VERSION:
        afterlama = morph(tmp)    ### afterlama: 43 seashells
        # else:
        #     pass
        chunks.append(afterlama)

        tmp_str = afterlama + '\n' ### tmp_str: 43 seashells\n
        fp.write(tmp_str)
        fp.flush()

        #global key
        #nodes[key] = self.buffer

        #key += 1

    def characters(self, data):
        # CHUNK tag was already checked at start
        self.buffer += data



def morph_English(quan, lama):
    if 1 == quan:
        ret_str = lama
        if 1 == len(lama):
            ret_str += " Warning!! Weird Word!? "   ### such as "n2", "n3"
        return ret_str

    '''morphology cases'''
    ret_str = ""
    # if len(lama) >= 3:
    #     if lama[-3] == "man":
    #         ret_str = "men"
    if lama == "child":
        ret_str = "children"
    elif lama == "foot":
        ret_str = "feet"
    elif lama == "tooth":
        ret_str = "teeth"
    else:
        # check typical rules
        if len(lama) >= 2:
            if lama[-1] == "y":             ### end with "y"
                tmp_char = lama[-2:-1]
                if tmp_char in vowels:        ### boys or toys
                    ret_str = lama + "s"
                else:
                    ret_str = lama[:-1] + "ies"  ## bodis
            elif lama[-2:] == "sh" or lama[-2:] == "ch" or lama[-1] == "s" or lama[-1] == "z" or lama[-1] == "x":
                ret_str = lama + "es"         ## fishes
            elif lama[-2:] == "fe":            ## TODO irregular
                ret_str = lama[:-2] + "ves"
            elif lama[-1] == "f":             ## TODO irregular
                ret_str = lama[:-1] + "ves"    ## wolves; but in some cases it ends with only "s", like
            elif lama[-1] == "o":             ## TODO irregular
                ret_str = lama + "es"         ## cargoes; but in some cases it ends with only "s"
            else:
                ret_str = lama + "s"
        else:  ## len(lama) == 1 or 0
            ret_str = lama + " Warning!! Weird Word from IE! "   ### such as "n2", "n3"

    return ret_str

def morph(lama):
    """ morphology check """

    ## Shouldn't be built-in values
    which_op = OP_dict.get(lama)
    if None != which_op:  ## lama is an OP Chunk
        return lama

    if "BeginTree" == lama or "EndTree" == lama or "UPSCOPE" == lama:  ## lama is a built-in
        return lama

    if lama[:2] == "V.":
        return lama


    ret_str = lama
    item_pat = "[a-zA-Z]+"
    match_item = re.search(item_pat, lama)

    if None != match_item:   ## morphology work for only English,
        # print ("SPAN :: ", match_item.span())
        item = match_item.group()
        if "n" == item:
            return lama + " Warning!! Un-decoded String from IE! "  ###TODO, Hard code is not a good solution for "n2" issue

        num_pat = "[\d]+"
        match_num = re.search(num_pat, lama)
        num = match_num.group()
        if None == num:      ## we assume the "number" of English word problem should be Arabic
            print("INVALID STRING CHUNK!!!")
            assert(0)

        if int(num) < 0:
            print("INVALID VALUE for this MATH WORD PROBLEM!")
            assert(0)

        # item = match_item.group()
        # correct_lama = ""
        # if int(num) > 1:
        correct_lama = morph_English(int(num), item)
        # else:
        #     correct_lama = item

        ret_str = num + " " + correct_lama
    else:                    ### for Chinese problems
        ret_str = lama

    return ret_str

'''    Main '''
if ( __name__ == "__main__"):
    # OP_dict = {"OP_Sum":1, "OP_Multiplication":2, "OP_CommonDivision":3}
    # n1 = Node("Joo")
    # print (n1)
    # exit(-3)
    # Create XMLReader
    parser = xml.sax.make_parser()

    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # ReWrite ContextHandler
    ### Parsing to RAW TREE file
    Handler = ChunkHandler()
    parser.setContentHandler( Handler )


    fp = open(FILE_RAW_TREE, encoding='utf-8', mode='w+')
    fp.write(str('<') + str('root') + str(">") + str('\n'))
    try:
        parser.parse(FILE_INPUT_0)  ## Call into ChunkHandler Class, refer to API for detail
    except ValueError as e:
        print (FILE_INPUT_0, " Warning!! This file does NOT exist! ")#, e)
        fp_o.write("No Input File : " + FILE_INPUT_0 + "!!!")
        fp_o.close()
        sys.exit(2)
    except NameError as e:
        print("Input file is not defined!")
        fp_o.write("Input File not Defined!")
        fp_o.close()
        sys.exit(2)

    fp.write(str('<') + str('/') + str('Unit') + str('>')+ str('\n'))
    fp.write(str('<') + str('/') + str('root') + str('>')+ str('\n'))
    fp.close()

    ### BUILD TREE ###
    Handler2 = ExpGenTreeBuilder()
    parser.setContentHandler(Handler2)

    'Dictionary for nodes'
    nodes = {}
    chunks = []
    # global key
    # key = 1

    fp = open(FILE_BUILD_TREE_LOG, encoding='utf-8', mode='w+')
    parser.parse(FILE_RAW_TREE) ##################################
    fp.close()     ## CALL INTO ExpGenTreeBuilder::endElement()

    tree = Tree()
    node_id = 0       # ROOT's node_id   is   0, serves as chunkdata, the input
    par_id = None     # ROOT's parent_id is  None
    chunk_id = -1       ## ROOT's chunk id is -1,
                        ##  chunk id is same as the index of chunk List, which starts from 0
    level = 0         # ROOT's level        is   0
    node_type = NodeType.root
    curr_chunk = "ROOT"
    is_build_tree = False      # turn on after receiving BeginTree

    nodeid2nodename_dict = {}
    curr_id = 0       # "ROOT"    # as ptr that points to current node

    node = Node(node_id, par_id, chunk_id, level, node_type, curr_chunk)
    tree.add_node(node)
    par_id = node_id ### parent_id == 0  nows
    nodeid2nodename_dict[node_id] = node

    dbg_chunk_list_of_nodes_into_tree = [curr_chunk]
    all_tree_nodes_dict = {0:node}
    op_node_list = []
    # print ("nodes len :", len(nodes))
    ### Insert nodes here
    gen = (i for i,x in enumerate(chunks))
    # for key in nodes:
    for i in gen:
        # print (key, "aaaaa", nodes[key])
        chunk_id = i    ### chunk_id original id position in chunkList
        curr_chunk = chunks[i]  ### chunk

        ## TODO : get the Verb
        if not verb_list:
            pat = "V\."
            match = re.search(pat, curr_chunk)
            verb = None
            if None != match:
                verb_start_idx = match.span()[1]
                verb = curr_chunk[verb_start_idx:]

            if None != verb:
                verb_list.append(verb)

        ## switch
        if "BeginTree" == curr_chunk:
            is_build_tree = True
            continue
        if "EndTree" == curr_chunk:
            is_build_tree = False
            continue

        if not is_build_tree: ## to prevent "BeginTree" chunk  from being built as a node of tree
            continue

        if "UPSCOPE" == curr_chunk:
            level -= 1
            obje = nodeid2nodename_dict.get(curr_id)
            par_id = obje.get_parent_id()
            curr_id = par_id
            continue


        ## Start build tree
        # if "UPSCOPE" != curr_chunk:
        if None == OP_dict.get(curr_chunk): # chunk is a Value_node
            # curr_chunk += "$$" + str(key)   ## OP Encoding as below
            node_type = NodeType.value_node
        else:   #chunk is an OP_node
            node_type = NodeType.op_node           ### node_type

        level += 1          ### level
        node_id += 1        ### node_id

        node = Node(node_id, par_id, chunk_id, level, node_type, curr_chunk)
        tree.add_node(node)
        nodeid2nodename_dict[node_id] = node

        par_id = node_id
        curr_id = node_id       ### for node to find parent correctly

        all_tree_nodes_dict[node_id] = node

        if None != OP_dict.get(curr_chunk):
            op_node_list.append(node)
            ### discourse planner works according to level and node_id
            ### within node instance
            ### but query and compare is not efficient
            ### so we create level2node_dict for query

        dbg_chunk_list_of_nodes_into_tree.append(curr_chunk)

    tree_trans_str = tree.display(0)
    # print("tree_trans_str:: ", tree_trans_str)
    tree_trans_str_final = tree_trans_str.replace(")(", "|")
    tree_trans_str_final = tree_trans_str_final[1:] ## truncate the "(" before ROOT

    if DBG_OUTPUT:
        print("tree_trans_str_final:: ", tree_trans_str_final)


    global ID
    fp_o.write(str('<') + str('Unit') + str(" ID=\"") + str(ID) + str("\">") + str('\n'))
    ## TODO idx's number
    fp_o.write(str('\t') +
            str('<') + str('Ques') + str(" idx=\"") + str(1) + str("\">") + str('\n'))
    fp_o.write(str('\t') + str('\t') +
            str('<') + str('ANS') + str(">") + str('\n'))

    fp_o.write(str('\t') + str('\t') + str('\t') +
            str('<') + str('Chain') + str(">") + str('\n'))
    fp_o.write(str('\t') + str('\t') + str('\t') + str('\t') +
            tree_trans_str_final + str('\n'))
    fp_o.write(str('\t') + str('\t') + str('\t') +
            str('<') + str('/') + str('Chain') + str('>') + str('\n'))
    fp_o.flush()
    # fp_o.close()


    if DBG:
        print("DBG chunks of nodes into tree:   \n\t", dbg_chunk_list_of_nodes_into_tree, "\n end of DBG")  ### collectint
        print("DBG input_chunks:\n\t", chunks)    ## input

    tree_get_nodes = tree.get_nodes()
    # print("DB tree get nodes: ", temp_d.)
    ## print [(node.get_chunk_id(), node.get_chunk()) for node in temp_d]
    tree_nodes_checking = [(tmp_node.get_chunk()) for key, tmp_node in tree_get_nodes.items()]
    if DBG:
        print("DBG tree gets nodes: \n\t", tree_nodes_checking) ## collected in tree

        print ("DBG op_node_list: \t", op_node_list)
        for node in op_node_list:
            assert(node.get_chunk() == chunks[node.get_chunk_id()])
        tmm = [(node.get_node_id(), node.get_level()) for node in op_node_list]
        print ("tmmmmm", tmm)
    ###########################################################
    # Starting build discourse planner
    #
    ###########################################################

    discourse_trvs_op_list = []

    while op_node_list:
        op_levels = [node.get_level() for node in op_node_list]
        max_level = max(op_levels)
        idx_opnodelist2samelevelnodes = [i for i, j in enumerate(op_node_list) if j.get_level() == max_level]
            ### the idx is for op_node_list


        same_level_nodes = [j for i, j in enumerate(op_node_list) if j.get_level() == max_level]
        ####
        ## Sort the same_level_nodes according to node's node_id
        ####

        nodeids_for_same_levels = [tmp.get_node_id() for tmp in same_level_nodes]
            ### same_level_nodes            ==> [obj1, obj2, obj3]
            ### node_ids_for_same_levels    ==> [4,     8,      12]
        # min_nodeid_idx = nodeids_for_same_levels.index(min(nodeids_for_same_levels))  ### 0, in this case

        ordered_op_list = []
        # for i, j in enumerate(same_level_nodes):  ### (0, obj1), (1, obj2), (2, obj3)
        while same_level_nodes:
            min_nodeid_idx = nodeids_for_same_levels.index(min(nodeids_for_same_levels))
            ordered_op_list.append(same_level_nodes[min_nodeid_idx])
            nodeids_for_same_levels.pop(min_nodeid_idx)
            same_level_nodes.pop(min_nodeid_idx)

        reverse = list(idx_opnodelist2samelevelnodes)
        reverse.reverse()

        for tmp in reverse:
            op_node_list.pop(tmp)

        discourse_trvs_op_list.extend(ordered_op_list)

    if DBG:
        print ("discourse_trvs_op_list,\t", discourse_trvs_op_list)

    explanation = "Ans: \n"
    sr = None
    t_dict = {}
    last_idx = len(discourse_trvs_op_list) - 1
    for i, op_node in enumerate(discourse_trvs_op_list):
        op_type = op_node.get_chunk() ## to check op type
        which_op = OP_dict.get(op_type) ## OP_dict is in data20.py
        assert(None != which_op)

        cdn = op_node.get_children
        cdn_chunk = [node.get_chunk() for node in cdn]
        par_id = op_node.get_parent_id()
        par = tree_get_nodes[par_id]
        par_chunk = par.get_chunk()

        ### if it's the op_node for Ans, which is closest to ROOT
        if i == last_idx:
            # if 1 == len(discourse_trvs_op_list):
            #     explanation += "共"
            # else :
                # explanation += "\t所以, 共"
            if 1 != len(discourse_trvs_op_list):
                explanation += "\tThus,  "
                if IS_CHINESE_VERSION:
                    explanation += "\t所以,  " #, 共"

            ## TODO if Sum, append "共"
            if 1 == which_op: ##or 2 == which_op: 1::Sum, 2::Mul
                explanation += "Totally "
                if IS_CHINESE_VERSION:
                    explanation += "共 "

            if 5 != which_op and 6 != which_op and 8 !=  which_op and 9 != which_op:
                ### FloorDiv:5, Sub:6, CeilDiv:8, Surplus:9, don't need to add verb at beginning
                if verb_list:
                    explanation += verb_list[0]
                else:
                    explanation += ""   ## 中文: 是

        ### get the required function as template
        sr = OP_func_map.get(op_type)  ### OP_func_map is in data20.py
        if None == sr:
            print("No template for this OP!")
            assert(0)

        ## which_op = OP_dict.get(op_type)
        if 3 != which_op and 5 != which_op and 8 != which_op and 9 != which_op:
            explanation += sr(cdn_chunk, par_chunk)
        else:
            ### if 3: CommonDiv, 5: FloorDiv, 8: CeilDiv, 9: Surplue we pass the verb
            if not verb_list: #None == verb_list[0]:
                print ("\nNo Verb!\n")
                tmp_v = ""
            else:
                tmp_v = verb_list[0]

            # explanation += sr(cdn_chunk, par_chunk, verb_list[0])
            explanation += sr(cdn_chunk, par_chunk, tmp_v)

    print ("explanation : \n", explanation)
    fp_o.write(str('\t') + str('\t') + str('\t') + 
            str('<') + str('Explanation') + str(">") + str('\n'))
    fp_o.write(str('\t') + str('\t') + str('\t') + str('\t') + 
            explanation + str('\n'))
    fp_o.write(str('\t') + str('\t') + str('\t') +
            str('<') + str('/') + str('Explanation') + str('>')+ str('\n'))
    fp_o.flush()
    #fp_o.close()

    '''
    ' Per ChaoChun's request, add Ques, Ans, and Unit tags
    '''
    fp_o.write(str('\t') + str('\t') +
            str('<') + str('/') + str('ANS') + str('>')+ str('\n'))
    fp_o.write(str('\t') +
            str('<') + str('/') + str('Ques') + str('>')+ str('\n'))
    fp_o.write(str('<') + str('/') + str('Unit') + str('>')+ str('\n'))

    fp_o.close()
    # fp_o = open(FILE_OUTPUT_0, encoding='utf-8', mode='w+')
    # fp_o.write(str('<') + str('Chain') + str(">")) # + str('\n'))
    # fp_o.write(tree_trans_str_final)
    # fp_o.write(str('<') + str('/') + str('Chain') + str('>')+ str('\n'))
    # fp_o.flush()

# print(all_tree_nodes_dict)
## print(op_node_list)
# print(chunks[6])
### testing
# print ("data20's level2nodes_dict: ", level2nodes_dict)


# print (max(tmm[1]))
