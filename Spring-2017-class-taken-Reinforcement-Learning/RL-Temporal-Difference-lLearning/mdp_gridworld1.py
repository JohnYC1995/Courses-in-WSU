import numpy as np
import sys
from six import StringIO, b

from gym import utils
from gym.envs.toy_text import discrete

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3

MAP = [
	"+----+",
	"|   G|",
	"| | F|",
	"|S   |",
	"+----+"
]

class MDPGridworldEnv(discrete.DiscreteEnv):
	"""
	IMPORTANT: This code is based from openAI gym's FrozenLake code.
	This is a 3x4 grid world based from problem for an AI-Class. (https://goo.gl/GqkyzT)
	The surface is described using a grid like the following
	S : starting point, non-terminal state (reward: -3)
	  : non-terminal states (reward: -3)
	F : fire, burn to death (reward: -100)
	G : goal, an alternate universe where Trump is not the president (reward: +100)
	The episode ends when you reach the goal or burn in hell.
	"""

	metadata = {'render.modes': ['human', 'ansi']}

	def __init__(self, shape=[3,4]):
		self.shape = shape
		self.desc = np.asarray(MAP,dtype='c')

		self.nrow = nR = 3
		self.ncol = nC = 4
		nA = 4
		nS = nR * nC

		isd = np.zeros(nS)


		P = {s : {a : [] for a in range(nA)} for s in range(nS)}

		def to_s(row, col):
			return row*self.ncol + col
		def inc(row, col, a):
			t_row, t_col = row, col
			if a==WEST:
				col = max(col-1,0)
			elif a==SOUTH:
				row = min(row+1,self.nrow-1)
			elif a==EAST:
				col = min(col+1,self.ncol-1)
			elif a==NORTH:
				row = max(row-1,0)
			if self.desc[row+1,col+1] == '|':
				row, col = t_row, t_col
			return (row, col)

		isd[to_s(2, 0)] = 1
		for row in range(self.nrow):
			for col in range(self.ncol):
				s = to_s(row, col)
				for a in range(4):
					li = P[s][a]
					letter = self.desc[row+1, col+1]
					if letter in b'GF':
						li.append((1.0, s, 0, True))
					elif letter == '|':
						li.append((0.0, s, 0, False))
					else:
						rew = -3
						rew1 = -3
						rew2 = -3
						rew3 = -3
						if a == 0:
							a1=2
							a2=3
							a3=1
						if a == 1:
							a1=3
							a2=2
							a3=0
						if a == 2:
							a1=1
							a2=0
							a3=3
						if a == 3:
							a1=0
							a2=1
							a3=2
						
						newrow, newcol = inc(row, col, a)
						newrow1, newcol1 = inc(row, col, a1)
						newrow2, newcol2 = inc(row, col, a2)
						newrow3, newcol3 = inc(row, col, a3)
						
						newstate = to_s(newrow, newcol)
						newstate1 = to_s(newrow1, newcol1)
						newstate2 = to_s(newrow2, newcol2)
						newstate3 = to_s(newrow3, newcol3)
						
						newletter = self.desc[newrow+1, newcol+1]
						newletter1 = self.desc[newrow1+1, newcol1+1]
						newletter2 = self.desc[newcol2+1, newcol2+1]
						newletter3 = self.desc[newcol3+1, newcol3+1]
						
						done = bytes(newletter) in b'GF'
						done1 = bytes(newletter1) in b'GF'
						done2 = bytes(newletter2) in b'GF'
						done3 = bytes(newletter3) in b'GF'
						
						if bytes(newletter) in b'G':
							rew = 100
						if bytes(newletter1) in b'G':
							rew1 = 100
						if bytes(newletter2) in b'G':
							rew2 = 100
						if bytes(newletter3) in b'G':
							rew3 = 100
						if bytes(newletter) in b'F':
							rew = -100
						if bytes(newletter1) in b'F':
							rew1 = -100
						if bytes(newletter2) in b'F':
							rew2 = -100
						elif bytes(newletter3) in b'F':
							rew3 = -100
						
						li.append((0.9, newstate, rew, done))
						li.append((0.05, newstate1, rew1, done1))
						li.append((0.05, newstate2, rew2, done2))
						li.append((0, newstate3, rew3, done3))
						
						

		isd /= isd.sum()
		super(MDPGridworldEnv, self).__init__(nS, nA, P, isd)

	def _render(self, mode='human', close=False):
		if close:
			return

		outfile = StringIO() if mode == 'ansi' else sys.stdout

		row, col = (self.s // self.ncol)+1, (self.s % self.ncol)+1
		desc = self.desc.tolist()
		desc = [[c.decode('utf-8') for c in line] for line in desc]
		desc[row][col] = utils.colorize(desc[row][col], "red", highlight=True)
		outfile.write("\n".join(''.join(line) for line in desc)+"\n")
		if self.lastaction is not None:
			outfile.write("  ({})\n".format(["North","South","West","East"][self.lastaction]))
		else:
			outfile.write("\n")

		return outfile

