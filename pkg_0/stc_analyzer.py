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

    # def validate(self):
    #     print("Hello STC Analyzer")

    def get_info(self):
        try:
            tree = ET.ElementTree(file=self.__input_file)
        except FileNotFoundError as e:
            print("STC file is not found => Tense Error") ## for Tense info
            sys.exit(2)
        root = tree.getroot()
        print(root.tag, root.attrib)

        # for child_of_root in root:
        #     print(child_of_root.tag, child_of_root.attrib)

        # for tmp in root.findall('Ques'):
        #     print(tmp)

        pat_present_p = "VBP" #present plural
        pat_present_z = "VBZ" #present single
        pat_past_     = "VBD" #past

        ret_tense = "VBP"
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
                                            elif re.search(pat_past_, word.text):
                                                ret_tense = "VBD"
                                            else:
                                                pass
        return ret_tense
        # xmldoc = minidom.parse(FILE_INPUT_STC_LOCAL_0)
        # ques = xmldoc.getElementsByTagName('Ques')
        #
        # print(len(ques))
        # for sent in ques:
        #     '''for now, sent is only 1'''
        #     for cand in sent.childNodes:
        #         if cand.nodeType == cand.ELEMENT_NODE:
        #             for wordlist in cand.childNodes:
    #                 if wordlist.nodeType == wordlist.ELEMENT_NODE:
    #                     for word in wordlist.childNodes:
    #                         if word.nodeType == word.ELEMENT_NODE:
    #                             if word.localName == "WordList":
    #                                 print(word)

if(__name__ == "__main__"):
    input_file = FILE_INPUT_STC_LOCAL_0
    obj = STCAnalyzer(input_file)
    print(obj.get_info())
