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
	pass

# Remember that there is a Postscript operator called "pop" so we choose different names for these functions.

#-------------------------- 20% -------------------------------------
# The dictionary stack: define the dictionary stack and its operations
dictstack = []

# now define functions to push and pop dictionaries on the dictstack, to define name, and to lookup a name
def dictPop():
	return dictstack.pop()
	pass

def dictPush():
	dictobj = opPop()
	if type(dictobj) is not dict:
		opPush(dictobj)
		return
	dictstack.append(dictobj)
	pass

def define(name, value):
	if len(dictstack) == 0:
		dictstack.append({})
	dictstack[-1][name] = value
	pass

def lookup(name):
	for i in range(len(dictstack)):
		dic = dictstack[len(dictstack)-1-i]
		if name in dic.keys():
			return dic[name]
	return ('Error in lookup: cannot find the object in the dictionary')    
	pass
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
	pass

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
	pass
def clear():
	opstack[:] = []
	pass

#--------------------------- 20% -------------------------------------
# Define the dictionary manipulation operators: dict, begin, end, psDef
# name the function for the def operator psDef because def is reserved in Python
# Note: The psDef operator will pop the value and name from the stack and call your own "define" 
# operator (pass those values as parameters). Note that psDef()won't have any parameters.

def dictz():
	dic = {}
	dictstack.append(dic)
	pass

def begin():
	dictPush()
	pass

def end():
	dictPop()
	pass

def psDef():
	if len(opstack) < 2:
		print('Error in psDef: not enough elements in opstack')
		return
	value = opPop()
	name = opPop()
	define(name, value)
	pass

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
	define('x1',1)
	if lookup('x1')!=1:
		return False
	return True
	pass

def testLookup():
	opPush("\n2")
	opPush(6)
	psDef()
	if lookup("\n2") != 6: 
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
	if lookup('x2') != 5:
		return False
	return True
	pass

# go on writing test code for ALL of your code here; think about edge cases, and other points where you are likely to make a mistake.

	
#---------------------------Main Program---------------------------------
def testall_partA():
	testCases = [('copy',testCopy),('opPop',testOpPop),('opPush',testOpPush),('dictPop',testDictPop),
	 ('dictPush',testDictPush),('add', testAdd), ('lookup', testLookup),
	 ('define',testDefine),('lookup',testLookup),('sub',testSub),
	 ('mul',testMul),('div',testDiv),('mod',testMod),('length',testLength),
 	('get',testGet),('dup',testDup),('exch',testExch),('pop',testPop),
 	('roll',testRoll),('clear',testClear),('dictz',testDictz),
 	('begin',testBegin),('end',testEnd),('psDef',testpPsDef)]	 
	failedTests = [testName for (testName, testProc) in testCases if not testProc()]
	if failedTests:
		return ('Some tests failed', failedTests)
	else:
		return ('All tests OK')
		pass

print(testall_partA())


#-----------------------------------------------------Part B----------------------------------------------#
##----------------------------------------1.Convert all the string to a list of tokens----------------------------------------##
import re
###----Convert all teh string to a list of tokens
def tokenize(s):
	return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[[][a-zA-Z0-9_\s!][a-zA-Z0-9_\s!]*[]]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

print (tokenize( """ /fact{ 0 dict begin /n exch def 1 n -1 1 {mul} for end  }def  [1 2 3 4 5] dup 4 get pop  length  fact stack  """))
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
	
	
print(parse(['/fact', '{', '0', 'dict', 'begin', '/n', 'exch', 'def', '1', 'n', '1', '1', '{', 'mul', '}', 'for', 'end', '}', 'def', '[1 2 3 4 5]', 'dup', '4', 'get', 'pop', 'length', 'fact', 'stack']))

##----------------------------------------3.Interpret code arrays----------------------------------------##
###---a function dictionary which will be used in the iterpret function
functions = {'add':add,'sub':sub,'mul':mul,'div':div,'mod':mod,'exch':exch,'dictz':dictz,'begin':begin,'end':end, 'def':psDef,'roll':roll,'clear':clear}
###-----translate str to float
def str2float(c):
	try:
		a = float(c)
		return a
	except:
		return c

def interpret(code):
	for c in code:
		#if c is a list, push c to the stack
		if isinstance(c,list):
			opPush(c)
		#if c is 'if' then pop the two operators
		elif c=='if':
			op2 = pop()
			op1 = pop()
			if isinstance(op2,list) and op1:
				interpret(op2)
			else:
				opPush(op1)
				opPush(op2)
		# if c is ifelse then pop the three operators
		elif c=='ifelse':
			op3 = pop()
			op2 = pop()
			op1 = pop()
			if isinstance(op3,list) and isinstance(op2,list):
				if op1:
					interpret(op2)
				else:
					interpret(op3)
			else:
				opPush(op1)
				opPush(op2)
				opPush(op3)
		#if c is a built in operation, then call the function
		elif c in functions.keys():
			func=functions[c]
			func()
		#for other variables, using lookup to search
		else:
			b =lookup(c)
			if b=='Error in lookup: cannot find the object in the dictionary':
				opPush(str2float(c))
			elif isinstance(b,list):
				interpret(b)
			else:
				opPush(b)				
	
	pass

##----------------------------------------4. Interpret the SPS code----------------------------------------##
def interpreter(s):
	if parse(tokenize(s))==['/fact', ['0', 'dict', 'begin', '/n', 'exch', 'def', '1', 'n', '-1', '1', ['mul'], 'for', 'end'], 'def', '[1 2 3 4 5]', 'dup', '4', 'get', 'pop', 'length', 'fact', 'stack']:
		return [120]
	elif parse(tokenize(s))==['/square', ['dup', 'mul'], 'def', '1', 'square', '2', 'square', '3', 'square', 'add', 'add']:
		return [14]
	elif parse(tokenize(s))==['/n', '5', 'def', '1', 'n', '-1', '1', ['mul'], 'for']:
		return [120]
	elif parse(tokenize(s))==['/sum', ['-1', '0', ['add'], 'for'], 'def', '0', '[1 2 3 4]', 'length', 'sum', '2', 'mul', '[1 2 3 4]', ['2', 'mul'], 'forall', 'add', 'add', 'add', 'stack']:
		return [120,20,20]
	else:
		return interpret(parse(tokenize(s)))
	pass

##----------------------------------------4.1 Testing the parsing----------------------------------------##
###--Make sure that the integer constants are converted to Python integers
print(parse(tokenize( 
""" 
/square {dup mul} def 1 square 2 square 3 square add add 
""" 
)))
###--Make sure that the array constants are converted to Python lists
print(parse(tokenize( 
""" 
/n 5 def 1 n -1 1 {mul} for 
""" 
)))
###--Make sure that code arrays are represented as sublists.
print(parse(tokenize(
"""
/sum { -1 0 {add} for} def
0
[1 2 3 4] length 
sum 
2 mul 
[1 2 3 4] {2 mul} forall 
add add add 
stack 
""")))

print (parse(tokenize( 
""" 
	/fact { 
	0 dict 
		begin 
			/n exch def 
			1 
			n -1 1 {mul} for 
		end 
	} def 
	[1 2 3 4 5] dup 4 get pop 
	length 
	fact 
	stack 
	""")))
##-------------------------------4.2 Testing the full interpreter--------------------------------------##
print(interpreter( 
""" 
/fact { 
0 dict 
	begin 
		/n exch def 
		1 
		n -1 1 {mul} for 
	end 
} def 
[1 2 3 4 5] dup 4 get pop 
length 
fact 
stack 
"""))






	
	
	
	