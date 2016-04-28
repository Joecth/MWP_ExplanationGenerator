#!/usr/bin/env python3
#coding=utf-8
__author__ = 'JoeXPS13_AS'
import xml.etree.ElementTree as ET
import re
import sys
from xml.dom import minidom

FILE_INPUT_STC_LOCAL_0 = 'stc_form/ex0.stc.xml'
FILE_PARSING_STC_LOG_0 = 'stc_parsing.log'

class STCAnalyzer:
    def __init__(self, input_file):
        self.__input_file = input_file
        self.__log = FILE_PARSING_STC_LOG_0

    def get_info(self):
        try:
            tree = ET.ElementTree(file=self.__input_file)
        except FileNotFoundError as e:
            print("STC file is not found => Tense Error") ## for Tense info
            sys.exit(2)
        root = tree.getroot()
        # print(root.tag, root.attrib)

        pat_present_p = "VBP" #present plural
        pat_present_z = "VBZ" #present single
        pat_past_     = "VBD" #past
        pat_past_participle = "VBN" #past participle

        ''' if can't get tense, we try to get modal'''
        pat_future_lama = "will.*MD"
        pat_get_modal = "{.*}"

        ret_tense = None
        ret_modal = None
        for child_of_root in root:
            for phase in child_of_root.iter('Phase'):
                for unit in phase.iter('Unit'):
                    for unitcand in unit.iter('UnitCand'):
                        for ques in unitcand.iter('Ques'):
                            for sent in ques.iter('Sent'):
                                for cand in sent.iter('Cand'):
                                    for wordlist in cand.iter('WordList'):
                                        for word in wordlist.iter('Word'):
                                            # print(word.text)
                                            if re.search(pat_present_p, word.text):
                                                ret_tense = "VBP"
                                            elif re.search(pat_present_z, word.text):
                                                ret_tense = "VBZ"
                                                break       ### as uwds-0076, VBZ higher priority than VBP
                                            elif re.search(pat_past_, word.text):
                                                ret_tense = "VBD"
                                                break       ### check UWDS1/uwds-0015, VBD should have higher priority
                                            elif re.search(pat_past_participle, word.text):
                                                ret_tense = "VBN" ## not tested yet, since we don't have such case
                                                break
                                            ### Modal: will, would, should ... ###
                                            elif re.search(pat_future_lama, word.text):
                                                match = re.search(pat_get_modal, word.text)
                                                ret_modal = match.group()[1:-1]
                                            else:
                                                pass
        return (ret_tense, ret_modal)

if(__name__ == "__main__"):
    input_file = FILE_INPUT_STC_LOCAL_0
    obj = STCAnalyzer(input_file)
    print(obj.get_info())
