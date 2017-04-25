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
		self.rotors.append(r0)
		self.rotors.append(r1)
		self.rotors.append(r2)

	def setState(self,s0,s1,s2):
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


if __name__ == "__main__":
	main()