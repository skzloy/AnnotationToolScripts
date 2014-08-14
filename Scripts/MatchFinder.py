# -*- coding: cp1251 -*-
from collections import Counter

class EspersanCharacteristic:
    def __init__(self, block):
        self.block = block
        self.ESP6 = ESP6(block)
        self.ESP5 = ESP5(self.ESP6)
        self.ESP3 = ESP3(self.ESP6)

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
    def FindMatchesSubstring(st):
        originalString = st
        matches = {}
        res = []
        #clear matches
        for j in range(2,5):
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
        for j in range(2,5):
            for i in range(0, len(originalString)-j):
                substringToSearch = originalString[i:i+j]

                if substringToSearch in usedSubstrings:
                    continue

                usedSubstrings.add(substringToSearch)
                stringToSearchIn = originalString[i+j:]
                
                allSubstrings = SubstringGenerator.generate(stringToSearchIn, 2)
                possiblePermutations = PermutationGenerator.generate(substringToSearch)
                matchCount = 0
                for string in allSubstrings:
                    if string in substringToSearch:
                            continue
                    for permutedString in possiblePermutations:
                        
                        if (1.0*levenshtein(permutedString, string))/(len(substringToSearch)) <= 0.3:
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

class PermutationGenerator:
    @staticmethod
    def generate(string):
        return set([''.join(p) for p in permutations(string)])

class SubstringGenerator:
    @staticmethod
    def generate(string, minStringLen):
        res = []
        for start in xrange(0,len(string)):
            for end in xrange(start,len(string)):
                posibleSubstring = string[start:end]
                if(len(posibleSubstring) >= minStringLen):
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
    testText = "Ополченцы сбили два украинских Су-25 в Донецкой области. Об этом сообщили в штабе антитеррористического центра. Инцидент произошел в районе Саур-Могилы, где штурмовики выполняли боевые задачи. Информации о судьбе пилотов пока нет. Ранее 23 июля о двух сбитых самолетах сообщили ополченцы."
    anotherTest = "jjmoeeeenjmjiheoeieogokijed"
    #print SubstringGenerator.generate(anotherTest, 2)
    matches = MatchesFinder.FindMatchesSubstring(anotherTest)
    for match in matches:
        print match.substring + ' ' + str(match.startBlockID) + ' ' + str(match.matches)
