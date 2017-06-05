import numpy as np 
import time
import sys
import random
sys.path.append("/Users/Juhn/Documents/gym/gym/envs/toy_text")
from mdp_gridworld import MDPGridworldEnv
from scipy import stats
def Inital(env):
	global Qvalue,Pi,Return,episode
	#Initial Q
	Qvalue = {(s,a):0 for s in range(env.observation_space.n) for a in range(env.action_space.n)}
	#print(Qvalue)
	#Initial Pi
	Pi = {s:[0,1,2,3] for s in range(env.observation_space.n)}
	#print(Pi)
	#Initial Return pair(s,a)
	Return={(s,a):[] for s in range(env.observation_space.n) for a in range(env.action_space.n)}
	#print(Return)
	#episode result
	episode = []
	#print(episode)

#(a)	
def Genarate(env):
	global episode
	starts = env.reset()
	#print(starts)
	terminal = False
	count = 0
	Cstate = starts	
	#print(Cstate)					
	while terminal is False:
		TempPi=random.randint(0,3)
		#print(TempPi)
		count+=1		
		Nstate, reward, terminal, _ =env.step(TempPi)
		episode.append((Cstate,TempPi,reward))
		Cstate=Nstate
	#print("======Generate the episode====")
	#print(episode[1:10])

#(b)&(c)

def First_VisitMC(env):
	
	global Qvalue,Pi,Return,episode,count1
	#print("=====episode=====",episode)
	count1 = 0	
	Flag = True
	while True:
		#(a)
		Genarate(env)
		#(b)		
		temp=set()			
		for i,(s,a,_) in enumerate(episode):
			#print("count",count1)
			#print("i",i)
			if (s,a) not in temp:										
				reward = sum(r*pow(0.9,i2) for i2,(_1,_2,r) in enumerate(episode[i:]))
				#reward = sum(r for i2,(_1,_2,r) in enumerate(episode[i:]))
				#print("reward",reward)
				avgreward=reward/len(episode[i:])
				#print("avgreward",avgreward)
				Return[(s,a)].append(avgreward)		
				Qvalue[(s,a)]=np.mean(Return[(s,a)])
				temp.add((s,a))	
				#print("=======Tuple(s,a)=======")
				#print(temp)
#	print("=====Return======")
#	print(Return)
#	print("======Qvalue======")
#	temptest=sorted(Qvalue.items(), key=lambda e:(e[0]))
#	print(temptest)		
		#(c)
		for s in range(12):
			rmax =-1000
			for a in range(4):
				
				if rmax< Qvalue[(s,a)]:
					rmax = Qvalue[(s,a)]
					#print("s,a,rmax",s,a,rmax)						
					Maxa = a
					
					#print("Maxa",Maxa)
			if Maxa != Pi[s]:
				tempa=random.randint(0,3)
				x = [tempa,Maxa]
				p = (0.01, 0.99)
				dice = stats.rv_discrete(values=(x,p))
				trya=dice.rvs(size=1)
				Pi[s]=trya[0]
				
				#Pi[s]=Maxa
				#print("MaxPi[s]",s,Pi[s])
				Flag =False
			if Maxa == Pi[s]:
				count1 += 1
		if count1 >1000:
			break
	pass
 
def Readable_Policy(env):
	#print("Pi",Pi)

	orientation={0:'North',1:'South',2:'West',3:'East'}
	for i in Pi:
		if i==3 or i==5 or i==7:
			Pi[i]="--"
		else:
			Pi[i]=orientation[Pi[i]]			

	pass
					
			
if __name__ == "__main__":
	env = MDPGridworldEnv()
	print("========Start MC=========")
	Inital(env)
	First_VisitMC(env)
	Readable_Policy(env)
	print("=====Final Policy=====")
	print(Pi)
	#print(Qvalue)