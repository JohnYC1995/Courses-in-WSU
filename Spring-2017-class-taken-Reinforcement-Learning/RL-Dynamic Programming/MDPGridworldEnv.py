import numpy as np 
	import time
	import sys
	sys.path.append("/Users/Juhn/Documents/gym/gym/envs/toy_text")
	from mdp_gridworld import MDPGridworldEnv
	#Uncomment it if to run question 4
	#from mdp_gridworld1 import MDPGridworldEnv

	class My_Mdp:
		def __init__(self, env):
			self.env = env
			# give access to scalar value representing range for the states 12: S 
			self.space_n = env.observation_space.n
			# give access to scalar value representing range for the available actions 4
			self.action_n = env.action_space.n
			# Initial V
			self.Vstate = np.zeros(self.space_n)
			#Initial Policy
			act= [0,1,2,3]
			self.Action = [act for i in range(12)]
			#Count 
			self.count=0
		pass
		
		def Policy_iteration(self, gama = 0.9,theta = 0.1):
			while True:
				#Policy Evaluation
				#print("=======startPolicy_iteration=====")
				while True:
					delta = 0
					count = 1
					for state in range(self.space_n):
						v = self.Vstate[state]
						for action in self.Action[state]:
							Env_inform = self.env.P[state][action]
							V_temp = 0
							Probability_space = len(self.Action[state])
							Probability = 1/Probability_space
							for TransProbability,Next_state,reward,terminal in Env_inform:
								V_temp += Probability * TransProbability * (reward+gama * self.Vstate[Next_state])
								if state == 8:
									count = count+1
								if state == 5:
									V_temp = 0							
						self.Vstate[state] = V_temp
						delta = max(delta,abs(v-self.Vstate[state]))
					if delta<theta:
						break
				#print("possible action:",len(self.Action[8]))
				#print("Vvalue:",self.Vstate[8])
				Policy_stable = True
			    #Policy Improvement
				#print("========startPolicy_Improvement=======")
				for state in range(self.space_n):
					Max_V = 0
					tem_actionlist=[]
					a_action = self.Action[state]
					for action in range(self.action_n):
						Env_inform = self.env.P[state][action]
						V_temp = 0
						for TransProbability,Next_state,reward,terminal in Env_inform:
							V_temp +=  TransProbability*(reward+gama * self.Vstate[Next_state])
							if Max_V < V_temp:
								Max_V = V_temp
								del tem_actionlist[:]
								tem_actionlist.append(action)
							elif V_temp == Max_V:
								tem_actionlist.append(action)
							else:
								pass                   
						self.Action[state] = tem_actionlist           
					if a_action != self.Action[state]:
						Policy_stable = False
				self.count+=1
				if Policy_stable == True:
					break
		pass
		def Value_iteration(self,gama = 0.9,theta = 0.1):
			while True:
				#print("=====Start Value Iterations:",self.count)
				delta = 0			
				for state in range(self.space_n):
					v=self.Vstate[state]
					Max_V = 0
					tem_actionlist=[]
					for action in range(self.action_n):
						Env_inform = self.env.P[state][action]
						V_temp = 0					
						for TransProbability,Next_state,reward,terminal in Env_inform:						
							V_temp += TransProbability * (reward+gama * self.Vstate[Next_state])
							if state == 5:
								V_temp = 0
						if (Max_V < V_temp):
							Max_V = V_temp
							del tem_actionlist[:]
							tem_actionlist.append(action)
						elif (Max_V == V_temp) & (V_temp != 0):
							tem_actionlist.append(action)
						else:
						    pass
					self.Action[state] = tem_actionlist
					if state == 3 or state == 7:
						self.Action[state]=["stop"]
					if state == 5:
						self.Action[state]=["Wall"]
					self.Vstate[state] = Max_V
					#print ("state [{}] = {}".format(state,Max_V)) 
					delta = max(delta,abs(v-self.Vstate[state]))
					time.sleep(.1)
				self.count+=1
				if delta<theta:
					break
				for state in range(self.space_n):
					orientation={0:'North',1:'South',2:'West',3:'East'}
					if state == 3 or state == 7:
						self.Action[state]=["Stop"]
					if state == 5:
						self. Action[state]=["Wall"]
					else:
						self.Action[state]=[orientation[x] if x in orientation else x for x in self.Action[state]]
		pass
		
		def Readable_Policy(self):
			for state in range(self.space_n):
				orientation={0:'North',1:'South',2:'West',3:'East'}
				if state == 3 or state == 7:
					self.Action[state]=["Stop"]
				if state == 5:
					self. Action[state]=["Wall"]
				else:
					self.Action[state]=[orientation[x] if x in orientation else x for x in self.Action[state]]
		pass

	if __name__ == "__main__":
		env = MDPGridworldEnv()
		A = My_Mdp(env)

		A.Policy_iteration()
		A.Readable_Policy()
		print("=======Finish Policy iteration===========")
		print("Converge iteration numbers:",A.count)
		print("=====Policy Iteration Results=====")
		print(A.Vstate[0:4])
		print(A.Vstate[4:8])
		print(A.Vstate[8:12])
		print("=====Optimal Policy=====")
		print(A.Action[0:4])
		print(A.Action[4:8])
		print(A.Action[8:12])

		A.Value_iteration()
		A.Readable_Policy()
		print("=======Finish value iteration===========")
		print("Converge iteration numbers:",A.count)
		print("=====Value Iteration Results======")
		print(A.Vstate[0:4])
		print(A.Vstate[4:8])
		print(A.Vstate[8:12])
		print("=====Optimal Policy=====")
		print(A.Action[0:4])
		print(A.Action[4:8])
		print(A.Action[8:12])
		

		