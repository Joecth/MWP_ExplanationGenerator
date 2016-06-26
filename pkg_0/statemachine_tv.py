#!/usr/bin/env python3
#coding=utf-8
__author__ = 'JoeXPS13_AS'
'''StateMachine for Tense and Voice Extraction'''
'''
Description:

>>>TENSE:
                 Basic      Progressive     Perfect     Perfect Progressive
Present            1            2              3                4
Past               5            6              7                8
Future & MD        9            10             11               12


>>>VOICE:
A -- ThereBe
B -- Active
C -- Passive

'''
from statemachine import StateMachine
from data20 import stanford_issue_dict
actions = set(['VBZ', 'VBP', 'VBN', 'VBG', 'VB', 'MD', 'VBD'])
'1A'
l1A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'are'),
                ('PRP', 'now'), ('RB', 'there')]
'1B VBP'
l1B_VBP = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'do'),
                ('PRP', 'they'), ('VB', 'have'), ('RB', 'now')]
                                #^^^^^^^ should be VB for other verbs
'1B VBZ'
l1B_VBZ = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBZ', 'does'),
       ('PRP', 'he'), ('VB', 'have'), ('RB', 'now')]
                                #^^^^^^^ should be VB for other verbs
'1C'
l1C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'are'),
                ('PRP', 'now'), ('VBN', 'picked')]
'2A'
l2A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'are'),
                ('RB', 'now'), ('VBG', 'being'), ('RB', 'there')]
'2B'
l2B = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'are'),
                ('PRP', 'they'), ('VBG', 'picking'), ('RB', 'now')]
'2C'
l2C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'are'),
                ('RB', 'now'), ('VBG', 'being'), ('VBN', 'picked')]

'3A'
l3A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'have'),
       ('VBN', 'been'), ('RB', 'there')]
'3B'
l3B = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'have'),
       ('PRP', 'they'), ('VBN', 'picked'), ('RB', 'now')]
'3C'
l3C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'have'),
       ('VBN', 'been'), ('VBN', 'picked')]

'4A'
l4A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'have'),
       ('VBN', 'been'), ('VBG', 'being'), ('RB', 'there')]
'4B'
l4B = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'have'),
       ('PRP', 'they'), ('VBN', 'been'), ('VBG', 'picking')]
'4C'
l4C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBP', 'have'),
       ('VBN', 'been'), ('VBG', 'being'), ('VBN', 'picked')]

'''Past Tense Testing'''
'5A'
l5A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'were'),
                ('PRP', 'now'), ('RB', 'there')]
'5B'
l5B = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'did'),
                ('PRP', 'they'), ('VB', 'have'), ('RB', 'now')]
                                #^^^^^^^ should be VB for other verbs
'5C'
l5C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'were'),
                ('RB', 'slightly'), ('VBN', 'picked')]

'6A'
l6A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'were'),
                ('RB', 'then'), ('VBG', 'being'), ('RB', 'there')]
'6B'
l6B = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'were'),
                ('PRP', 'they'), ('VBG', 'picking'), ('RB', 'now')]
'6C'
l6C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'were'),
                ('RB', 'then'), ('VBG', 'being'), ('VBN', 'picked')]

'7A'
l7A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'had'),
       ('VBN', 'been'), ('RB', 'there')]
'7B'
l7B = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'had'),
       ('PRP', 'they'), ('VBN', 'picked'), ('RB', 'now')]
'7C'
l7C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'had'),
       ('VBN', 'been'), ('VBN', 'picked')]

'8A'
l8A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'had'),
       ('VBN', 'been'), ('VBG', 'being'), ('RB', 'there')]
'8B'
l8B = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'had'),
       ('PRP', 'they'), ('VBN', 'been'), ('VBG', 'picking')]
'8C'
l8C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('VBD', 'had'),
       ('VBN', 'been'), ('VBG', 'being'), ('VBN', 'picked')]

'9A'
l9A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'will'),
                ('VB', 'be'), ('RB', 'there')]
'9B'
l9B = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'will'),
                ('PRP', 'they'), ('VB', 'have'), ('RB', 'then')]
'9C'
l9C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'will'),
                ('VB', 'be'), ('VBN', 'picked')]


'10A'
l10A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'will'),
                ('VB', 'be'), ('VBG', 'being'), ('RB', 'there')]
'10B'
l10B = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'will'),
                ('PRP', 'they'), ('VB', 'be'), ('VBG', 'picking')]
'10C'
l10C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'will'),
                ('VB', 'be'), ('VBG', 'being'), ('VBN', 'picked')]

'11A'
l11A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'should'),
       ('VB', 'have'), ('VBN', 'been'), ('RB', 'there')]
'11B'
l11B = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'should'),
       ('VB', 'have'), ('PRP', 'they'), ('VBN', 'picked')]
'11C'
l11C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'should'),
       ('VB', 'have'), ('VBN','been'), ('VBN', 'picked')]

'12A'
l12A = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'should'),
       ('VB', 'have'), ('VBN', 'been'), ('VBG', 'being'), ('RB', 'there')]
'12B'
l12B = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'will'),
       ('PRP', 'they'), ('VBP', 'have'), ('VBN', 'been'), ('VBG', 'picking')]
'12C'
l12C = [('WRB', 'How'), ('JJ', 'many'), ('NNS', 'books'), ('MD', 'should'),
        ('VBP','have'), ('VBN', 'been'), ('VBG', 'being'), ('VBN', 'picked')]

LOCAL_CARGOS = l1B_VBP




class statemachine_tv():
    def __init__(self, cargo):
        self.__cargos = list(cargo)

    def set_cargo(self, cargo):
        self.__cargos = list(cargo)

    def start_transitions(self, cargo):
        # Present, Past, MD
        # Present : 1A, Z1, Z2
        # Past    : 5A, Z3, Z4
        # MD      : ZM

        # splitted_txt = txt.split(None,1)
        # words, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
        item = cargo[0]
        cargo.pop(0)
        words =  item[0] + '(' + item[1] + ')' ## VBP(do)

        if words == "VBZ(is)" or words == 'VBP(are)':
            newState = "1A_state"
        # elif words == 'VBZ(does)' or words == 'VBP(do)':
        #     newState = 'Z1_state'   <== we need to seperate VBZ and VBP, since 1B requires verb's morphology
        elif words == 'VBP(do)':
            newState = 'Z1_VBP_state'
        elif words == 'VBZ(does)':
            newState = 'Z1_VBZ_state'
        elif words == 'VBZ(has)' or words == 'VBP(have)':
            newState = 'Z2_state'
        elif words == 'VBD(was)' or words == 'VBD(were)':
            newState = '5A_state'
        elif words == 'VBD(did)':
            newState = 'Z3_state'
        elif words == 'VBD(had)':
            newState = 'Z4_state'
        elif words[:2] == 'MD':
            # already checked safety outside
            newState = 'ZM_state'
        else:
            if 'VBP' in words:  ## uwds-166, we create 5D state for Quantity Subject
                newState = '1D_state'
            else:
                newState = "error_state"
        # return (newState, txt)
        return (newState, cargo)

    def _1A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN':
            if orig_word != 'been':
                newState = '1C_state'
            else :
                newState = 'error_state'
        elif POS == 'VBG':
            if orig_word == 'being':
                newState = '2A_state'
            else:
                newState = '2B_state'
        elif POS == 'VB': ## ilds-0005..
            if orig_word == 'total':
                newState = '1A_state'
            else:
                newState = 'error_state'
        else:
            newState = "error_state"
        return (newState, cargo)

    def _Z1_VBP_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VB':
            if orig_word != 'be':
                newState = '1B_VBP_state'
            else :
                newState = 'error_state'
        elif POS == 'VBP':
            # if orig_word == 'have' or orig_word == 'find' or orig_word == 'sell' or orig_word == 'use' or\
            #    orig_word == 'produce': ## for uwds-15, Stanford parser's issue, I walk around here
            ## eat: uw-183
            if orig_word in stanford_issue_dict:
                newState = '1B_VBP_state'
            else:
                newState = 'error_state'
        else:
            newState = "error_state"
        return (newState, cargo)

    def _Z1_VBZ_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VB':
            if orig_word != 'be':
                newState = '1B_VBZ_state'
            else :
                newState = 'error_state'
        elif POS == 'VBP':
           # if orig_word == 'have' or orig_word == 'find' or orig_word == 'sell' or orig_word == 'use' or\
            #    orig_word == 'produce': ## for uwds-15, Stanford parser's issue, I walk around here
            ## sell: uw158; use: uw161
            if orig_word in stanford_issue_dict:
                newState = '1B_VBZ_state'
            else:
                newState = 'error_state'
        else:
            newState = "error_state"
        return (newState, cargo)

    def _1B_state_transitions(self, cargo): ## Also: 1C
        '''Terminal'''
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]
        # Terminal State
        print('in 1B STATE. Shouldn\'t be called into!\n ITEMS: '+ item[0] + item[1])
        new_state = '1B_state'
        return (new_state, cargo)

    def _2A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]
        if POS == 'VBN':
            newState = '2C_state'
        else:
            newState = 'error_state'
        return (newState, cargo)

    def _Z2_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN':
            if orig_word != 'been':
                newState = '3B_state'
            else:
                newState = '3A_state'
        else:
            newState = 'error_state'
        return (newState, cargo)

    def _3A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN':
            if orig_word != 'been':
                newState = '3C_state'
            else:
                newState = 'error_state'
        elif POS == 'VBG':
            if orig_word == 'being':
                newState = '4A_state'
            else:
                newState = '4B_state'
        else:
            newState = 'error_state'
        return (newState, cargo)

    def _3B_state_transitions(self, cargo): # 3C, 4B are same
        '''Terminal State, no need'''
        pass

    def _4A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN':
            if orig_word != 'been':
                newState = '4C_state'
            else:
                newState = 'error_state'
        return (newState, cargo)

    '''Past'''
    def _5A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN':
            if orig_word != 'been':
                newState = '5C_state'
            else :
                newState = 'error_state'
        elif POS == 'VBG':
            if orig_word == 'being':
                newState = '6A_state'
            else:
                newState = '6B_state'
        else:
            newState = "error_state"
        return (newState, cargo)

    def _Z3_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VB':
            if orig_word != 'be':
                newState = '5B_state'
            else :
                newState = 'error_state'
        elif POS == 'VBP':
            # if orig_word == 'have' or orig_word == 'find' or orig_word == 'sell' or orig_word == 'use' or\
            #    orig_word == 'produce': ## for uwds-15, Stanford parser's issue, I walk around here
            ## sell: uw158; use: uw161
            if orig_word in stanford_issue_dict:
                newState = '5B_state'
            else:
                newState = 'error_state'
        else:
            if orig_word == 'cut':## uw-178... cut is tagged as VBD...
                newState = '5B_state'
            else:
                newState = "error_state"
        return (newState, cargo)

    def _5B_state_transitions(self, cargo): ## Also: 5C
        '''Terminal'''
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]
        # Terminal State
        print('in 5B STATE. Shouldn\'t be called into!\n ITEMS: '+ item[0] + item[1])
        new_state = '5B_state'
        return (new_state, cargo)

    def _5D_state_transitions(self, cargo): ## Also: 5C
        '''Terminal'''
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]
        # Terminal State
        print('in 5D STATE. Shouldn\'t be called into!\n ITEMS: '+ item[0] + item[1])
        new_state = '5D_state'
        return (new_state, cargo)

    def _6A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]
        if POS == 'VBN':
            newState = '6C_state'
        else:
            newState = 'error_state'
        return (newState, cargo)

    def _Z4_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN' or POS =='VBD':  # case-uw172, we add 'VBD'.. actually, verb like "picked" may be VBD or VBN
            if orig_word != 'been':
                newState = '7B_state'
            else:
                newState = '7A_state'
        else:
            newState = 'error_state'
        return (newState, cargo)

    def _7A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN':
            if orig_word != 'been':
                newState = '7C_state'
            else:
                newState = 'error_state'
        elif POS == 'VBG':
            if orig_word == 'being':
                newState = '8A_state'
            else:
                newState = '8B_state'
        else:
            newState = 'error_state'
        return (newState, cargo)

    def _7B_state_transitions(self, cargo): # 7C, 8B are same
        '''Terminal State, no need'''
        pass

    def _8A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN':
            if orig_word != 'been':
                newState = '8C_state'
            else:
                newState = 'error_state'
        return (newState, cargo)

    '''Future and MD'''
    def _ZM_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VB':
            if orig_word == 'be':
                newState = '9A_state'
            # elif orig_word == 'have': ###### Special process
                # newState = 'Z5_state' ######
            else:
                newState = '9B_state' ## 9B should merge with Z5
        elif POS == 'VBP':
            ## handle Stanford CoreNLP suit's tag issue : VB(have) and VBP(have)
            if orig_word == 'have':
                newState = '9B_state'
            else:
                newState = 'error_state'
        else:
            newState = 'error_state'

        return (newState, cargo)

    def _9A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN':
            if orig_word != 'been':
                newState = '9C_state'
            else :
                newState = 'error_state'
        elif POS == 'VBG':
            if orig_word == 'being':
                newState = '10A_state'
            else:
                newState = '10B_state'
        else:
            newState = "error_state"
        return (newState, cargo)


    def _10A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]
        if POS == 'VBN':
            newState = '10C_state'
        else:
            newState = 'error_state'
        return (newState, cargo)

    def _9B_state_transitions(self, cargo):
        '''Serve as Z5 state'''
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN':
            if orig_word != 'been':
                newState = '11B_state'
            else:
                newState = '11A_state'
        else:
            newState = 'error_state'
        return (newState, cargo)

    def _11A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN':
            if orig_word != 'been':
                newState = '11C_state'
            else:
                newState = 'error_state'
        elif POS == 'VBG':
            if orig_word == 'being':
                newState = '12A_state'
            else:
                newState = '12B_state'
        else:
            newState = 'error_state'
        return (newState, cargo)

    def _11B_state_transitions(self, cargo): # 7C, 8B are same
        '''Terminal State, no need'''
        pass

    def _12A_state_transitions(self, cargo):
        item = cargo[0]
        cargo.pop(0)
        POS = item[0]
        orig_word = item[1]

        if POS == 'VBN':
            if orig_word != 'been':
                newState = '12C_state'
            else:
                newState = 'error_state'
        return (newState, cargo)

    def go(self):
        m = StateMachine()
        # for  tmp in self.__cargos:
        #     print(tmp)
        '''Present'''
        m.add_state("Start", self.start_transitions)
        m.add_state('1A_state', self._1A_state_transitions)
        m.add_state('1C_state', None, end_state=1)
        m.add_state('2A_state', self._2A_state_transitions)
        m.add_state('2B_state', None, end_state=1)
        m.add_state('2C_state', None, end_state=1)

        m.add_state('Z1_VBP_state', self._Z1_VBP_state_transitions)
        m.add_state('Z1_VBZ_state', self._Z1_VBZ_state_transitions)
        m.add_state('1B_VBP_state', None, end_state=1)
        m.add_state('1B_VBZ_state', None, end_state=1)
        m.add_state('1D_state', None, end_state=1)  ### TODO: review, we add quan-subj state for uw-166

        m.add_state('Z2_state', self._Z2_state_transitions)
        m.add_state('3A_state', self._3A_state_transitions)
        m.add_state('3B_state', None, end_state=1)
        m.add_state('3C_state', None, end_state=1)
        m.add_state('4A_state', self._4A_state_transitions)
        m.add_state('4B_state', None, end_state=1)
        m.add_state('4C_state', None, end_state=1)

        '''Past'''
        m.add_state('5A_state', self._5A_state_transitions)
        m.add_state('5C_state', None, end_state=1)
        m.add_state('6A_state', self._6A_state_transitions)
        m.add_state('6B_state', None, end_state=1)
        m.add_state('6C_state', None, end_state=1)

        m.add_state('Z3_state', self._Z3_state_transitions)
        m.add_state('5B_state', None, end_state=1)

        m.add_state('Z4_state', self._Z4_state_transitions)
        m.add_state('7A_state', self._7A_state_transitions)
        m.add_state('7B_state', None, end_state=1)
        m.add_state('7C_state', None, end_state=1)
        m.add_state('8A_state', self._8A_state_transitions)
        m.add_state('8B_state', None, end_state=1)
        m.add_state('8C_state', None, end_state=1)

        '''Future and MD'''
        m.add_state('ZM_state', self._ZM_state_transitions)
        m.add_state('9A_state', self._9A_state_transitions)
        m.add_state('9C_state', None, end_state=1)
        m.add_state('10A_state', self._10A_state_transitions)
        m.add_state('10B_state', None, end_state=1)
        m.add_state('10C_state', None, end_state=1)

        # m.add_state('Z3_state', self._Z3_state_transitions)
        m.add_state('9B_state', self._9B_state_transitions)

        # m.add_state('Z5_state', self._Z5_state_transitions) Z5 merged with 9B
        m.add_state('11A_state', self._11A_state_transitions)
        m.add_state('11B_state', None, end_state=1)
        m.add_state('11C_state', None, end_state=1)
        m.add_state('12A_state', self._12A_state_transitions)
        m.add_state('12B_state', None, end_state=1)
        m.add_state('12C_state', None, end_state=1)
        m.add_state('error_state', None, end_state=1)

        m.set_start("Start")
        m.run(self.__cargos, actions)

        return m.get_tvstate(), m.get_action()
        # for item in self.__cargo:
        #     if item[0] in actions:
        #         m.run(self.__cargo)


if __name__== "__main__":
    '''original testing'''
    s_tv = statemachine_tv(LOCAL_CARGOS)
    print(s_tv.go())

    CARGO = 'l'
    VOICE = 'A'
    for tmp in range(12):
        idx = tmp+1
        for tt in range(3):
            if 0 == tt % 3:
                tt = 'A'
            elif 1 == tt % 3:
                tt = 'B'
            elif 2 == tt % 3:
                tt = 'C'
            else:
                assert(0)
            CARGO = 'l' + str(idx) + tt
            if CARGO[:3] == 'l1B':
                for tmp in range(2):
                    if tmp == 0:
                        CARGO_x = CARGO + '_VBP'
                    else:
                        CARGO_x = CARGO + '_VBZ'
                    s_tv = statemachine_tv(eval(CARGO_x))
                    print(s_tv.go())
            else:
                s_tv = statemachine_tv(eval(CARGO)) ## eval: treat str as variable
                print(s_tv.go())
            # print(CARGO)


        # CARGO = 'l'+idx+
        # s_tv.set_cargo(l1A)
        # s_tv.go()

    # m.add_state("Start", start_transitions)
    # m.add_state('error_state', None, end_state=1)
