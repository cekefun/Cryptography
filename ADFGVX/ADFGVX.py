import sys
import math
import time
import operator
import random
from itertools import permutations

class Alphabet:
    '''Class representing useful alphabetical operations.'''
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def letterIndex(l):
        out = Alphabet.alphabet.find(l.upper())
        if out < 0:
            raise ValueError("INVALID CHARACTER: {0}".format(l))
        return out        
        
    def addLetters (l1, l2):
        l1 = Alphabet.letterIndex(l1.upper())
        l2 = Alphabet.letterIndex(l2.upper())
        l3 = (l1 + l2) % 26
        return Alphabet.alphabet[l3]

    def subLetters (l1, l2):
        l1 = Alphabet.letterIndex(l1.upper())
        l2 = Alphabet.letterIndex(l2.upper())
        l3 = (l1 - l2) % 26
        return Alphabet.alphabet[l3]

class Morse:
    '''A class used to decode the relevant subset of morse into text.'''
    # don't need the whole alphabet
    alphabet = {
        '.-'    : 'A',
        '-..'   : 'D',
        '..-.'  : 'F',
        '--.'   : 'G',
        '...-'  : 'V',
        '-..-'  : 'X',    
    }
    
    def decode(code):
        letters = code.split('/')
        text = ''.join([Morse.alphabet[c] for c in letters])
        return text

class Frequency:
    '''A class holding single letter frequencies for the 4 relevant languages, and operations thereon.'''
    # source for frequencies: Wikipedia
    english = {
        'a' : .08167,
        'b' : .01492,
        'c' : .02782,
        'd' : .04253,
        'e' : .12702,
        'f' : .02228,
        'g' : .02015,
        'h' : .06094,
        'i' : .06966,
        'j' : .00153,
        'k' : .00772,
        'l' : .04025,
        'm' : .02406,
        'n' : .06749,
        'o' : .07507,
        'p' : .01929,
        'q' : .00095,
        'r' : .05987,
        's' : .06327,
        't' : .09056,
        'u' : .02758,
        'v' : .00978,
        'w' : .02360,
        'x' : .00150,
        'y' : .01974,
        'z' : .00074
    }
    
    dutch = {
        'a' :  .07486,
        'b' :  .01584,
        'c' :  .01242,
        'd' :  .05933,
        'e' :  .1891,
        'f' :  .00805,
        'g' :  .03403,
        'h' :  .02380,
        'i' :  .06499,
        'j' :  .0146,
        'k' :  .02248,
        'l' :  .03568,
        'm' :  .02213,
        'n' :  .10032,
        'o' :  .06063,
        'p' :  .0157,
        'q' :  .00009,
        'r' :  .06411,
        's' :  .0373,
        't' :  .0679,
        'u' :  .0199,
        'v' :  .0285,
        'w' :  .0152,
        'x' :  .00036,
        'y' :  .00035,
        'z' :  .0139
    }
    
    french = {    
        'a' :  .07636,
        'b' :  .00901,
        'c' :  .03260,
        'd' :  .03669,
        'e' :  .14715,
        'f' :  .01066,
        'g' :  .00866,
        'h' :  .00737,
        'i' :  .07529,
        'j' :  .00613,
        'k' :  .00049,
        'l' :  .05456,
        'm' :  .02968,
        'n' :  .07095,
        'o' :  .05796,
        'p' :  .02521,
        'q' :  .01362,
        'r' :  .06693,
        's' :  .07948,
        't' :  .07244,
        'u' :  .06311,
        'v' :  .01838,
        'w' :  .00074,
        'x' :  .00427,
        'y' :  .00128,
        'z' :  .00326
    }
        
    german = {
        'a' :  .06516,
        'b' :  .01886,
        'c' :  .02732,
        'd' :  .05076,
        'e' :  .16396,
        'f' :  .01656,
        'g' :  .03009,
        'h' :  .04577,
        'i' :  .06550,
        'j' :  .00268,
        'k' :  .01417,
        'l' :  .03437,
        'm' :  .02534,
        'n' :  .09776,
        'o' :  .02594,
        'p' :  .00670,
        'q' :  .00018,
        'r' :  .07003,
        's' :  .07270,
        't' :  .06154,
        'u' :  .04166,
        'v' :  .00846,
        'w' :  .01921,
        'x' :  .00034,
        'y' :  .00039,
        'z' :  .01134
    }
    
    def analyse(text):
        dict = {}
        for t in text:
            try:
                dict[t] += 1
            except:
                dict[t] = 1
                
        for k in dict:
            dict[k] /= len(text)
            
        for k in range(26 - len(dict)):
            dict['_' * (k + 1)] = 0
            
        return dict
        
    def MSE(sfreq1, sfreq2):
        '''Rate the similarity of two frequencies using sum of squared errors.'''
        mse = 0
        
        n = min(len(sfreq1), len(sfreq2))
        for i in range(n):
            mse += (( sfreq1[i][1] - sfreq2[i][1] )** 2)
        return mse
        
    def MSE_all(freq):
        '''Rate the similarities of a frequency compared to the frequencies of all languages.'''
        sfreq = sorted(freq.items(), key=operator.itemgetter(1))
        sfreq.reverse() 
        
        mse = {}            
        for language in Frequency.sorted:
            mse[language] = Frequency.MSE( Frequency.sorted[language], sfreq)        
        return mse     
  
    def sort_frequency(freq):
        '''Turn a frequency dict into list of (letter, frequency) tuples sorted by descending frequency. '''
        out = sorted(freq.items(), key=operator.itemgetter(1))
        out.reverse()
        return out
    
Frequency.all = {
    'english'   : Frequency.english,
    'dutch'     : Frequency.dutch,
    'french'    : Frequency.french,
    'german'    : Frequency.german
}

Frequency.sorted = {c : Frequency.sort_frequency(Frequency.all[c]) for c in Frequency.all}
    
class ADFGVX:
    '''Class storing ADFGVX encryption tools.'''

    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'

    def bundle(text):
        '''
        Turn a string characters int a list of two-character strings
        "abcdef" → ["ab", "cd", "ef"]
        '''
        out = []
        for i in range(0, len(text), 2):
            symbol = text[i:i+2]
            out.append(symbol)
        return out

    def apply_frequency(bundled, language):
        '''
        Substitute the given string of pairs as if it had the exact letter frequency of the given language.
        This method is very naive and very unlikely to give a legible result, even if the input were correct.
        '''
        sbfreq = Frequency.sort_frequency(Frequency.analyse(bundled))
        slfreq = Frequency.sorted[language]

        out = bundled[:]        
        for i in range(len(sbfreq)):
            if i < len(slfreq):
                out = substitute(out, sbfreq[i][0], slfreq[i][0])
            else:
                out = substitute(out, sbfreq[i][0], '?')

        return out


class Column:
    '''Class representing Columnar transposition encryption.'''
    def checkKey(key):
        '''Verify whether or not a certain columnar transposition key is valid.'''
        key = key.upper()
        for i in range(len(key)):
            if key[i+1:].find(key[i]) >= 0:
                raise ValueError('Invalid key: More than one occurrence of ' + key[i])
        return key

    def getColFunc(key):
        '''Uses the given key to generate the column transposition function.'''
        key = Column.checkKey(key)
        sortedKey = ''.join(sorted(key))
        return lambda i : sortedKey.find(key[i])

    def getInvColFunc(key):
        '''Uses the given key to generate the inverse column transposition function.'''
        key = Column.checkKey(key)
        sortedKey = ''.join(sorted(key))
        return lambda i : key.find(sortedKey[i])

    def encypher(text, key):
        colFunc = Column.getColFunc(key)
        m = len(key)
        l = len(text)
        
        matrix = []
        newMatrix = []
        for i in range(m):
            matrix.append([])
            newMatrix.append([])
        
        for i in range(l):
            matrix[i % m].append(text[i])
            
        for i in range(m):
            newMatrix[colFunc(i)] = matrix[i]
            
        s = ''
        for i in range(m):
            for c in newMatrix[i]:
                s += c
        return s
        
    def decypher(text, key):
        colFunc = Column.getColFunc(key)
        invColFunc = Column.getInvColFunc(key)
        m = len(key)     
        l = len(text)
        # h is the minimum elements in each column
        h = int(l/m)
        # indices for the columns that hold an extra value
        extraColumns = [colFunc(i) for i in range(l % m)]
        
        matrix = []
        newMatrix = []
        for i in range(m):
            matrix.append([])                
            newMatrix.append([])
            
        for i in range(m):
            col = text[:h]
            text = text[h:]
            [matrix[i].append(c) for c in col]
            if i in extraColumns:
                matrix[i].append(text[0])
                text = text[1:]
            else:
                matrix[i].append('')
            
        for i in range(m):
            newMatrix[invColFunc(i)] = matrix[i]
            
        s = ''
        for i in range(h + 1):
            for j in range(m):
                s += newMatrix[j][i]
            
        return s
        

        
def draw(dict, barLength = 100, formatString = '{}'):
    '''Draws a simple bar graph.'''
    ymax = 0
    for (x, y) in dict.items():
        ymax = max(ymax, y)
        
    items = sorted(dict.items(), key=operator.itemgetter(1))
    items.reverse()
        
    for (x, y) in items:
        print(x, ':\t', '■' * int(y * barLength / ymax), formatString.format(y))
        
def rate_permutations(code, minLength, maxLength = None, skipChance = 0):
    '''
    A function that gives the results of the above function a rating.
    The rating correlates with the likelihood of the original text being Vigenère encoded human writing.
    '''
    if maxLength is None:
        maxLength = minLength
    startTime = time.time()
    scores = {}            
    for length in range(minLength, maxLength + 1):
        # pick a piece of alphabet
        baseKey = Alphabet.alphabet[:length]
        
        # loading bar stuff
        loadBit = 50/math.factorial(length)
        i = 0
        print('Checking', math.factorial(length), 'permutations of length', str(length) + '...')
        
        # run through all its permutations
        for colKey in permutations(baseKey):
            if(skipChance < random.random()):
                colKey = ''.join(colKey)
                
                decyphered = Column.decypher(code, colKey)
                
                bundled = ADFGVX.bundle(decyphered)
                freq = Frequency.analyse(bundled)
                mse = Frequency.MSE_all(freq)
                
                score = score_from_mse(mse)
                scores[colKey] = score
            
            i += loadBit
            while i >= 1:
                i -= 1
                print('■', end='', flush=True)
        print()        
    print()
            
    scores = sorted(scores.items(), key=operator.itemgetter(1))
    for key, score in scores[:10]:
        print(key, '\trated a score of', score) 
    print()
    print('{0:.1f} seconds elapsed'.format(time.time() - startTime))
       
def substitute(text, fro, to):
    out = text
    for i in range(len(text)):
        if out[i] == fro:
            out[i] = to
    return out
       
def score_from_mse(mse):
    s = 1000
    for l in mse:
        # s += mse[l]
        s = min(s, mse[l])
    return s
    
def print_mse(mse):
    for l, s in sorted(mse.items(), key=operator.itemgetter(1)):
        print('{:<10}:'.format(l), s)
    
    
def main():
    openfile = open('ADFGVX.txt','r')
    code = openfile.read()
    code = Morse.decode(code)
    
    # rate_permutations(code, 6)
    
    # GFDBEAC
    decolumned = Column.decypher(code, 'EABDFGC')
    bundled = ADFGVX.bundle(decolumned)
    
    print('\n\t ENGLISH:')
    print(''.join(ADFGVX.apply_frequency(bundled, 'english')[:200]))
    print('\n\t GERMAN:')
    print(''.join(ADFGVX.apply_frequency(bundled, 'german')[:200]))
    print('\n\t FRENCH:')
    print(''.join(ADFGVX.apply_frequency(bundled, 'french')[:200]))
    print('\n\t DUTCH:')
    print(''.join(ADFGVX.apply_frequency(bundled, 'dutch')[:200]))
    
    
    # mse = Frequency.MSE_all(freq)
    # print_mse(mse)
    # print('total     :', sum_mse(mse))
            
    # print('\n\tOUR THING:')
    # draw(freq, 30, '{:.3f}')
    
    # print('\n\tGERMAN:')
        
    # draw(Frequency.german, 30, '{:.3f}') 
    
    
if __name__ == "__main__":
	main()
