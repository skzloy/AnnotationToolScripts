# -*- coding: cp1251 -*-
from collections import Counter
from TrieNode import *
from LeviOnTries import *
import math
import time

class EspersanCharacteristic:
    def __init__(self, block):
        self.block = block
        self.ESP6 = ESP6(block)
        self.ESP5 = ESP5(self.ESP6)
        self.ESP3 = ESP3(self.ESP6)

class CharToESP6Groupd:
    @staticmethod
    def transform(letter):
        letter = letter.lower()
        result = '0'
        if(letter in 'птк'):
            result = '1'
        elif(letter in 'сшфцхщ'):
            result = '2'
        elif(letter in 'бдг'):
            result = '3'
        elif(letter in 'взж'):
            result = '4'
        elif(letter in 'мн'):
            result = '5'
        elif(letter in 'лрй'):
            result = '6'
        return result
            

class ESP6:
    def __init__(self, text):
        c = Counter(text.lower())
        self.E1 = c['п'] + c['т'] + c['к']
        self.E2 = c['с'] + c['ш'] + c['ф'] + c['ц'] + c['х']+c['щ']
        self.E3 = c['б'] + c['д'] + c['г']
        self.E4 = c['в'] + c['з'] + c['ж']
        self.E5 = c['м'] + c['н']
        self.E6 = c['л'] + c['р'] + c['й']

class ESP5:
    def __init__(self, esp6):
        self.E1 = esp6.E1
        self.E2 = esp6.E2
        self.E3 = esp6.E3 + esp6.E4
        self.E4 = esp6.E5
        self.E5 = esp6.E6

class ESP3:
    def __init__(self, esp6):
        self.E1 = esp6.E1 + esp6.E2
        self.E2 = esp6.E3 + esp6.E4
        self.E3 = esp6.E5 + esp6.E6
        self.InitESP3Groups()
        self.EP1, self.EP2, self.EP3 = self.GetESPIndices(self.E1, self.E2, self.E3)
        self.GroupID = self.GetESP3Group(str(self.EP1) + str(self.EP2) + str(self.EP3))

    def InitESP3Groups(self):
        self.groupMaps = {}
        self.groupMaps['112'] = 'a'
        self.groupMaps['121'] = 'b'
        self.groupMaps['122'] = 'c'
        self.groupMaps['123'] = 'd'
        self.groupMaps['132'] = 'e'

        self.groupMaps['222'] = 'f'
        self.groupMaps['212'] = 'g'
        self.groupMaps['213'] = 'h'
        self.groupMaps['221'] = 'i'
        self.groupMaps['223'] = 'q'
        self.groupMaps['231'] = 'j'
        self.groupMaps['232'] = 'k'

        self.groupMaps['312'] = 'l'
        self.groupMaps['321'] = 'm'
        self.groupMaps['322'] = 'n'
        self.groupMaps['312'] = 'o'
        self.groupMaps['332'] = 'p'
        

    def GetESPIndices(self, e1, e2, e3):
        ep1 = ep2 = ep3 = 0
        if(e1 == e2):
            ep1 = ep2 = 2
            if(e1 == e3):
                ep3 = 2
            elif e1 < e3:
                ep3 = 1
            else:
                ep3 = 3

        elif(e1 == e3):
            ep1 = ep3 = 2
            if(e1 == e2):
                ep2 = 2
            elif e1 < e2:
                ep2 = 1
            else:
                ep2 = 3

        elif(e2 == e3):
            ep2 = ep3 = 2
            if(e2 == e1):
                ep1 = 2
            elif e2 < e1:
                ep1 = 1
            else:
                ep1 = 3
            
        else:
            if(e1 < e2):
                if(e2 < e3):
                    ep1 = 3
                    ep2 = 2
                    ep3 = 1
                elif(e1 < e3):
                    ep1 = 3
                    ep2 = 1
                    ep3 = 2
                else:
                    ep1 = 2
                    ep2 = 1
                    ep3 = 3
              
            else:
              if(e2 > e3):
                ep1 = 1
                ep2 = 2
                ep3 = 3
              elif(e1 < e3):
                ep1 = 2
                ep2 = 3
                ep3 = 1
              else:
                ep1 = 1
                ep2 = 3
                ep3 = 2
              
        return ep1, ep2, ep3

    def GetESP3Group(self, esp3p):
        return self.groupMaps[esp3p]

import re
from Levenshtein import *
from itertools import permutations
from sets import Set
class MatchesFinder:
    @staticmethod
    def FindMatchesSubstring(st, minSize, maxSize):
        originalString = st
        matches = {}
        res = []
        #clear matches
        for j in range(minSize,maxSize):
            for i in range(0, len(originalString)):
                if(len(originalString) - i < j):
                    break

                substringToSearch = originalString[i:i+j]
                
                if (substringToSearch in originalString) and (substringToSearch not in matches):
                    matchCount = 0
                    startBlockID = [m.start()+1 for m in re.finditer(substringToSearch, originalString)]
                    matchCount = len(startBlockID)
                    if(matchCount > 1) and (len(substringToSearch)>1):
                        ms = MatchingSubstring(substringToSearch)
                        ms.AddMatch(substringToSearch, set(startBlockID))
                        matches[substringToSearch] = ms
                        

        #replacements with permutations
        usedSubstrings = set()
        usedIndices = []
        for j in range(maxSize,minSize,-1):
            for i in range(0, len(originalString)-j):

                if i in usedIndices:
                    continue
                
                substringToSearch = originalString[i:i+j]
                #print "subs len %d startPosition %d len %d" % (j, i, len(originalString))
                if substringToSearch in usedSubstrings:
                    continue

                usedSubstrings.add(substringToSearch)
                stringToSearchIn = originalString[i+j:]
                
                allSubstrings = SubstringGenerator.generate(stringToSearchIn, j - 2, j + 2, usedIndices)
                
                possiblePermutations = PermutationGenerator.generate(substringToSearch)
                matchCount = 0

                for string in allSubstrings:
                    if string in substringToSearch:
                            continue
                    for permutedString in possiblePermutations:
                        
                        if (1.0*levenshtein(permutedString, string))/(len(substringToSearch)) <= 0.3:
                            usedIndices += range(i,i+j)
                            if(substringToSearch not in matches):
                                startBlockID = [m.start()+1 for m in re.finditer(string, originalString)]
                                startBlockID += [m.start()+1 for m in re.finditer(substringToSearch, originalString)]
                                ms = MatchingSubstring(substringToSearch)
                                ms.AddMatch(string, set(startBlockID))
                                matches[substringToSearch] = ms
                            else:
                                ms = matches[substringToSearch]
                                startBlockID = [m.start()+1 for m in re.finditer(string, originalString)]
                                ms.AddMatch(string, set(startBlockID))
                            break
                     
                
        #permutations
##        for j in range(2,5):
##            for i in range(0, len(originalString)-j):
##                substringToSearch = originalString[i:i+j]
##                possiblePermutations = PermutationGenerator.generate(substringToSearch)
##                for permut in possiblePermutations:
##                    stringToSearchIn = originalString[i+j:len(originalString)]
##                    if (permut in stringToSearchIn) and (permut != substringToSearch):
##                        if(substringToSearch not in matches):
##                            startBlockID = [m.start()+1 for m in re.finditer(permut, stringToSearchIn)]
##                            startBlockID += [m.start()+1 for m in re.finditer(substringToSearch, stringToSearchIn)]
##                            ms = MatchingSubstring(substringToSearch)
##                            ms.AddMatch(permut, set(startBlockID))
##                            matches[string] = ms
##                        else:
##                            ms = matches[substringToSearch]
##                            
##                            startBlockID = [m.start()+1 for m in re.finditer(permut, stringToSearchIn)]
##                            ms.AddMatch(permut, set(startBlockID))
##
                            
        for match in matches.values():
            res.append(match)
        return res

    @staticmethod
    def is_visited(i, j, k, visited):
        m = visited.get((i,j),-1)
        if k>m:
            visited[(i,j)] = k
            return False
        return True

    @staticmethod
    def fuzzy_compare(S1, S2, k, i = 0, j = 0, visited = None):
        N1 = len(S1)
        N2 = len(S2)
        if visited is None:
            visited = {}
        while True:
            if N1-i<=k and N2-j<=k:
                return True
            try:
                if S1[i] == S2[j]:
                    visited[(i,j)] = k
                    i+=1
                    j+=1
                    continue
            except IndexError:
                return False
            if k == 0:
                return False
            else:
                if not MatchesFinder.is_visited(i+1, j, k-1, visited):
                    if MatchesFinder.fuzzy_compare(S1, S2, k-1, i+1, j, visited):
                        return True
                if not MatchesFinder.is_visited(i, j+1, k-1, visited):
                    if MatchesFinder.fuzzy_compare(S1, S2, k-1, i, j+1, visited):
                        return True
                if not MatchesFinder.is_visited(i+1, j+1, k-1, visited):
                    if MatchesFinder.fuzzy_compare(S1, S2, k-1, i+1, j+1, visited):
                        return True
                return False

    @staticmethod
    def FindMatchesSubstringOfSonorStringOnTries(st, minSize, maxSize):
        originalString = st
        matches = {}
        res = []
        filteredOriginalString = originalString.replace('0','')
        # clear matches
        for j in range(minSize,maxSize):
            for i in range(0, len(originalString)):
                if(len(originalString) - i < j):
                    break

                substringToSearch = originalString[i:i+j]
                ss = substringToSearch.replace('0','')

                if (ss in filteredOriginalString) and (substringToSearch not in matches):
                    matchCount = 0
                    startBlockID = [m.start()+1 for m in re.finditer(substringToSearch, originalString)]
                    matchCount = len(startBlockID)
                    if(matchCount > 1) and (len(substringToSearch)>1):
                        ms = MatchingSubstring(substringToSearch)
                        ms.AddMatch(substringToSearch, set(startBlockID))
                        matches[substringToSearch] = ms


        #replacements with permutations
        usedSubstrings = set()
        usedIndices = []
        
        for j in range(minSize,maxSize):

            print time.asctime( time.localtime(time.time()) )
            print "%s of %s" % (j - minSize, maxSize - minSize )

            allSubstrings = SubstringGenerator.generate(originalString, j - 2, j + 2, usedIndices)

            trie = TrieNode()
            for word in allSubstrings:
                trie.insert( word )

            for i in range(0, len(originalString)-j):

                # if i in usedIndices:
                #     continue
                
                substringToSearch = originalString[i:i+j]
                results = LeviOnTries.search( trie, substringToSearch, math.floor(len(substringToSearch) * 0.3) )
                # ss = substringToSearch.replace('0','')
                #
                # if len(ss) == 0:
                #     continue
                #print "subs len %d startPosition %d len %d" % (j, i, len(originalString))
                # if substringToSearch in usedSubstrings:
                #     continues
                #
                # usedSubstrings.add(substringToSearch)
                stringToSearchIn = originalString[i+j:]
                # allSubstrings = SubstringGenerator.generate(stringToSearchIn, j - 2, j + 2, usedIndices)
                

                # possiblePermutations = PermutationGenerator.CustomPermutations(ss)
                matchCount = 0

                for r in results:
                    string = r[0]
                    # stringToSearch = string.replace('0','')

                    if(substringToSearch not in matches):
                        startBlockID = [m.start() for m in re.finditer(string, originalString)]
                        startBlockID += [m.start() for m in re.finditer(substringToSearch, originalString)]
                        ms = MatchingSubstring(substringToSearch)
                        ms.AddMatch(string, set(startBlockID))
                        matches[substringToSearch] = ms
                    else:
                        ms = matches[substringToSearch]
                        startBlockID = [m.start() for m in re.finditer(string, originalString)]
                        ms.AddMatch(string, set(startBlockID))
                    break

        for match in matches.values():
            res.append(match)
        return res

    @staticmethod
    def FindMatchesSubstringOfSonorString(st, minSize, maxSize):
        originalString = st
        matches = {}
        res = []
        filteredOriginalString = originalString.replace('0','')
        #clear matches
        for j in range(minSize,maxSize):
            for i in range(0, len(originalString)):
                if(len(originalString) - i < j):
                    break

                substringToSearch = originalString[i:i+j]
                ss = substringToSearch.replace('0','')

                if (ss in filteredOriginalString) and (substringToSearch not in matches):
                    startBlockID = [m.start()+1 for m in re.finditer(substringToSearch, originalString)]
                    matchCount = len(startBlockID)
                    if(matchCount > 1) and (len(substringToSearch)>1):
                        ms = MatchingSubstring(substringToSearch)
                        ms.AddMatch(substringToSearch, set(startBlockID))
                        matches[substringToSearch] = ms


        #replacements with permutations
        usedIndices = []

        for j in range(minSize,maxSize):

            print time.asctime( time.localtime(time.time()) )
            print "%s of %s" % (j - minSize, maxSize - minSize )

            allSubstrings = SubstringGenerator.generate(originalString, j - 2, j + 2, usedIndices)

            for i in range(0, len(originalString)-j):


                substringToSearch = originalString[i:i+j]
                ss = substringToSearch.replace('0','')

                if len(ss) == 0:
                    continue

                stringToSearchIn = originalString[i+j:]
                # allSubstrings = SubstringGenerator.generate(stringToSearchIn, j - 2, j + 2, usedIndices)


                #possiblePermutations = PermutationGenerator.CustomPermutations(ss)

                for string in allSubstrings:
                    stringToSearch = string.replace('0','')

                    # for permutedString in possiblePermutations:

                    # if (1.0*levenshtein(ss, stringToSearch))/(len(ss)) <= 0.4:
                    if MatchesFinder.fuzzy_compare(ss, stringToSearch,  math.floor(len(ss) * 0.3)):
                        if(substringToSearch not in matches):
                            startBlockID = [m.start() for m in re.finditer(string, originalString)]
                            startBlockID += [m.start() for m in re.finditer(substringToSearch, originalString)]
                            ms = MatchingSubstring(substringToSearch)
                            ms.AddMatch(string, set(startBlockID))
                            matches[substringToSearch] = ms
                        else:
                            ms = matches[substringToSearch]
                            startBlockID = [m.start() for m in re.finditer(string, originalString)]
                            ms.AddMatch(string, set(startBlockID))
                        break

        for match in matches.values():
            res.append(match)
        return res

class PermutationGenerator:
    @staticmethod
    def generate(string):
        allPermuts = permutations(string)
        for perm in allPermuts:
            if(levenshtein(string,perm)/(len(string)+1) <= 0.1):
                yield perm


    @staticmethod
    def CustomPermutations(iterable, r=None):
        # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
        # permutations(range(3)) --> 012 021 102 120 201 210
        pool = tuple(iterable)
        n = len(pool)
        r = n if r is None else r
        if r > n:
            return
        indices = range(n)
        cycles = range(n, n-r, -1)
        #yield tuple(pool[i] for i in indices[:r])
        while n:
            for i in reversed(range(r)):
                cycles[i] -= 1
                if cycles[i] == 0:
                    indices[i:] = indices[i+1:] + indices[i:i+1]
                    cycles[i] = n - i
                else:
                    j = cycles[i]
                    indices[i], indices[-j] = indices[-j], indices[i]
                    yield tuple(pool[i] for i in indices[:r])
                    break
            else:
                return

    @staticmethod
    def oneLevelPermutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
        pool = tuple(iterable)
        n = len(pool)
        r = n if r is None else r
        if r > n:
            return
        indices = range(n)
        for i in range(0,2):
            for i in reversed(range(r)):
                indices[i:] = indices[i+1:] + indices[i:i+1]
                yield tuple(pool[i] for i in indices[:r])

class SubstringGenerator:
    @staticmethod
    def generate(string, minStringLen, maxLen, usedIndices):
        res = []
        hasUsedIndices = False
        if len(usedIndices) > 0:
            hasUsedIndices = True
        for start in xrange(0,len(string)):
            # if hasUsedIndices:
            #     if start in usedIndices:
            #         continue
            for end in xrange(start,len(string)):
                if end - start < minStringLen:
                    continue

                if end - start > maxLen:
                    break

                # if hasUsedIndices:
                #     if end in usedIndices:
                #         continue
                #
                # containsBlackHole = False
                #
                # if hasUsedIndices:
                #     for content in xrange(start, end + 1):
                #         if content in usedIndices:
                #             containsBlackHole = True
                #             break
                #
                # if containsBlackHole:
                #     continue
                
                posibleSubstring = string[start:end]
                ln = len(posibleSubstring)
                if ln >= minStringLen and ln <= maxLen:
                    # yield posibleSubstring
                    res.append(posibleSubstring)
        return res

    

class MatchingSubstring:
    def __init__(self, substring):
        self.substring = substring
        self.startBlockID = set()
        self.matches = set()
    def MatchCount(self):
        return len(self.startBlockID)
    def AddMatch(self,match, blockID):
        self.matches.add(match)
        self.startBlockID |= blockID
    

     

if __name__ == "__main__":
    text = "Ополченцысбилидваукраинских"
    text1 = "abcd"

    print [''.join(p) for p in PermutationGenerator.oneLevelPermutations(text1)]
    print [''.join(p) for p in PermutationGenerator.CustomPermutations(text1)]
    print MatchesFinder.fuzzy_compare("11116362151", "52612156315",  5)

##    print ''.join([CharToESP6Groupd.transform(l) for l in text])
##    testText = "Ополченцы сбили два украинских Су-25 в Донецкой области. Об этом сообщили в штабе антитеррористического центра. Инцидент произошел в районе Саур-Могилы, где штурмовики выполняли боевые задачи. Информации о судьбе пилотов пока нет. Ранее 23 июля о двух сбитых самолетах сообщили ополченцы."
##    anotherTest = "jjmoeeeenjmjiheoeieogokijed"
##    #print SubstringGenerator.generate(anotherTest, 2)
##    matches = MatchesFinder.FindMatchesSubstring(anotherTest)
##    for match in matches:
##        print match.substring + ' ' + str(match.startBlockID) + ' ' + str(match.matches)
