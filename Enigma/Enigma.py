class Enigma:
	Rotor = {}
	Reflector = {}
	code = ""
	crib=""


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

	def loadCrypt(self,filname):
		openfile = open(filename,"r")
		self.crib = openfile.read()		



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
	print(e.Rotor["r0.txt"])
	print(e.Reflector)


if __name__ == "__main__":
	main()