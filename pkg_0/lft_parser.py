#!/usr/bin/env python3
#coding=utf-8

__author__ = 'JoeXPS13_AS'
import sys
import re
class LogicFormParser:
    def __init__(self, input_file, log):
        self.__input_file   = input_file
        self.__log          = log

        # self.parse()

    def parse(self):
        # print("in LFT Parser : ", self.__input_file)
        try:
            fp_o = open(self.__input_file, "r", encoding="utf-8")
        except FileNotFoundError as e:
            # print(self.__input_file, " Not Found! ") ##TODO write to o_file
            sys.exit(2)

        # line = fp_o.readline()
        # print("line: ", line)

        lines = fp_o.readlines()
        # print("lines: ", lines)

        pattern = "<Ques idx="
        idx = 0
        ques_tokens = None
        for token in lines:
            match = re.search(pattern, token)
            if None != match:
                # print("match: ", match)
                ques_tokens = lines[idx:]
                break
            idx += 1

        # print("ques_tokens: ", ques_tokens)
        # ques_tokens:  ['\t<Ques idx="1">\n', '\t\t<Sent idx="1">\n', '\t(LF0\n', '\t\t(s3w6 have)\n', '\t\t(s3w3 book)\n', '\t\t(s3w2 many)\n', '\t\t(s3w1 how)\n', '\t\t(s3w4 do)\n', '\t\t(s3w5 they)\n', '\t\t(s3w7 together)\n', '\t)\n', '\n', '\t(LF1\n', '\t\t(verb v3 s3w6)\n', '\t\t(dobj v3 n3)\n', '\t\t(head n3 s3w3)\n', '\t\t(amod n3 s3w2)\n', '\t\t(advmod n3 s3w1)\n', '\t\t(aux v3 s3w4)\n', '\t\t(nsubj v3 s3w5)\n', '\t\t(advmod v3 s3w7)\n', '\t)\n', '\n', '\t(LF2\n', '\t\t\n', '\t\t(ASK ANS (Addition (quan q2 # s1w4) (quan q4 # s2w4)))\n', '\t)\n', '\n', '\t\t</Sent>\n', '\t</Ques>\n', '</Unit>\n']

        '''Seperate the code from previous loop for Readability'''
        LF0_pat = "\(LF0"
        LF1_pat = "\(LF1"
        LF2_pat = "\(LF2"
        idx = 0
        idx_lf0 = idx_lf1 = idx_lf2 = 0
        LF0_list = LF1_list = None
        for token in ques_tokens:
            match_LF0 = re.search(LF0_pat, token)
            match_LF1 = re.search(LF1_pat, token)
            match_LF2 = re.search(LF2_pat, token)

            if None != match_LF0:
                idx_lf0 = idx
            if None != match_LF1:
                idx_lf1 = idx
            if None != match_LF2:
                idx_lf2 = idx

            if idx_lf0 and idx_lf1 and idx_lf2:
                assert((idx_lf0 < idx_lf1) and (idx_lf1 < idx_lf2))
                LF0_list = ques_tokens[idx_lf0:idx_lf1]
                LF1_list = ques_tokens[idx_lf1:idx_lf2]

            idx += 1

        # print("LF0 list: ", LF0_list)
        # print("LF1 list: ", LF1_list)
        return (LF0_list, LF1_list)
        #
        # pat = "\(.*\)"  # (s1w2 have), (s1w1 Keith), ... etc
        # '''Build LF0 Hash'''
        # LF0_dict = {}
        # for token in LF0_list:
        #     match = re.search(pat, token)
        #     if None != match:
        #         print("match (): ", match.start(), match.end())
        #         str = match.group()
        #         # print(str[match.start()-1: match.end()-3])
        #         pair = str[match.start()-1: match.end()-3].split()
        #         LF0_dict[pair[0]] = pair[1]
        #         print(LF0_dict)
        #
        # '''Build LF1 Hash'''