import sys

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def letterIndex(l):
    out = alphabet.find(l.upper())
    if out < 0:
        raise ValueError("INVALID CHARACTER: {0}".format(l))
    return out

def addLetters (l1, l2):
    l1 = letterIndex(l1)
    l2 = letterIndex(l2)
    l3 = (l1 + l2) % 26
    return alphabet[l3]

def subLetters (l1, l2):
    l1 = letterIndex(l1)
    l2 = letterIndex(l2)
    l3 = (l1 - l2) % 26
    return alphabet[l3]
    
def encypher(text, key):
    l = len(key)
    i = 0
    out = ''
    for c in text:
        out += addLetters(c, key[i % l])
        i += 1
    return out
    
def decypher(text, key):
    l = len(key)
    i = 0
    out = ''
    for c in text:
        out += subLetters(c, key[i % l])
        i += 1
    return out
    

def main():
	openfile = open('Vigenereplus.txt','r')
	code = openfile.read()
	print(code)

if __name__ == "__main__":
	main()
















