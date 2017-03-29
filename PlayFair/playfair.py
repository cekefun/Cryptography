import sys

def main(filename):
	openfile = open(filename,"r")
	code = openfile.read()
	print(code)

if __name__ == "__main__":
	main(sys.argv[1])