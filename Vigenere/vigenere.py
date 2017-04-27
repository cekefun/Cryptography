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

    def addLetters(l1, l2):
        l1 = Alphabet.letterIndex(l1.upper())
        l2 = Alphabet.letterIndex(l2.upper())
        l3 = (l1 + l2) % 26
        return Alphabet.alphabet[l3]

    def subLetters(l1, l2):
        l1 = Alphabet.letterIndex(l1.upper())
        l2 = Alphabet.letterIndex(l2.upper())
        l3 = (l1 - l2) % 26
        return Alphabet.alphabet[l3]


class Vigenere:
    '''Class representing regular Vigenère encryption.'''
    def encypher(text, key):
        l = len(key)
        i = 0
        out = ''
        for c in text:
            out += Alphabet.addLetters(c, key[i % l])
            i += 1
        return out

    def decypher(text, key):
        l = len(key)
        i = 0
        out = ''
        for c in text:
            out += Alphabet.subLetters(c, key[i % l])
            i += 1
        return out


class Column:
    '''Class representing Columnar transposition encryption.'''

    def checkKey(key):
        '''Verify whether or not a certain columnar transposition key is valid.'''
        key = key.upper()
        for i in range(len(key)):
            if key[i + 1:].find(key[i]) >= 0:
                raise ValueError(
                    'Invalid key: More than one occurrence of ' + key[i])
        return key

    def getColFunc(key):
        '''Uses the given key to generate the column transposition function.'''
        key = Column.checkKey(key)
        sortedKey = ''.join(sorted(key))
        return lambda i: sortedKey.find(key[i])

    def getInvColFunc(key):
        '''Uses the given key to generate the inverse of the column transposition function.'''
        key = Column.checkKey(key)
        sortedKey = ''.join(sorted(key))
        return lambda i: key.find(sortedKey[i])

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
        h = int(l / m)
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


def find_distances(text):
    '''
    Given a piece of text, returns a dict of tuples (distance, count)
    where `distance` is the distance between some pair of identical strings of 3 characters in the text,
    and `count` the number of times that this distance was encountered.
    '''
    searched = []
    distances = {}
    for i in range(len(text) - 2):
        str = text[i:i + 3]
        if str not in searched:
            searched.append(str)
            j = i + 3
            while True:
                dist = text[j:].find(str)
                if dist < 0:
                    break
                try:
                    distances[dist + 3] += 1
                except:
                    distances[dist + 3] = 1
                j = j + dist + 3

    return distances


def factors_up_to(number, limit):
    '''
    Finds all factors smaller than `limit` for the given `number`.
    '''
    for i in range(2, limit):
        if number % i == 0:
            yield i


def factorise_distances(distances, limit=30):
    '''Returns a dictionary representing how often distances with certain factors under `limit` occurred.'''
    factors = {}
    for (dist, count) in distances.items():
        for i in factors_up_to(dist, limit):
            try:
                factors[i] += count
            except:
                factors[i] = count

    return factors


def rate_factors(factors):
    '''
    A function that gives the results of the above function a rating.
    The rating correlates with the likelihood of the original text being Vigenère encoded human writing.
    '''
    s = 0
    for (f, count) in factors.items():
        s += count * f
        # s = max(s, count * f)
    return s


def draw(dict, barLength=100):
    '''Draws a simple bar graph.'''
    ymax = 0
    for (x, y) in dict.items():
        ymax = max(ymax, y)

    for (x, y) in sorted(dict.items()):
        print(x, ':\t', '■' * int(y * barLength / ymax) + ' ' + str(y))


def rate_permutations(code, minLength, maxLength=None, skipChance=0):
    '''
    Tries all possible columnar keys of length in [minLength, maxLength].
    For each key it tries to decypher the text, it then applies analysis to give the decyphered text a rating.
    Each key gets rated in this way, and the highest rated keys are printed to the terminal.
    skipChance gives a way to speed this up (at the cost of some accuracy) by giving the system a chance to skip each key.
    '''
    if maxLength is None:
        maxLength = minLength
    startTime = time.time()
    scores = {}
    for length in range(minLength, maxLength + 1):
        # pick a piece of alphabet
        baseKey = Alphabet.alphabet[:length]

        # loading bar stuff
        loadBit = 50 / math.factorial(length)
        i = 0
        print('Checking', math.factorial(length),
              'permutations of length', str(length) + '...')

        # run through all its permutations
        for colKey in permutations(baseKey):
            if(skipChance < random.random()):
                colKey = ''.join(colKey)
                decyphered = Column.decypher(code, colKey)
                distances = find_distances(decyphered)
                factors = factorise_distances(distances)
                score = rate_factors(factors)
                scores[colKey] = score

            i += loadBit
            while i >= 1:
                i -= 1
                print('■', end='', flush=True)
        print()
    print()

    scores = sorted(scores.items(), key=operator.itemgetter(1))
    scores.reverse()
    for key, score in scores[:10]:
        print(key, '\trated a score of', score)
    print()
    print('{0:.1f} seconds elapsed'.format(time.time() - startTime))


def main():
    openfile = open('Vigenereplus.txt', 'r')
    code = openfile.read()

    # amount of characters to print
    charCount = 100

    print('Encyphered mystery:')
    print(code[:charCount] + '...\n')

    distances = find_distances(code)
    factors = factorise_distances(distances)
    print('The factors of distances between repeated occurrences of three letters in a row:')
    draw(factors, 50)
    print('I rate these factors a', rate_factors(factors), ', which is very bad.\n')

    print('Decyphering Column transposition with key "GBDAFCE".')
    decolumned = Column.decypher(code, 'GBDAFCE')
    print(decolumned[:charCount] + '...\n')

    distances = find_distances(decolumned)
    factors = factorise_distances(distances)
    print('The factors of distances between repeated occurrences of three letters in a row:')
    draw(factors, 50)
    print('I rate these factors a', rate_factors(factors), ', which is very good.\n')

    print('(At this point: Use the Vigenère Cracking Tool to find the key)')

    print('Decyphering Vigenère with key "SASKIADECOSTER":')
    decyphered = Vigenere.decypher(decolumned, 'SaskiadeCoster')
    print(decyphered[:charCount] + '...\n')


if __name__ == "__main__":
    main()
