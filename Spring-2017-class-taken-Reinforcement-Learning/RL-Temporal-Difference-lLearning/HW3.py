import numpy as np 
import time
import sys
import random
sys.path.append("/Users/Juhn/Documents/gym/gym/envs/toy_text")
from mdp_gridworld import MDPGridworldEnv

def e_policy(Max,e):
	ran = random.uniform(0,1)
	a = random.randint(0,3)
	if ran > 1-e:
		output = a
	else:
		output = Max
	return output
	pass
def optimal_action(state,Q):
	Q_s_max = Q[(state,0)]
	a = 0
	tempQ = 0
	for i in range(4):
		tempQ = Q[(state,i)]
		if tempQ > Q_s_max:
			Q_s_max = tempQ
			a = i
	return a
	pass
def Q_Learning(env,alpha,gama,epsilon,countall):
	count = 0
	iteration = 0
	Q = {(s,a):0 for s in range(env.observation_space.n) for a in range(env.action_space.n)}	
	Pi = {s:[0,1,2,3] for s in range(env.observation_space.n)}
	while True:
		Converge = True
		s=env.reset()
		terminal = False
		while True:		
			a = optimal_action(s,Q)
			#e-greedy:
			a = e_policy(a,epsilon)
			if Pi[s] != a:
				Converge = False
			Pi[s] = a
			s1, reward, terminal, _ = env.step(a)			
			a1 = optimal_action(s1,Q)
			# Updata Q value
			Q[(s,a)] = Q[(s,a)] + alpha * (reward + gama*Q[(s1,a1)]-Q[(s,a)])
			s=s1
			if terminal is True:
				break
		if Converge == True:
			count = count + 1
		else:
			count = 0
		iteration += 1
		if count > countall:
			break
	return Pi, iteration
	pass
def Q_lamda_Learning(env,lamda,alpha,gama,epsido,countall):
	count = 0
	iteration = 0
	Q = {(s,a):0 for s in range(env.observation_space.n) for a in range(env.action_space.n)}
	#e = {(s,a):0 for s in range(env.observation_space.n) for a in range(env.action_space.n)}
	Pi = {s:[0,1,2,3] for s in range(env.observation_space.n)}
	while True:
		e = {(s,a):0 for s in range(env.observation_space.n) for a in range(env.action_space.n)}
		Converge = True
		s=env.reset()
		a = 0
		terminal = False
		Pi[s] = a
		while True:
			s1, reward, terminal, _ = env.step(a)
			a_optm = optimal_action(s1,Q)
			#e-greedy policy
			a1 = e_policy(a_optm,0.05)
			if Pi[s1] != a1:
				Converge = False
			Pi[s1] = a1
			delta = reward + gama * Q[(s1,a_optm)] - Q[(s,a)]
			e[(s,a)] = e[(s,a)] + 1
			for i in range(12):
				for j in range(4):
					Q[(s,a)] = Q[(s,a)] + alpha*delta*e[(s,a)]
					if a1 == a_optm:
						e[(s,a)] = gama * lamda *e[(s,a)]
					else:
						e[(s,a)] = 0
			s = s1
			a=a1 
			if terminal is True:
				break
		if Converge == True:
			count = count + 1
		else:
			count = 0
		iteration += 1
		if count > countall:
			break
	return Pi, iteration
	pass

def Readable_Policy(Pi):
	orientation={0:'^',1:'v',2:'<',3:'>'}
	output=[]
	for i in Pi:
		if i==3 or i==5 or i==7:
			Pi[i]="--"	
		else:
			Pi[i]=orientation[Pi[i]]
		output.append(Pi[i])				
	return output
	pass
def Test_Q_Learning():
	env = MDPGridworldEnv()
	print("=========Q-learning=========")
	total = 0
	for i in range(50):
		Pi,iterations=Q_Learning(env,0.1,0.9,0.05,20)
		total = total +iterations
		i+=1

	average = total/50
	Pi=Readable_Policy(Pi)
	print("average iterations:",average)
	print("=====Finial Policy====")
	print(Pi[0:4])
	print(Pi[4:8])
	print(Pi[8:12])
	pass
def Test_Q_lamda_Learning():
	env = MDPGridworldEnv()
	print("======Q(lamda)learning======")
	#Pi,iterations=Q_lamda_Learning(env,0.1,0.1,0.9,0.2,10)
	total = 0
	for i in range(50):
		Pi,iterations=Q_lamda_Learning(env,0.6,0.1,0.9,0.05,20)
		total = total +iterations
		i+=1
	average = total/50
	Pi=Readable_Policy(Pi)
	print("average iterations:",average)
	print("=====Finial Policy====")
	print(Pi[0:4])
	print(Pi[4:8])
	print(Pi[8:12])
	pass
if __name__ == "__main__":
	Test_Q_Learning()
	Test_Q_lamda_Learning()
