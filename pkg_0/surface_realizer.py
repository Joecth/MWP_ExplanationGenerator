#!/usr/bin/env python
# coding: utf-8
__author__ = 'JoeXPS13_AS'
"""
surface_realizer.py,
create template for fillers to make a sentence
"""
from chinesenumber2arabicnumber_converter import *

def sr_Sum(children, parent):               ## 1
    ret_set = "\t"
    nf2 = " = "

    for i, tmp in enumerate(children):
        ret_set += str(tmp)
        if i is not len(children) - 1:
            ret_set += " + "

    ret_set += nf2
    ret_set += parent
    return ret_set

def sr_Mul(children, parent):  ## 2   ## children is [obj1, obj2, ...]; parent is obj0
    # nf0 = ", 乘起來"

    ret_set = None
    ### TODO Refactor later
    from data20 import IS_CHINESE_VERSION
    if IS_CHINESE_VERSION:
        ret_set = "\t"
        nf1 = "就是   "
        nf2 = "="

        for tmp in children:
            ret_set += str(tmp)
            ret_set += str("  ")

        # ret_set += nf0
        ret_set += nf1

        for i, tmp in enumerate(children):
            # ret_set +=
            tmp_quan = str(tmp)
            get_quan = extract_quan_from_quanstr(tmp_quan) # need to get 3 from "3個"
            if None == get_quan: # we need to get 1000 from "一仟元鈔票"
                get_quan = chns_num_2_abra_num(tmp_quan)

            ret_set += str(get_quan)
            if i is not len(children)-1:
                ret_set += " * "
            else:
                ret_set += " = "

        # ret_set += nf2
        ret_set += parent

    else:
        ret_set = "\t"
        left  = str(children[0])
        right = str(children[1])
        q_right = extract_quan_from_quanstr(left)
        q_left  = extract_quan_from_quanstr(right)

        template = right + ' * ' + left + ' = ' + parent
        ret_set +=template

    ret_set += "\n"
    return ret_set

def sr_CommonDiv(children, parent, verb):   ## 3
    assert(2 == len(children))
    ret_set = None
    from data20 import IS_CHINESE_VERSION
    ### TODO : refactor later
    if IS_CHINESE_VERSION:
        ret_set = "\t"
        ie  =   "就是"
        # local_children = list(children)
        # local_children.reverse()
        ret_set += str(children[1])
        ret_set += verb
        ret_set += str(children[0])

        ret_set += ie

        #TODO wrap extract_num API into function
        for i, tmp in enumerate(children):
            # ret_set +=
            tmp_quan = str(tmp)
            get_quan = extract_quan_from_quanstr(tmp_quan)
            if None == get_quan:
                get_quan = chns_num_2_abra_num(tmp_quan)

            ret_set += str(get_quan)
            if i is not len(children)-1:
                ret_set += " ÷ "
            else:
                ret_set += " = "
        ret_set += parent

    else: ## English version now  ## ilds-119
        ret_set = "\t"
        left  = str(children[0])
        right = str(children[1])
        q_right = extract_quan_from_quanstr(left)
        q_left  = extract_quan_from_quanstr(right)

        import data20
        if not data20.IS_LAST_IDX:
            template = "We got " + left + " with every " + right
        else:
            template = left + '/' + right + ' = ' + parent
        # ret_set += left
        # ret_set += "is"
        ret_set += template
    ret_set += "\n"
    return ret_set

def sr_UnitTrans(children, parent):     ## 4
    assert(1 == len(children))
    ret_set = "\t"
    ie  = "就是"

    ret_set += children[0]
    ret_set += ie
    ret_set += parent
    ret_set += "\n"
    return ret_set

def sr_FloorDiv(children, parent, verb):       ## 5
    assert(2 == len(children))
    ret_set = "\t"
    print("in sr_FloorDiv func()!")
    ret_set += str(children[0])
    ATMOST_ABLE = " 最多可以 "
    ret_set += ATMOST_ABLE

    ret_set += verb
    ret_set += " "
    # ret_set += str(children[1])   remove, Accodring to Prof. Su's suggestion
    ret_set += "\t:\t"

    for i, tmp in enumerate(children):
        # ret_set +=
        tmp_quan = str(tmp)
        get_quan = extract_quan_from_quanstr(tmp_quan)
        if None == get_quan:
            get_quan = chns_num_2_abra_num(tmp_quan)

        ret_set += str(get_quan)
        if i is not len(children)-1:
            ret_set += " ÷ "
        else:
            # ret_set += " 取商, 餘數不理, = "    remove, according to Prof. Su's suggestion
            ret_set += " = "    # remove, according to Prof. Su's suggestion

    ret_set += parent
    ret_set += "\n"
    return ret_set

def sr_Subtraction(children, parent):           ## 6
    assert(2 == len(children))
    ret_set = "\t"

    ret_set += children[0]
    ret_set += " - "
    ret_set += children[1]
    ret_set += " = "
    ret_set += parent
    # ret_set += "\n"
    # ret_set +=
    return ret_set

def sr_TVQSubtraction(children, parent):           ## 6
    assert(2 == len(children))
    ret_set = "\t"

    ret_set += children[1]
    ret_set += " - "
    ret_set += children[0]
    ret_set += " = "
    ret_set += parent
    ret_set += "\n"
    # ret_set +=
    return ret_set

def sr_Addition(children, parent):              ## 7
    # assert(1 == len(children))
    ret_set = "\t"
    ret_set += children[0]
    ret_set += " + "
    ret_set += children[1]
    ret_set += " = "
    ret_set += parent
    ret_set += "\n"

    return ret_set

def sr_CeilDiv(children, parent, verb):       ## 8
    assert(2 == len(children))
    ret_set = "\t"
    # print("in sr_CeilDiv func()!")
    ret_set += str(children[0])
    ATLEAST_ABLE = " 最少需要 "
    ret_set += ATLEAST_ABLE

    ret_set += verb
    ret_set += " "
    # ret_set += str(children[1])   remove, Accodring to Prof. Su's suggestion
    ret_set += "\t:\t"

    for i, tmp in enumerate(children):
        # ret_set +=
        tmp_quan = str(tmp)
        get_quan = extract_quan_from_quanstr(tmp_quan)
        if None == get_quan:
            get_quan = chns_num_2_abra_num(tmp_quan)

        ret_set += str(get_quan)
        if i is not len(children)-1:
            ret_set += " ÷ "
        else:
            # ret_set += " 取商, 餘數不理, = "    remove, according to Prof. Su's suggestion
            ret_set += " + 1 = "    # remove, according to Prof. Su's suggestion

    ret_set += parent
    # ret_set += "\n"
    return ret_set

def sr_Surplus(children, parent, verb):       ## 9
    assert(2 == len(children))
    ret_set = "\t"
    # print("in  func()!")
    # ret_set += str(children[0])

    # ret_set += verb
    ret_set += "剩下"
    ret_set += " "
    # ret_set += str(children[1])   remove, Accodring to Prof. Su's suggestion
    ret_set += "\t:\t"

    for i, tmp in enumerate(children):
        # ret_set +=
        tmp_quan = str(tmp)
        get_quan = extract_quan_from_quanstr(tmp_quan)
        if None == get_quan:
            get_quan = chns_num_2_abra_num(tmp_quan)

        ret_set += str(get_quan)
        if i is not len(children)-1:
            ret_set += " ÷ "
        else:
            # ret_set += " 取商, 餘數不理, = "    remove, according to Prof. Su's suggestion
            ret_set += " … "    # remove, according to Prof. Su's suggestion

    ret_set += parent
    # ret_set += "\n"
    return ret_set

def find(pattern, string):
    match = re.search(pattern,string)
    if match:
        print(match.group())
    else:
        print("not find")

if (__name__ == "__main__"):
    print("AAAAAA : "+str(IS_CHINESE_VERSION))
    print ("Hello srufacea_realizer.py!")
    cdn = ["2疊","一萬元鈔票"]
    par = "20000元"
    # print (int(par))
    print(sr_Mul(cdn, par))
    cdn_sum = ["20000元", "6000元","1300元"]
    par_sum = "27300元"
    print(sr_Sum(cdn_sum, par_sum))

    v_list = ['V.付出來', 'UPSCOPE']
    tmp_pattern = v_list[0]
    print (tmp_pattern)

    import re
    matcho = re.search("V\.", tmp_pattern)
    verb_start_idx = matcho.span()[1]
    print(matcho.span())
    print(tmp_pattern[verb_start_idx:])

    #######################################
    num_pat = "[\d]+"
    num_str = "13張100元鈔票"
    match2 = re.search(num_pat, num_str)
    num = match2.group()
    print (num)
