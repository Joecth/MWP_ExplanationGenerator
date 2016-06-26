#!/usr/bin/env python3
#coding=utf-8
__author__ = 'JoeXPS13_AS'
import xml.etree.ElementTree as ET
import re
import sys
from statemachine_tv import *
from data20 import *
from xml.dom import minidom

# FILE_INPUT_STC_LOCAL_0 = 'stc_form/ex02.stc.xml'
FILE_INPUT_STC_LOCAL_0 = 'demo_cases/task.UWDS.20160407/data.ENG.UW.DS1.small/uwds-0002.stc.xml'
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

        ## Starting point of How or What
        pat_how = "[h|H]ow|[w|W]hat"
        pat_position_pos = "\(.*\)" # infos within (), such as (3, VBZ)

        VBP = "VBP" #present plural
        VBZ = "VBZ" #present single
        VBD     = "VBD" #past tense
        VBN = "VBN" #past participle
        VB = "VB\)"
        ''' if can't get tense, we try to get modal'''
        MD_will = "will.*MD"
        MD_must = "must.*MD"

        cargo = []

        # pat_basic_token = "\w+\(" # how(
        pat_basic_token = "\w+[-|\w+]*\(" ##uw-228:light-year
        pat_orig_token = "{.*}"

        ret_tense = None
        ret_modal = None
        ret_verb_bakup = None
        is_start_recording = False
        how_pos = -1
        compare_pos = INF
        conj_pos = INF
        is_compare_q = False
        for child_of_root in root:
            for phase in child_of_root.iter('Phase'):
                for unit in phase.iter('Unit'):
                    for unitcand in unit.iter('UnitCand'):
                        for ques in unitcand.iter('Ques'):
                            for sent in ques.iter('Sent'):
                                for cand in sent.iter('Cand'):
                                    for wordlist in cand.iter('WordList'):
                                        for word in wordlist.iter('Word'):
                                            match = re.search(pat_basic_token, word.text)
                                            basic = orig_word = None
                                            if match:
                                                basic = match.group()[0:-1]

                                            match = re.search(pat_orig_token, word.text)
                                            if match:
                                                orig_word = match.group()[1:-1]

                                            if not basic or not match:
                                                print("Check the STC file")
                                                assert(0)
                                            if basic in comparison_words_dict:
                                                # for UIUC set issue. how is not "How"
                                                if 'how' in basic2orig_dict or \
                                                    'How' in basic2orig_dict or \
                                                    'what' in basic2orig_dict or \
                                                    'What' in basic2orig_dict:
                                                    is_compare_q = True
                                            basic2orig_dict[basic] = orig_word

                                            ## we don't start recording until find "how" or "How"
                                            ## to solve clause issue, check 76, 253
                                            if re.search(pat_how, word.text):
                                                is_start_recording = True
                                                how_token = re.search(pat_position_pos, word.text).group()[1:-1] ## position of "how"
                                                infos = how_token.split(",")
                                                how_pos = int(infos[0])

                                            if is_start_recording:
                                            # print(word.text)
                                                position_token = re.search(pat_position_pos, word.text).group()[1:-1]
                                                infos = position_token.split(',')
                                                POS = infos[1] # Part of Speach

                                                ## TODO: call into tv_statemachine here
                                                # POS_orig = (POS, orig_word)
                                                cargo.append((POS, orig_word))

                                                if basic in conj_set:
                                                    conj_pos = int(infos[0])
                                                    break     # prune conject clause's info

                                                ''' State Machine for getting exact Tense '''


                                                ''' Old Flow ↓ '''
                                                '''
                                                if re.search(VBP, word.text):
                                                    if ret_tense == None:
                                                        ret_tense = "VBP"
                                                    # match = re.search(pat_orig_token, word.text)
                                                    ret_verb_bakup = orig_word #match.group()[1:-1]
                                                elif re.search(VBZ, word.text):
                                                    ret_tense = "VBZ"
                                                    # match = re.search(pat_orig_token, word.text)
                                                    ret_verb_bakup = orig_word #match.group()[1:-1]
                                                    # break       ### as uwds-0076, VBZ higher priority than VBP
                                                elif re.search(VBD, word.text):
                                                    ret_tense = "VBD"
                                                    # match = re.search(pat_orig_token, word.text)
                                                    ret_verb_bakup = orig_word #match.group()[1:-1]
                                                    # break       ### check UWDS1/uwds-0015, VBD should have higher priority
                                                elif re.search(VBN, word.text):
                                                    ret_tense = "VBN" ## not tested yet, since we don't have such case
                                                    # match = re.search(pat_orig_token, word.text)
                                                    ret_verb_bakup = orig_word #match.group()[1:-1]
                                                    # break
                                                ### Modal: will, would, should ... ###
                                                elif re.search(MD_will, word.text):
                                                    # match = re.search(pat_orig_token, word.text)
                                                    ret_modal = orig_word #match.group()[1:-1]
                                                elif re.search(MD_must, word.text):
                                                    ret_modal = orig_word
                                                elif re.search(VB, word.text):
                                                    # ret_tense = "VB" VB has no tense info
                                                    # match = re.search(pat_orig_token, word.text)
                                                    ret_verb_bakup = orig_word #match.group()[1:-1]
                                                else:
                                                    pass
                                                '''
                                                '''Old Flow ↑ '''
        # print ("cargos : " )
        # for tmp in cargo:
        #     print (tmp)
        s_tv = statemachine_tv(cargo)
        state, orig_verb = s_tv.go()
        ### TODO in uwds-0005, stanford parsing tree treat 'plant' as NN, thus state is Z3 state...
        illegal_pat = 'Z\d'
        match = re.search(illegal_pat, state)
        if match:
            return (-1, None, ret_modal, None, how_pos, conj_pos, is_compare_q)

        if state == 'error_state':
            return (-2, None, ret_modal, None, how_pos, conj_pos, is_compare_q)

        num_pat = '\d+\w'  ## 11A_state, 12B_state... etc
        match = re.search(num_pat, state)
        if match:
            tmp = match.group()
            ret_tense = tmp[:-1]
            ret_voice = tmp[-1]
            if tmp == '1B':
                if 'VBP'in state:
                    ret_voice = ret_voice + '_VBP'
                elif 'VBZ' in state:
                    ret_voice = ret_voice + '_VBZ'
                else:
                    print('Illegal 1B state')
                    assert(0)
        else:
            print('No state found!')
            assert(0)

        if int(ret_tense) >= 9: ## MD
            ret_modal = orig_word

        if (int(ret_tense) == 1 and (ret_voice == 'B_VBP' or ret_voice =='B_VBZ')) or \
           (int(ret_tense) == 5 and (ret_voice == 'B')): #B is active
            orig_verb = orig_verb[1:]

        verb = ''
        tmp = list(orig_verb)
        for item in orig_verb:
            verb += item
            if 1 != len(tmp):
                verb += ' '
            tmp.pop(0)
        # print (verb)

        return (ret_tense, ret_voice, ret_modal, verb, how_pos, conj_pos, is_compare_q)

if(__name__ == "__main__"):
    input_file = FILE_INPUT_STC_LOCAL_0
    obj = STCAnalyzer(input_file)
    print(obj.get_info())
