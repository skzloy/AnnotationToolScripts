from Levenshtein import *
from MatchFinder import *

class SymmetryExractor:
    def __init__(self, source):
        self.source = source

    def Extract(self):
        return self.source

    def FindSimpleSymmetries(self):
        symmetries = []
        #with non zero centers
        for center in xrange(1, len(self.source)):
            #right part
            left1,sym1 = self.addNeighbors(center-1, center+1)
            left2,sym2 = self.addNeighbors(center-1, center+2)
            if len(sym1) > 2:
                s = Symmetry(sym1, left1)
                symmetries.append(s)
            if len(sym2) > 2:
                s = Symmetry(sym2, left2)
                symmetries.append(s)

        return symmetries

    def addNeighbors(self, left, right):
        if left < 0 or right > len(self.source)-1:
            return left+1,self.source[left+1:right]

        #tempBody = self.source[left:right+1]# + body + self.source[right]
        center = (right + left)/2
           
        leftPart = self.source[left:center]
        rightPart = self.source[right:center:-1]
        if (right - left) % 2 != 0:
            leftPart = self.source[left:center+1]
            rightPart = self.source[right:center:-1]
            #tempBody = self.source[left:right+1]
        
        
       
        #print center, self.source[center], leftPart, rightPart
        error = 2.0 * levenshtein(leftPart, rightPart)/(right - left)
        
        #print tempBody, error

        if error > 0.3:

            possiblePermutations = PermutationGenerator.generate(rightPart)
            for permutedString in possiblePermutations:
                permutedError = 1.0 * levenshtein(leftPart, permutedString)/(right - left)
                if(permutedError > 0.3):
                    return left,self.source[left+1:right]
        
        return self.addNeighbors(left-1, right+1 )
        
            


class Symmetry:
    def __init__(self, body, startPosition):
        self.body = body
        self.startPosition = startPosition + 1

    def __str__(self):
        return "Start Pos: %s %s" % ( self.startPosition, self.body)


        
if __name__ == "__main__":
    example1 = "jpjppjpp"
    ex2 = "jjmoeeeenjmjiheoeieogokijed"
    extractor = SymmetryExractor(ex2)
    print extractor.Extract()
    for sym in extractor.FindSimpleSymmetries():
         print sym

    extractor2 = SymmetryExractor(example1)
    print extractor2.Extract()
       
    for sym in extractor2.FindSimpleSymmetries():
         print sym
    #print extractor.addNeighbors(4,6)
    #print extractor.addNeighbors( 0,2)
