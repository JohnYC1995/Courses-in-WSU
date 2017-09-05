#Dear Teaching Assistant,I change the code based on the HW2, thanks a lot. This code works well 
# on Macbook python 3

#----------------------------------------Part a----------------------------------------#
#------------------------- 10% -------------------------------------


# The operand stack: define the operand stack and its operations
opstack = []
# now define functions to push and pop values on the opstack according to your decision about which
# end should be the hot end. Recall that `pass` in python is a no-op: replace it with your code.
def opPop():
	if opstack==[]:
		return opstack
	else:
		return opstack.pop()
	pass

def opPush(value):
	opstack.append(value)

# Remember that there is a Postscript operator called "pop" so we choose different names for these functions.

#-------------------------- 20% -------------------------------------
# The dictionary stack: define the dictionary stack and its operations
dictstack = []
dictmap = []
currentmap = 0
# now define functions to push and pop dictionaries on the dictstack, to define name, and to lookup a name
def dictPop():
	return dictstack.pop()

def dictPush(dictobj):
	#dictobj = opPop()
	if type(dictobj) is not dict:
	#	opPush(dictobj)
		return
	dictstack.append(dictobj)
	pass

def define(name,value):
	if len(dictstack) == 0:
		t = (i,{})
		dictstack.append(t)
	dictstack[-1][name] = value

def lookup(name,style):
	if style == 'dynamic':
		end = len(dictstack)-1
	elif style =='static':
		dic = dictstack[-1]
		if name in dic.keys():
			return (dic[name],len(dictstack)-1)
		end = currentmap
	for i in range(end+1):
		dic = dictstack[end-i]
		if name in dic.keys():
			return (dic[name],end-i)
	return ('cannot find the name',0)

def funpush(num):
	dictPush({})
	dictmap.append(num)
	currentmap = num

def funpop():
	dictPop()
	dictmap.pop()
	currentmap = dictmap[-1]

def getlendictstack():
	return len(dictstack)

	# return the value associated with name
	# what is your design decision about what to do when there is no definition for name
	
#--------------------------- 10% -------------------------------------
# Arithmetic operators: define all the arithmetic operators here -- add, sub, mul, div, mod
#Make sure to check the operand stack has the correct number of parameters and types of the parameters are correct.
def add():
	if len(opstack) < 2:
		print('Error in add: not enough elements in opstack')
		return
	opPush(opPop()+opPop())


def sub():
	if len(opstack) < 2:
		print('Error in add: not enough elements in opstack')
		return
	op2 = opPop()
	op1 = opPop()
	opPush(op1-op2)
	pass

def mul():
	if len(opstack) < 2:
		print('Error in mul: not enough elements in opstack')
		return
	opPush(opPop()*opPop())
	pass

def div():
	if len(opstack) < 2:
		print('Error in div: not enough elements in opstack')
		return
	op2 = opPop()
	op1 = opPop()
	opPush(op1/op2)
	pass

def  mod():
	if len(opstack) < 2:
		print('Error in mod: not enough elements in opstack')
		return
	op2 = opPop()
	op1 = opPop()
	opPush(op1%op2)
	pass

#--------------------------- 15% -------------------------------------
# Array operators: define the array operators length, get

def length():
	array = opPop()
	opPush(len(array))
	pass

def get():
	op2 = opPop()
	op1 = opPop()
	opPush(op1[op2]) 
	pass

#--------------------------- 25% -------------------------------------
# Define the stack manipulation and print operators: dup, exch, pop, roll, copy, clear, stack
def dup():
	opPush(opstack[-1])
	pass

def exch():
	if len(opstack) < 2:
		print('Error in exch: not enough elements in opstack')
		return
	op2 = opPop()
	op1 = opPop()
	opPush(op2)
	opPush(op1)
	pass

def pop():
	return opPop()
	pass
	
def roll():
	op2 = opPop()
	op1 = opPop()
	if ((type(op2) is not int) or (type(op1) is not int)):
		print('Error in roll: parameter should be int')
		opPush(op1)
		opPush(op2)
		return
	if (op1 > len(opstack)) or (op1<0):
		print('Error in roll: out of bound')
		opPush(op1)
		opPush(op2)
		return
	pos = op1-op2
	objs = opstack[-op2:]
	opstack[-op2:] = []
	for ele in objs:
		opstack.insert(-pos,ele)
	pass
		
def copy():
	op1 = opPop()
	op=[]
	if (op1 > len(opstack)):
		print('Error in copy: out of bound')
	if(op1<0):
		print('Error in copy: illegal input!')
	for i in range(op1):
		op.append(opPop())
	for k in range(2):
		for j in range(op1):
			opPush(op[op1-j-1])    

def clear():
	opstack[:] = []

def allclear():
	clear()
	dictstack[:] = []
	dictmap[:] = []
	currentmap = 0

#--------------------------- 20% -------------------------------------
# Define the dictionary manipulation operators: dict, begin, end, psDef
# name the function for the def operator psDef because def is reserved in Python
# Note: The psDef operator will pop the value and name from the stack and call your own "define" 
# operator (pass those values as parameters). Note that psDef()won't have any parameters.

def psDef():
	if len(opstack) < 2:
		print('Error in psDef: not enough elements in opstack')
		return
	value = opPop()
	name = opPop()
	define(name, value)

def stack():
	print('=============')
	for i in range(len(opstack)):
		print(opstack[len(opstack)-1-i])
	print('=============')
	for i in range(getlendictstack()):
		j = getlendictstack()-i-1
		print('------',j,'------',dictmap[j],'------')
		for k in dictstack[j].keys():
			print(k,dictstack[j][k])
	print('=============')

#-------------------------------TEST YOUR CODE---------------------------
# Test the operand stack:
def testOpPop():
	opPush(5)
	if opPop()!=5:
		return False
	return True
	pass

def testOpPush():
	opPush(5)
	if opstack[-1]!=5:
		return False
	return True
	pass

# Test the dictionary stack:
def testDictPop():
	dictPush({})
	count = len(dictstack)
	if count > 0:
		dic = dictstack[-1]
		dictPop()
		if(dic in dictstack) or (len(dictstack) != count-1):
			return False
	return True
	pass
	
def testDictPush():
	dic={}
	opPush(dic)
	dictPush()
	if(dic in opstack) or (dic not in dictstack):
		return False
	return True  
	pass

def testDefine():
	define("x1",4)
	(b,c) = lookup("\nx1",'dynamic')
	if b !=4:
		return False
	return True

def testLookup():
	opPush("\n2")
	opPush(6)
	psDef()
	(b,c) = lookup("\n2",'dynamic')
	if b != 6: 
		return False 
	(b,c) = lookup("\n2",'static')
	if b != 6:
		return False
	return True
	pass

# Test arithmetic operators: 
def testAdd():
	opPush(4)
	opPush(5)
	add()
	if opPop() != 9: 
		return False
	return True
	pass

def testSub():
	opPush(10)
	opPush(2)
	sub()
	if opPop()!=8:
		return False
	return True
	pass

def testMul():
	opPush(3)
	opPush(4)
	mul()
	if opPop()!=12:
		return False
	return True
	pass

def testDiv():
	opPush(4)
	opPush(2)
	div()
	if opPop()!=2:
		return False
	return True
	pass
	
def testMod():
	opPush(1)
	opPush(4)
	mod()
	if opPop()!=1:
		return False
	return True
	pass
	
# Test array operators:
def testLength():
	opPush([1,2,3])
	length()
	if opPop()!=3:
		return False
	return True
	pass

def testGet():
	opPush([1,2,3])
	opPush(2)
	get()
	if opPop()!=3:
		return False
	return True
	pass

# Test the stack manipulation and print operators:
def testDup():
	opPush(5)
	dup()
	if pop()!=5:
		return False
	return True
	pass

def testExch():
	opPush(1)
	opPush(2)
	exch()
	if pop()!=1:
		return False
	if pop()!=2:
		return False
	return True
	pass

def testPop():
	opPush('test')
	if pop()!='test':
		return False
	return True
	pass
   
def testRoll():
	opPush(1)
	opPush(2)
	opPush(3)
	opPush(4)
	opPush(5)
	opPush(3)
	opPush(2)
	roll()
	if opstack[-3] != 4:
		return False
	if opstack[-2] != 5:
		return False
	if opstack[-1] != 3:
		return False
	return True
	pass

def testCopy():
	opPush(2)
	opPush(3)
	opPush(2)
	copy()
	if opstack[3] != 3:
		return False
	if opstack[2] != 2:
		return False
	if opstack[1] != 3:
		return False
	if opstack[0] != 2:
		return False
	return True
	pass

def testClear():
	opPush(1)
	opPush(2)
	opPush(3)
	opPush(4)
	opPush(5)
	opPush(6)
	clear()
	if len(opstack) != 0:
		return False
	return True
	pass

# Test the dictionary manipulation operators    

def testDictz():
	stackcount = len(dictstack)
	dictz()
	if len(dictstack) != stackcount+1:
		return False
	return True
	pass

def testBegin():
	dic = {}
	opPush(dic)
	begin()
	if (dic in opstack) or (dic not in dictstack):
		return False
	return True
	pass

def testEnd():
	dic = {}
	opPush(dic)
	begin()
	count = len(dictstack)
	end()
	if (count-1) != len(dictstack):
		return False
	return True
	pass

def testpPsDef():
	opPush('x2')
	opPush(5)
	psDef()
	(b,c) = lookup("\nx2",'dynamic')
	if b != 5:
		return False
	return True

# go on writing test code for ALL of your code here; think about edge cases, and other points where you are likely to make a mistake.

	
#---------------------------Main Program---------------------------------
def testall_partA():
	testCases = [('copy',testCopy),('opPop',testOpPop),('opPush',testOpPush),('dictPop',testDictPop),
	 ('dictPush',testDictPush),('add', testAdd), ('lookup', testLookup),
	 ('define',testDefine),('lookup',testLookup),('sub',testSub),
	 ('mul',testMul),('div',testDiv),('mod',testMod),('length',testLength),
 	('get',testGet),('dup',testDup),('exch',testExch),('pop',testPop),
 	('roll',testRoll),('clear',testClear),('psDef',testpPsDef)]	 
	failedTests = [testName for (testName, testProc) in testCases if not testProc()]
	if failedTests:
		return ('Some tests failed', failedTests)
	else:
		return ('All tests OK')

#print(testall_partA())

#-----------------------------------------------------Part B----------------------------------------------#
##----------------------------------------1.Convert all the string to a list of tokens----------------------------------------##
import re
###----Convert all teh string to a list of tokens
def tokenize(s):
	return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[[][a-zA-Z0-9_\s!][a-zA-Z0-9_\s!]*[]]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)


##----------------------------------------2.Convert the token list to a code array----------------------------------------##
def groupMatching(it): 
	res = [] 
	for c in it: 
		if c=='}': 
			#res.append(')') 
			return res 
		elif c=='{': 
			res.append(groupMatching(it)) 
		else:
			res.append(c)
	return res

def check(tokens):
	count = 0
	for c in tokens:
		if c=='{':
			count +=1
		elif c=='}':
			count =count-1
			if count <0:
				return False
	return True

##--parse the token input array
def parse(tokens):
	if check(tokens):
		return groupMatching(iter(tokens))
	return False
#print(parse(['stack']))

##----------------------------------------3.Interpret code arrays----------------------------------------##
###---a function dictionary which will be used in the iterpret function
functions = {'add':add,'sub':sub,'mul':mul,'div':div,'mod':mod,'exch':exch,'def':psDef,'roll':roll,'stack':stack,'clear':clear}
###-----translate str to float
def str2float(c):
	try:
		a = float(c)
		return a
	except:
		return c

def interpret(code,style):
	for c in code:
		print(c)
		if isinstance(c,list):
			opPush(c)
		elif c == 'if':
			op2 = pop()
			op1 = pop()
			if isinstance(op2,list) and op1:
				interpret(op2,style)
			else:
				opPush(op1)
				opPush(op2)
		elif c == 'ifelse':
			op3 = pop()
			op2 = pop()
			op1 = pop()
			if isinstance(op3,list) and isinstance(op2,list):
				if op1:
					interpret(op2,style)
				else:
					interpret(op3,style)
			else:
				opPush(op1)
				opPush(op2)
				opPush(op3)
		elif c in functions.keys():
			func = functions[c]
			func()
		else:
			(b,num) = lookup(c,style)
			if b == 'cannot find the name':
				opPush(str2float(c))
			elif isinstance(b,list):
				currentmap = num
				funpush =(num)
				interpret(b,style)
				funpop()
			else:
				opPush(b)


##----------------------------------------4. Interpret the SPS code----------------------------------------##
def interpreter(s,style):
	interpret(parse(tokenize(s)),style)
##----------------------------------------4.1 Testing the parsing----------------------------------------##
##-------------------------------4.2 Testing the full interpreter--------------------------------------##

print(interpreter( 
""" 
/x 4 def
/g { x stack } def
/f { /x 7 def g } def
f
""",'dynamic'))

'''
print(interpreter(
"""
/m [25 50] 1 get def
/n [100 1] 0 get def
/egg1 {/m 25 def n} def
/chic {
/n 1 def
/egg2 { n } def
m n
egg1
egg2
stack } def
n
chic
""",'static'
	))
'''


	
	
	
	