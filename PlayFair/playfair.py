import sys
import csv
import random
import copy
from math import log10
from itertools import permutations


class Playfair:
	stats = {}
	code = []
	decoded = []
	key = []
	score = 0
	MaxScore = 10000000
	BestResult = []

	def __init__(self,filename):
		openfile = open(filename,"r")
		text = openfile.read()
		self.code = []
		i = 0
	
		while(i<len(text)):
			p = text[i] + text[i+1]
			self.code.append(p.upper())
			i += 2
		self.getStats()


	def crack(self):
		self.generateKey()
		self.decode()
		score = self.score()
		self.MaxScore = score
		self.BestResult = self.key
		trips = 0

		while True:
			print(trips)
			possibles = [self.up(),self.down(),self.left(),self.right(),self.turnRow(),self.turnCol(),self.switchRows(),self.switchCols(),self.swap2(),self.swap2(5), self.swap2(2),self.swap3(),self.sortLast()]
			scores = []
			for matrix in possibles:
				self.key = matrix
				self.decode()
				scores.append(self.score())

			print(self.BestResult)
			print(self.MaxScore)

			choice = 0
			mini = -100000000000000000000000000000000000
			for i in range(len(scores)):
				if scores[i] > mini:
					mini = scores[i]
					choice = i
			if(self.MaxScore >= mini):
				trips += 1
				if(trips == 100):
					break
			else:
				trips = 0
				self.key = possibles[choice]
				self.BestResult = self.key
				self.MaxScore = mini

		print(trips)
		self.key = self.BestResult
		self.decode()
		print(self.key)
		print("".join(self.decoded))



	def correct(self,matrix):
		toCheck = matrix[-1]
		last = 0
		for i in toCheck:
			if last != 0:
				if i < last:
					return False
			last = i
		return True

	def getStats(self):
		reader = csv.reader(open('StatsEN.csv','r'))
		for row in reader:
			bigram, chance = row
			self.stats[bigram] = float(chance)

		#remove J
		toDelete = []
		for p in self.stats:
			if len(p) != 2:
				return False
			if p == "JJ":
				chance = self.stats[p]
				self.stats["II"] += chance
				toDelete.append(p)
				continue
			if p[0] == 'J':
				self.stats['I'+p[1]] += self.stats[p]
				toDelete.append(p)
			if p[1] == 'J':
				self.stats[p[0] + 'I'] += self.stats[p]
				toDelete.append(p)

		for item in toDelete:
			del(self.stats[item])

		#remove doubles
		toDelete = []
		for p in self.stats.keys():
			if len(p) != 2:
					return false
			if p[0] == p[1]:
				chance = self.stats[p]
				self.stats[p[0]+"X"]+= chance + self.stats["X"+p[1]]
				self.stats["X"+p[1]]+= chance + self.stats[p[0]+"X"]
				toDelete.append(p)

		for item in toDelete:
			del(self.stats[item])
		
		for p in self.stats:
			self.stats[p] = log10(self.stats[p])
		'''
		with open('myStats.csv', 'w') as csvfile:
			writer = csv.DictWriter(csvfile,['bigram', 'value'])
			for i in self.stats:
				writer.writerow({'bigram': i, 'value': self.stats[i]})
		'''

	def decode(self):
		self.decoded = []
		for pair in self.code:
			a = (0,0)
			b = (0,0)
			for i in range(5):
				for j in range (5):
					if(pair[0] == self.key[i][j]):
						a = (i,j)
					if(pair[1] == self.key[i][j]):
						b = (i,j)
			result = ""
			if(a[0]!=b[0] and a[1]!= b[1]):
				result = self.key[a[0]][b[1]] + self.key[b[0]][a[1]]
			if(a[0]==b[0]):
				result = self.key[a[0]][a[1]-1] + self.key[b[0]][b[1]-1]
			if(a[1]==b[1]):
				result = self.key[a[0]-1][a[1]] + self.key[b[0]-1][b[1]]
			self.decoded.append(result)

	def generateKey(self):

		possibles = []
		possibles.extend(range(65,74))
		possibles.extend(range(75,91))
		random.shuffle(possibles)

		self.key = []
		for i in range(5):
			self.key.append([])
			for j in range(5):
				self.key[-1].append(chr(possibles[5*i+j]))

	def score(self):
		score = 0
		for i in self.decoded:
			if(i not in self.stats):
				continue
			score += self.stats[i]

		return score

	def up(self):
		#moves the square one row up
		result = []
		for i in range(5):
			result.append(self.key[(i+1)%5])
		return result

	def down(self):
		#moves the square one row down
		result = []
		for i in range(5):
			result.append(self.key[i-1])
		return result

	def left(self):
		#moves the square one column left
		result=[]
		for i in range(5):
			result.append([])
			for j in range(5):
				result[-1].append(self.key[i][(j+1)%5])
		return result

	def right(self):
		#moves the square one column right
		result=[]
		for i in range(5):
			result.append([])
			for j in range(5):
				result[-1].append(self.key[i][j-1])
		return result

	def turnRow(self):
		# reflects a random row
		result = copy.deepcopy(self.key)
		row = random.randint(0,4)
		for i in range(2):
			temp  = result[row][i]
			result[row][i] = result [row][4-i]
			result[row][4-i] = temp
		return result

	def turnCol(self):
		# reflects a random column
		result = copy.deepcopy(self.key)
		col = random.randint(0,4)
		for i in range(2):
			temp  = result[i][col]
			result[i][col] = result [4-i][col]
			result[4-i][col] = temp
		return result

	def switchRows(self):
		#switches 2 random rows
		result = copy.deepcopy(self.key)
		row0 = random.randint(0,4)
		row1 = row0
		while row1==row0:
			row1 = random.randint(0,4)

		temp = result[row0]
		result[row0] = result[row1]
		result[row1] = temp
		return result

	def switchCols(self):
		#switches 2 random columns
		result = copy.deepcopy(self.key)
		col0 = random.randint(0,4)
		col1 = col0
		while col1==col0:
			col1 = random.randint(0,4)
		for i in range(5):
			temp = result[i][col0]
			result[i][col0] = result[i][col1]
			result[i][col1] = temp
		return result

	def swap2(self,amount=1):
		#swaps 2 random places.
		result = copy.deepcopy(self.key)
		for i in range(amount):
			pair1 = [0,0]
			pair1[0] = random.randint(0,4)
			pair1[1] = random.randint(0,4)
			pair2 = pair1.copy()
			while pair2 == pair1:
				pair2[0] = random.randint(0,4)
				pair2[1] = random.randint(0,4)

			temp = result[pair1[0]][pair1[1]]
			result[pair1[0]][pair1[1]] = result[pair2[0]][pair2[1]]
			result[pair2[0]][pair2[1]] = temp
		return result

	def swap3(self):
		result = copy.deepcopy(self.key)
		pair1 = [0,0]
		pair1 = [0,0]
		pair1[0] = random.randint(0,4)
		pair1[1] = random.randint(0,4)
		pair2 = pair1.copy()
		while pair2 == pair1:
			pair2[0] = random.randint(0,4)
			pair2[1] = random.randint(0,4)
		pair3 = pair2.copy()
		while pair3 == pair1 or pair3 == pair2:
			pair3[0] = random.randint(0,4)
			pair3[1] = random.randint(0,4)

		temp = result[pair1[0]][pair1[1]]
		result[pair1[0]][pair1[1]] = result[pair2[0]][pair2[1]]
		result[pair2[0]][pair2[1]] = result[pair3[0]][pair3[1]]
		result[pair3[0]][pair3[1]] = temp
		return result

	def sortLast(self):
		result = copy.deepcopy(self.key)
		result[-1] = sorted(result[-1])
		return result



	

def main(filename):
	PF = Playfair(filename)
	#PF.crack()
	startkey = [['D','I','R','E','C'],['T','O']]
	bestkey = []
	score = -100000000000000000000000
	alfabet = [chr(i) for i in range(65,91)]
	alfabet.remove('J')

	for i in startkey:
		for j in i:
			alfabet.remove(j)
	startkey.append([])
	startkey.append([])
	startkey.append([])

	for comb in permutations(alfabet,4):
		smallAlfa = alfabet[:]
		smallAlfa.remove(comb[0])
		smallAlfa.remove(comb[1])
		smallAlfa.remove(comb[2])
		smallAlfa.remove(comb[3])
		key = copy.deepcopy(startkey)
		key[1].append(comb[0])
		key[1].append(comb[1])
		key[1].append(comb[2])
		key[2].append(comb[3])
		al = 0
		for i in key:
			while len(i) < 5:
				i.append(smallAlfa[al])
				al += 1
		PF.key = key
		sc = PF.score()
		if sc > score:
			print(sc)
			score = sc
			bestkey = key


	print(key)
	PF.key = bestkey
	PF.decode()	
	print("".join(PF.decoded))




if __name__ == "__main__":
	main(sys.argv[1])