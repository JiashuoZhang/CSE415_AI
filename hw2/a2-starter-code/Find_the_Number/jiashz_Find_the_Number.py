'''jiashz_Farmer_Fox_etc.py
by Josh Zhang

Assignment 2, in CSE 415, Winter 2018.

This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''
#<METADATA>
QUIET_VERSION = "1.0"
PROBLEM_NAME = "Find the Number"
PROBLEM_VERSION = "1.1"
PROBLEM_AUTHORS = ['Josh Zhang']
PROBLEM_CREATION_DATE = "22-JAN-2018"
PROBLEM_DESC=\
'''This formulation of the Find the Number problem uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.
'''
#</METADATA>

#<COMMON_DATA>
secret_number = 0
max_n = 10

try:
  import sys
  arg2 = sys.argv[2]
  arg3 = sys.argv[3]
  secret_number = int(arg2)
  max_n = int(arg3)
  print("A new secret number was successfully read in from the command line: " + arg2)
  print("A new maximum number (range limit) was successfully read in from the command line: " + arg3)

except:
  print("Using default maximum number: "+str(max_n))
  print(" (To use a specific number, enter it on the command line, e.g.,")
  print("python3 ../Int_Solv_Client.py jiashz_Farmer_Fox_etc 100")
#</COMMON_DATA>

#<COMMON_CODE>
class State:
	"""docstring for State"""
	def __init__(self, d):
		self.possibilities = d
		self.phase = 0
		self.last_m = None

	def __eq__(self, s):
		return self.possibilities == s.possibilities and self.phase == s.phase and self.last_m == s.last_m

	def __str__(self):
		txt = "question_phase: " + str(self.phase) + "\n"
		txt += str(self.last_m) + "\n"
		txt += str(self.possibilities)
		return txt

	def __hash__(self):
		return (self.__str__).__hash__()

	def copy(self):
		news = State([])
		news.possibilities = self.possibilities[:]
		news.phase = self.phase
		news.last_m = self.last_m
		return news

	def can_move(self, n, q_phase):
		try:
			if q_phase != self.phase:
				return False
			if q_phase == 0:
				return True
			return n < self.last_m
		except Exception as e:
			print(e)

	def move(self, n, q_phase):
		news = self.copy()
		if q_phase == 0:
			news.phase = 1
			news.last_m = n
		else:
			expected = is_n_minus_k_divisible_by_m(secret_number, n, self.last_m)
			news.possibilities = [x for x in news.possibilities if is_n_minus_k_divisible_by_m(x, n, self.last_m) == expected]
			news.phase = 0
		return news

def goal_test(s):
	return len(s.possibilities) == 1 and s.possibilities[0] == secret_number

def goal_message(s):
	return "You have solved the problem by reaching a goal state."

def isPrimeUnder1000(m):
	return m > 1 and m < 1000 and all(m % i for i in range(2, m))

def is_n_minus_k_divisible_by_m(n, k, m):
    if not isPrimeUnder1000(m):
        return False
    return (n - k) % m == 0

class Operator:
	"""docstring for Operator"""
	def __init__(self, name, precond, state_transf):
		self.name = name
		self.precond = precond
		self.state_transf = state_transf

	def is_applicable(self, s):
		return self.precond(s)

	def apply(self, s):
		return self.state_transf(s)
#</COMMON_CODE>

#</COMMON_CODE>

#<INITIAL_STATE>
INITIAL_POSSIBILITIES = list(range(0, max_n + 1))
CREATE_INITIAL_STATE = lambda: State(INITIAL_POSSIBILITIES)
#</INITIAL_STATE>

#<OPERATORS>
div_combinations = [2, 3, 5, 7]
sub_combinations = list(range(0, 7))
OPERATORS = [Operator("Is N divisible by " + str(p) + ' after ...',
                      lambda s,p1=p: s.can_move(p1, 0),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,p1=p: s.move(p1, 0)) for p in div_combinations]
OPERATORS += [Operator("... subtracting " + str(q) + ' ?',
                      lambda s,q1=q: s.can_move(q1, 1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,q1=q: s.move(q1, 1)) for q in sub_combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
