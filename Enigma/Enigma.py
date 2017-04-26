from collections import defaultdict
from itertools import permutations

class Enigma:
	Rotor = {}
	Reflector = {}
	code = ""
	crib=""
	rotors = []
	state = {}
	alfabet = [chr(i) for i in range(65,91)]


	def loadRotor(self,filename):
		self.Rotor[filename] = {}
		openfile = open(filename,"r")
		text = openfile.read()
		for i in range(len(text)-1):
			self.Rotor[filename][text[i]] = text[i+1]
		self.Rotor[filename][text[-1]]= text[0]

	def loadReflector(self,filename):
		openfile = open(filename,"r")
		text = openfile.read()
		i = 0
		while(i<len(text)):
			self.Reflector[text[i]] = text[i+1]
			self.Reflector[text[i+1]]=text[i]
			i += 2

	def loadCode(self,filename):
		openfile = open(filename,"r")
		self.code = openfile.read()

	def loadCrypt(self,filename):
		openfile = open(filename,"r")
		self.crib = openfile.read()

	def setRotors(self,r0,r1,r2):
		self.rotors = []
		self.rotors.append(r0)
		self.rotors.append(r1)
		self.rotors.append(r2)

	def setState(self,s0,s1,s2):
		self.state = {}
		self.state[self.rotors[0]] = ord(s0) - ord('A')
		self.state[self.rotors[1]] = ord(s1) - ord('A')
		self.state[self.rotors[2]] = ord(s2) - ord('A')

	def turn(self):
		if(self.alfabet[self.state[self.rotors[0]]] == self.alfabet[-1]):
			if(self.alfabet[self.state[self.rotors[1]]] == self.alfabet[-1]):
				self.state[self.rotors[2]] = (self.state[self.rotors[2]]+1)%len(self.alfabet)
			self.state[self.rotors[1]] = (self.state[self.rotors[1]]+1)%len(self.alfabet)
		self.state[self.rotors[0]] = (self.state[self.rotors[0]]+1)%len(self.alfabet)

	def decode(self,c):
		toDecode = c
		for i in self.rotors:
			toDecode =ord(toDecode) + self.state[i]
			if toDecode > ord('Z'):
				toDecode -= 25				
			toDecode = chr(toDecode)
			toDecode = self.Rotor[i][toDecode]
		toDecode = self.Reflector[toDecode]
		for i in reversed(self.rotors):
			revMap = {v: k for k,v in self.Rotor[i].items()}
			toDecode = ord(toDecode) + self.state[i]
			if toDecode > ord('Z'):
				toDecode -= 25
			toDecode = chr(toDecode)
			toDecode = revMap[toDecode]
		self.turn()
		return toDecode


class Bombe:
	def __init__(self,Enigma):
		self.e = Enigma
		self.graph = defaultdict(list)
		self.cycles = defaultdict(list)
		self.possibles = []
	def makeGraph(self):
		crib = self.e.crib
		check = self.e.code[:len(crib)]
		for i in range(len(crib)):
			self.graph[crib[i]].append((check[i],i))
			self.graph[check[i]].append((crib[i],i))

	def crack(self):
		for i in self.e.alfabet:
			for j in self.e.alfabet:
				for k in self.e.alfabet:
					for perm in permutations(self.e.Rotor.keys(),3):
						success = True
						for key,value in self.cycles.items():
							if(not success):
								break
							for loop in value:
								for bar in self.e.alfabet:
									ch = bar
									for path in loop:
										self.e.setRotors(perm[0],perm[1],perm[2])
										self.e.setState(i,j,k)
										for foo in range(path):
											self.e.turn()
										ch = self.e.decode(ch)
									if(ch == bar):
										success = True
										break
								if(not success):
									break
						if(success):
							self.possibles.append([[i,j,k],perm])







def main():
	e = Enigma()
	e.loadRotor("r0.txt")
	e.loadRotor("r1.txt")
	e.loadRotor("r2.txt")
	e.loadRotor("r3.txt")
	e.loadRotor("r4.txt")
	e.loadReflector("ref.txt")
	e.loadCode("Code.txt")
	e.loadCrypt("Crib.txt")
	e.setRotors("r0.txt","r1.txt","r2.txt")
	e.setState('B','A','A')
	e.decode('A')
	b = Bombe(e)
	b.makeGraph()
	print (b.graph)

	#made on paper
	b.cycles['V'].append([5,8,15,10,21,19,14])
	b.cycles['V'].append([12,4,17,1])
	b.cycles['E'].append([2,7])
	b.cycles['B'].append([11,23])

	b.crack()
	#print (b.possibles)




if __name__ == "__main__":
	main()