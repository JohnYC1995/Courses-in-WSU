#Name: Yongjun Chen
#ID:11529168
#This code only run on Macbook. I used a .replace() function on the first problem.
def cryptDict(str1,str2):
	#write your code here
	S3={}
	for k in range(0,len(str1)):
			S3[str1[k]]=str2[k]
	return S3
	pass
def decrypt(cdict,s):
	#write your code here
	for char in s:
		if char in cdict:
			s=s.replace(char,cdict[char])        
	return s
	pass

def testDecrypt():
	#write your code here
	cdict = cryptDict('abc','xyz')
	revcdict = cryptDict('xyz','abc')
	tests = "Now I know MY abc's"
	answer = "Now I know MY xyz's"
	if decrypt(cdict,tests)!=answer:
		return False
	if decrypt(revcdict, decrypt(cdict, tests)) != tests:
		return False
	if decrypt(cdict,'')!='':
		return False        
	if decrypt(cryptDict('',''), 'abc')!= 'abc':
		return False            
	return True
	pass
	

testDecrypt()
def charCount(S):
	#write your code here
	dic={}
	for i in S:
		if(i!='0'):
			if i not in dic:
				dic[i]=1
			else:
				dic[i]=dic[i]+1
	del dic[' ']
	dic2=sorted(dic.items(), key=lambda e:(e[1],e[0]))
	return(dic2)
	pass
def testCount():
	#write your code here
	S='Cpts355 --- Assign1'
	result=charCount(S)
	answer=[('1', 1), ('3', 1), ('A', 1), ('C', 1), ('g', 1), ('i', 1), ('n', 1), ('p', 1), ('t', 1), ('5', 2), ('-', 3), ('s', 3)]
	if result != answer:
		return False
	return True
	pass
testCount()
def dictAddup(d):
	#write your code here
	res={}
	for i in d:
		idx=i
		for j in d[i]:
			idx2=j
			if idx2 in res:
				res[idx2]=res[idx2]+d[idx][idx2]
			else:
				res[idx2]=d[idx][idx2]
	return(res)
	pass
def testAddup():
	#write your code here
	d={'Monday':{'355' :2,'451' :1,'360' :2},'Tuesday':{'451' :2,'360' :3},'Thursday':{'355' :3,'451' :2,'360' :3}, 'Friday':{'355' :2},'Sunday':{'355':1,'451':3,'360':1}}
	result=dictAddup(d)
	answer={'355':8,'451':8,'360':9}
	if result!=answer:
		return False      
	return True
	pass  
testAddup()

if __name__ == '__main__':
	passedMsg = "%s passed"
	failedMsg = "%s failed"
	if testDecrypt():
		print( passedMsg % 'testDecrypt')
	else:
		print( failedMsg % 'testDecrypt')
	if testCount():
		print( passedMsg % 'testCount')
	else:
		print( failedMsg % 'testCount')
	if testAddup():
		print( passedMsg % 'testAddup')
	else:
		print( failedMsg % 'testAddup')
		

