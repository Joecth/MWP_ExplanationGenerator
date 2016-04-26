#!/usr/bin/env python3
#coding=utf-8
__author__ = 'JoeXPS13_AS'

from lft_parser import *

FILE_INPUT_LFT_LOCAL_0        = 'logic_form/ex01.lft.xml'  ## try to get all from disk from shell
FILE_INPUT_LFT_LOCAL_0        = 'logic_form/ex07.lft.xml'  ## case of non-terminal node mapping,
                                                           #e.g. (nsubj v4 n15)
                                                           #     (head n15 s4w5),
# sentence = "At eight o'clock on Thursday morning... Arthur didn't feel very good."
# tokens = nltk.word_tokenize(sentence)
FILE_OUTPUT_0       = 'lft_analyzer.out.xml'
FILE_PARSING_LOG_0  = 'log.txt'

class LogicFormAnalyzer:
    def __init__(self, input_file):
        # print("Hello World")
        self.__input_file = input_file
        self.__log  = FILE_PARSING_LOG_0
        self.__LF_dicts = None
        self.__LF0_dict = None
        self.__LF1_dict = None
        self.__LF1_vm_dict = None #var mapping dictionary
        if (False == self.validate()):
            # print("Invalid LF!!")
            sys.exit(2)

    def has_lftfile(self):
        if not self.__input_file:
            return False
        return True

    def validate(self):

        # print(self.__input_file)
        parser = LogicFormParser(self.__input_file, self.__log)
        LF_lists = parser.parse() # return LF0 and LF1 tokens
        # try:
        #     opts, args = getopt.get
        # print("LF0 list: ", LF_lists[0])
        # print("LF1 list: ", LF_lists[1])
        #   LF1 list:
        #   ['\t(LF1\n', '\t\t(verb v4 s4w6)\n', '\t\t(dep v4 n5)\n', '\t\t(head n5 s4w3)\n', ...

        LF0_dict = self.logic2dict(LF_lists[0])
        LF1_dict = self.logic2dict(LF_lists[1])
        LF1_vm_dict = self.logicvm2dict(LF_lists[1]) # record mapping-var in LF1
        # print(LF1_vm_dict)

        if None == LF0_dict or None == LF1_dict or None == LF1_vm_dict:
            return False
        self.__LF0_dict = LF0_dict
        self.__LF1_dict = LF1_dict
        self.__LF1_vm_dict = LF1_vm_dict
        return True

    def get_info(self):
        assert(self.__LF1_dict and self.__LF0_dict)
        voice = None
        ret_subj = None
        '''checking Voice'''
        if "verb" not in self.__LF1_dict:  ## checking for "ThereBe" voice
            # print("check case!")
            sys.exit(2)

        if "be" == self.__LF0_dict.get(self.__LF1_dict.get("verb")):
            '''How many xxx "are" there ?'''
            voice = "ThereBe"
            ret_verb = "are"
            '''EG : There are [EG Tree's explanation]''' ##TODO LF1 has no Tense info
        else:
            if "auxpass" in self.__LF1_dict:
                assert("nsubjpass" in self.__LF1_dict) ## not sure LFT's all cases, thus set here for debuggint
                voice = "Passive"
                key_lf0 = self.__LF1_dict.get("verb")
                if not key_lf0:
                    # print("Chcek case's verb!")
                    sys.exit(2)
                if not self.__LF0_dict.get(key_lf0):
                    # print("Check case!")
                    sys.exit(2)

                ret_verb = self.__LF0_dict.get(key_lf0)
                '''EG : [EG Tree's explanation] were/was Ved. '''
            else:
                voice = "Active"
                '''EG : ret_subj V [EG Tree's explanation]. '''
                key_lf0 = self.__LF1_dict.get("nsubj")
                if not key_lf0:
                    # print("Check case's nsubj!")
                    sys.exit(2)
                if not self.__LF0_dict.get(key_lf0):
                    #
                    # might be the case as demo/tmp.edemo.out.20160413/ex07.lft.xml
                    # (nsubj v4 n15)
                    # (head n15 s4w5),
                    # thus, we need to check one more layer
                    # TODO Solve non-terminal node mapping

                    print("LF1 maps to variable!")
                    re_mapping_key = self.__LF1_vm_dict.get(key_lf0)
                    if not re_mapping_key:
                        print("Remapping in LF1 failed, Check case!")
                        sys.exit(2)
                    else:
                        key_lf0 = re_mapping_key
                    # sys.exit(2)
                '''get subject'''
                ret_subj = self.__LF0_dict.get(key_lf0)

                key_lf0 = self.__LF1_dict.get("verb")
                if not key_lf0:
                    # print("Chcek case's verb!")
                    sys.exit(2)
                if not self.__LF0_dict.get(key_lf0):
                    # print("Check case!")
                    sys.exit(2)
                '''get verb'''
                ret_verb = self.__LF0_dict.get(key_lf0)

        ret_dict = {}
        ret_dict["Voice"] = voice
        ret_dict["Subject"] = ret_subj
        ret_dict["Verb"] = ret_verb
        return ret_dict


        '''Build LF1 Hash'''
    def logic2dict(self, LF_list):
        pat = "\(.*\)"  # (s1w2 have), (s1w1 Keith), ... etc
        '''Build LF0 or LF1 Hash'''
        ret_dict = {}
        for token in LF_list:
            match = re.search(pat, token)
            if None != match:
                # print("match (): ", match.start(), match.end())
                str = match.group()
                # print(str[match.start()-1: match.end()-3])
                pair = str[match.start()-1: match.end()-3].split()
                ret_dict[pair[0]] = pair[-1]
                # print(ret_dict)
        return ret_dict
                ## TODO Same tag issue: e.g. 2 advmod

    def logicvm2dict(self, LF_list):
        #e.g. (nsubj v4 n15)   ==> {v4:n15}
        #     (head n15 s4w5), ==> {n15:s4w5} this one will be used, since n15 can't be mapped in LF0_dict
        pat = "\s[n|v].*\)"
        ret_dict = {}
        for token in LF_list:
            match = re.search(pat, token)
            if None != match:
                str = match.group() ## str= " n15 s4w5)"
                pair = str[1:-1].split()
                ret_dict[pair[0]] = pair[-1]
                # print(sentence.split())
        return ret_dict

if(__name__ == "__main__"):
    input_file = FILE_INPUT_LFT_LOCAL_0
    obj = LogicFormAnalyzer(input_file)
    print(obj.get_info())



