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
        ret_verb = None
        pos_verb = None

        '''checking Voice'''
        if "be" == self.__LF0_dict.get(self.__LF1_dict.get("verb")):
            '''How many xxx "are" there ?'''
            voice = "ThereBe"
            # ret_verb = "are"
            '''EG : There are [EG Tree's explanation]''' ##TODO LF1 has no Tense info
        else:
            '''Active or Passive'''
            ''' both need to get verb '''
            '''get verb'''
            if "verb" in self.__LF1_dict:
                key_lf0 = self.__LF1_dict.get("verb")
                if not key_lf0:
                    # print("Chcek case's verb!")
                    sys.exit(2)

                # if not self.__LF0_dict.get(key_lf0):
                #     # print("Check case!")
                #     sys.exit(2)
                ret_verb, pos_verb = self.extract_lf1_encoded_info(key_lf0)
                # ret_verb = self.__LF0_dict.get(key_lf0)
            if "auxpass" in self.__LF1_dict:
                assert("nsubjpass" in self.__LF1_dict) ## not sure LFT's all cases, thus set here for debuggint
                voice = "Passive"
                '''EG : [EG Tree's explanation] were/was Ved. '''
            else:
                voice = "Active"
                '''EG : ret_subj V [EG Tree's explanation]. '''
                key_lf0 = self.__LF1_dict.get("nsubj")
                if not key_lf0:
                    # print("Check case's nsubj!")
                    sys.exit(2)
                # might be the case as demo/tmp.edemo.out.20160413/ex07.lft.xml
                # (nsubj v4 n15)
                # (head n15 s4w5),
                # thus, we need to check one more layer

                ret_subj, pos_noun_nouse = self.extract_lf1_encoded_info(key_lf0)


        ret_dict = {}
        ret_dict["Voice"] = voice
        ret_dict["Subject"] = ret_subj
        if ret_verb:
            ret_dict["Verb"] = ret_verb
        return ret_dict, pos_verb


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

        # pat = "\s[n|v].*\)"
        pat = "\s[\w].*\)"
        ret_dict = {}
        for token in LF_list:
            match = re.search(pat, token)
            if None != match:
                str = match.group() ## str= " n15 s4w5)"
                pair = str[1:-1].split()

                key = pair[0]
                word = pair[-1]
                if key in ret_dict:
                    ## e.g.:
                    #(nsubj v3 n14)
		            #(head n14 s3w8)
		            #(det n14 s3w7) , where n14 = s3w7+s3w8
                    ### Purpose: {n14:[s3w7, s3w8]} 
                    wordlist = []

                    orig_value = ret_dict.get(key)
                    if isinstance(orig_value, list):
                        wordlist.extend(orig_value)
                        #for tmp in dict.get(key):
                        #    value.append(tmp)
                    else:
                        wordlist.append(orig_value)
                    wordlist.append(word)
                    wordlist.sort()
                    ret_dict[key] = wordlist #pair[-1] ==> [s3w7, s3w8]
                else:
                    ret_dict[key] = word
                # print(sentence.split())
        return ret_dict

    def extract_lf1_encoded_info(self, key_lf0):
        ret_str = ""
        ret_1st_elem = key_lf0
        if key_lf0 in self.__LF0_dict:
            ret_str = self.__LF0_dict.get(key_lf0)
        else: ## key_lf0 should be still a variable or wordlist,
                                        # i.e, n14 or [s3w7, s3w8]
            # might be the case as demo/tmp.edemo.out.20160413/ex07.lft.xml
            # (nsubj v4 n15)
            # (head n15 s4w5),
            # thus, we need to check one more layer

            # print("LF1 maps to variable!")
            re_mapping_key = self.__LF1_vm_dict.get(key_lf0)
            ## re_mapping_key should be n# or [s3w7, s3w8]
            if not re_mapping_key:
                print("Remapping in LF1 failed, Check case!")
                sys.exit(2)

            key_lf0 = re_mapping_key

            '''get subject or verb'''
            if isinstance(key_lf0, list):
                decoded_lf0_keys = self.get_back_all_orig_lf0_keys(key_lf0)

                # for token in key_lf0:
                #     elem = self.get_back_all_orig_lf0_keys(token)
                #     lf0_keys.append(elem)
                # lf0_keys.sort()
                ret_1st_elem = decoded_lf0_keys[0]
                for word in decoded_lf0_keys:
                    ret_str += self.extract_lf1_encoded_info(word)[0]
                    ret_str += " "
                if ret_str[-1] == " ":
                    ret_str = ret_str[:-1]
            else: # it's merely a string
                ret_str += self.extract_lf1_encoded_info(key_lf0)[0]
                #str = self.__LF0_dict.get(key_lf0)

        return [ret_str, ret_1st_elem]

    def get_back_all_orig_lf0_keys(self, lf0_keys):
        ## lf0_keys: [n4, n5, s3w7, s3w8], we want to decode n4 and n5 to return list with all s3w#
        ret_val = []
        for lf0_key in lf0_keys:

            if lf0_key in self.__LF0_dict:
                ret_val.append(lf0_key)
            else:
                ## token is n3, n4,... etc, instead of s3w7, s3w8... etc
                re_map_lf0_key = self.__LF1_vm_dict.get(lf0_key)
                if isinstance(re_map_lf0_key, list):
                    ret_val = self.get_back_all_orig_lf0_keys(re_map_lf0_key)
                else:
                    ## 0005's n17 in such case...
                    # print("Unexpected dummy variable in LFT!\n")
                    # assert(0)
                    # key = self.__LF1_vm_dict.get(re_map_lf0_key)
                    ret_val.append(re_map_lf0_key)
        ret_val.sort()
        return ret_val


if(__name__ == "__main__"):
    input_file = FILE_INPUT_LFT_LOCAL_0
    obj = LogicFormAnalyzer(input_file)
    print(obj.get_info())



