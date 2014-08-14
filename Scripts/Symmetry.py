from Levenshtein import *
from MatchFinder import *

class SymmetryExractor:
    def __init__(self, source):
        self.source = source
##        self.matches = MatchesFinder.FindMatchesSubstring(source)
##        self.MapMatches()

    def MapMatches(self):
        self.matchesMap = {}
        counter = 0
        
        for matchSubstring in self.matches:
            matchID = "#%(count)d#" % {"count":counter}
            if matchSubstring.substring not in self.matchesMap.keys():
                self.matchesMap[matchSubstring.substring] = matchID
            for match in matchSubstring.matches:
                if(match not in self.matchesMap.keys()):
                    self.matchesMap[match] = matchID
                else:
                    oldMatchID = self.matchesMap[match]
                    self.matchesMap[matchSubstring.substring] = oldMatchID
            counter += 1

                
    def TransformSource(self):
        self.transformedSource = self.source
        for k, v in self.matchesMap.iteritems():
            self.transformedSource = self.transformedSource.replace(k, v)

        print self.source
        print self.matchesMap
        print self.transformedSource

    def FindSimpleSymmetries(self):
        symmetries = []
        #with non zero centers
        for center in xrange(1, len(self.source)):
##            print "center = %d, len = %d" % (center, len(self.source))
            if(center < len(self.source) - 1 and self.source[center + 1] == '0'):
                continue
            
            left1,sym1,e1 = self.addNeighbors(center-1, center+1,0)
            left2,sym2,e2 = self.addNeighbors(center-1, center+2,0)
            if len(sym1.replace('0','')) > 2:
                left = self.source[left1 : center+1]
                right = self.source[center + 1 : left1+len(sym1)]
                c = ''
                s = Symmetry(sym1, left1, left, right, c)
                symmetries.append(s)
            if len(sym2.replace('0','')) > 2:
                left = self.source[left2 : center+1]
                right = self.source[center+2 : left2+len(sym2)]
                c = self.source[center+1]
                s = Symmetry(sym2, left2, left, right, c)
                symmetries.append(s)

        return symmetries

    def addNeighbors(self, left, right, errorLevel , rkLevel = 0):
        if left < 0 or right > len(self.source)-1:
            return left+errorLevel+1,self.source[left+errorLevel+1:right-errorLevel], 0

                    
        
        #tempBody = self.source[left:right+1]# + body + self.source[right]
        center = (right + left)/2


        if(errorLevel > 3):
            return left+errorLevel+1 , self.source[left+errorLevel+1:right-errorLevel] , 0

        if(rkLevel > 15):
            return left+errorLevel+1 , self.source[left+errorLevel+1:right-errorLevel] , 0

        rkLevel += 1
          
        leftPart = self.source[left:center]
        rightPart = self.source[right:center:-1]
        if (right - left) % 2 != 0:
            leftPart = self.source[left:center+1]
            rightPart = self.source[right+1:center+1:-1]
        
        leftPart = leftPart.replace('0','')

        

        
        rightPart = rightPart.replace('0','')
       
        #print center, self.source[center], leftPart, rightPart
        error = 2.0 * levenshtein(leftPart, rightPart)/(len(leftPart + rightPart)+1)
        
        #print tempBody, error

        if error > 0.3:

            possiblePermutations = PermutationGenerator.generate(rightPart)
            for permutedString in possiblePermutations:
                permutedError = 1.0 * levenshtein(leftPart, permutedString)/(len(leftPart + rightPart)+1)
                if(permutedError > 0.3):
                    if(errorLevel < 3):
                        return self.addNeighbors(left-1, right+1, errorLevel + 1, rkLevel )
                    else:
                        return left+errorLevel+1,self.source[left+errorLevel+1:right-errorLevel], 0
                else:
                    if(errorLevel > 0):
                        errorLevel -= 1
                    return self.addNeighbors(left-1, right+1, errorLevel, rkLevel )

            return self.addNeighbors(left-1, right+1, errorLevel + 1, rkLevel )

        if(errorLevel > 0):
            errorLevel -= 1
        return self.addNeighbors(left-1, right+1, errorLevel, rkLevel)
        
            


class Symmetry:
    def __init__(self, body, startPosition, left, right, center):
        self.body = body
        self.startPosition = startPosition + 1
        self.rightBody = right
        self.leftBody = left
        self.center = center

    def __str__(self):
        filteredText = self.body.replace('0','')
        return "%s" % ( filteredText)


        
if __name__ == "__main__":
    example1 = "dckdmekqoqkjeeeeedkmdejeojmkdkiddeeiheekoegjekkkeemjijjekodjejecjeqejeekjeeieokcedjjqedeecjenfejkjemjomjjdeenkijjjjeiojjkjjeejgijkjeedihjeejjeekjenci"
    ex2 = "jjmoeeeenjmjiheoeieogokijed"
    
##    print ex2
##    extractor = SymmetryExractor(ex2)
##    for sym in extractor.FindSimpleSymmetries():
##         print sym

##    print example1
    extractor2 = SymmetryExractor(example1)
    for sym in extractor2.FindSimpleSymmetries():
         print sym
