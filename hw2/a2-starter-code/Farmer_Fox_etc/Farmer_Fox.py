'''jiashz_Farmer_Fox_etc.py
by Josh Zhang

Assignment 2, in CSE 415, Winter 2018.

This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

#<METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['Josh Zhang']
PROBLEM_CREATION_DATE = "22-JAN-2018"
PROBLEM_DESC=\
'''This formulation of the Farmer, Fox, Chicken, and Grain problem uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
class State:
  def __init__(self, d):
    self.d = d

  def __eq__(self, s2):
    for p in ['lBank','rBank']:
      if self.d[p] != s2.d[p]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    # Might not be needed in normal operation with GUIs.
    txt = "["
    for bank in ['lBank','rBank']:
      txt += str(self.d[bank]) + " |"
    return txt[:-2]+"]"

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    for bank in ['lBank', 'rBank']:
      news.d[bank]=self.d[bank][:]
    return news

  def can_move(self,From,Item):
    '''Tests whether it's legal to cross the river with Item 
    in state s from the From bank.'''
    try:
      items=self.d[From] # all the items on From bank
      if items==[]: return False  # empty bank
      if 'farmer' not in items: return False # no farmer
      if Item == 'grain' and 'chicken' in items and 'fox' in items: return False
      if Item == '':
      	if len(items) == 4 or len(items) == 2: return True
      	if 'grain' in items and 'chicken' in items or 'chicken' in items and 'fox' in items:
      		return False
      if Item != '' and Item not in items: return False # item
      return True # Disk too big for one it goes on.
    except (Exception) as e:
      print(e)

  def move(self,From,Item):
    '''Assuming it's legal to make the move, this computes
       the new state resulting from crossing the river with Item
       from the From bank.'''
    news = self.copy() # start with a deep copy.
    fBank=news.d[From] # list of items on fBank
    otherBank = None
    if From == 'lBank': 
    	otherBank=news.d['rBank']
    else:
    	otherBank=news.d['lBank']
    news.d[From].remove('farmer') # remove it from the bank.
    otherBank.append('farmer')
    if Item != '': 
    	fBank.remove(Item)
    	otherBank.append(Item)
    return news # return new state
  
def goal_test(s):
  '''If the first two pegs are empty, then s is a goal state.'''
  return s.d['lBank']==[]

def goal_message(s):
  return "The fox, chicken, and grain have been moved across the river!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

#</COMMON_CODE>

#<INITIAL_STATE>
ITEMS = ['farmer', 'chicken', 'fox', 'grain']
INITIAL_DICT = {'lBank': ITEMS, 'rBank':[]}
CREATE_INITIAL_STATE = lambda: State(INITIAL_DICT)
#DUMMY_STATE =  {'peg1':[], 'peg2':[], 'peg3':[] }
#</INITIAL_STATE>

#<OPERATORS>
mv_combinations = [('lBank', carry) for carry in ITEMS[1:4]] + [('rBank', carry) for carry in ITEMS[1:4]]
mv_combinations = mv_combinations + [('lBank', ''), ('rBank', '')]
OPERATORS = [Operator("Crosses the river with " + q + ' from ' + p,
                      lambda s,p1=p,q1=q: s.can_move(p1,q1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,p1=p,q1=q: s.move(p1,q1)) for (p,q) in mv_combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
