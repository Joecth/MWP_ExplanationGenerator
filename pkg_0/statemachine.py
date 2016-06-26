#!/usr/bin/env python3
#coding=utf-8
__author__ = 'JoeXPS13_AS'

class StateMachine():
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []
        self.tv_state = None
        self.actions = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
             self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo, actions=None):
        try:
           handler = self.handlers[self.startState]
        except BaseException:
           raise "must call .set_start() before .run()"

        if not self.endStates:
            # raise  "InitializationError", "at least one state must be an end_state"
            raise  "at least one state must be an end_state"

        newState = None
        ret_verb = []
        while 1:
            if actions:
                for item in cargo:
                    # print(item)
                    if item[0] in actions:
                        (newState, cargo) = handler(cargo)
                        if newState == 'error_state':
                            cargo = None
                            break
                        ret_verb.append(item[1])
                        if newState.upper() in self.endStates:
                            # print("reached ", newState, "which is an end state.")
                            break
                        else:
                            tmp_new = newState.upper()
                            if tmp_new not in self.handlers:
                                raise NameError('No such state! : '+tmp_new)
                            handler = self.handlers[tmp_new]
                    # elif item[0] == 'TO': ## solve uwds-210 verb to verb issue, we don't care the verb after "TO"
                    #     cargo = None
                    #     break
                    else:
                        cargo = cargo[1:]
            if not cargo:
                # print('STATE: '+newState)
                self.tv_state = newState
                self.actions = ret_verb
                break

    def get_tvstate(self):
        return self.tv_state

    def get_action(self):
        return self.actions
    def aaa(tmp):
        print ("hey! "+tmp)



if __name__ == "__main__":
    print("main is : "+__file__)

