# -*- coding: cp1251 -*-

import os, os.path
import re
from MatchFinder import *
from Symmetry import *

class TextProcessor:
    @staticmethod
    def SignCount(text):
        return len(text.replace(' ', ''))
    
    @staticmethod
    def WordCount(text):
        onlyText = re.sub(r'[^А-Яа-я0-9A-Za-z]', ' ', text)
        return len(onlyText.split())

class TextParser:
    @staticmethod
    def GenerateArticlesFromFiles(pathToFolder):
        #return set of articles
        articles = []
        for subdir, dirs, files in os.walk(pathToFolder):
            for file in files:
                filePath = subdir+'/'+file
                articles.append(TextParser.GetArticle(filePath, file))

        return articles

        

    @staticmethod
    def GetArticle(pathToFile, fileName):
        fileObj = open(pathToFile,'r')
        article = Article(fileObj.read(), fileName)
        fileObj.close()
        return article
        


from operator import attrgetter
class Article:
    def __init__(self, text, title):
        self.text = text
        self.title = title
        self.blocks40, self.BlockIDByWordCount40 = self.GetBlocks(40)
        self.blocks50, self.BlockIDByWordCount50 = self.GetBlocks(50)
        self.blocks60, self.BlockIDByWordCount60 = self.GetBlocks(60)
        self.blockClassByID40 = self.SetClassesToBlocks(self.blocks40)
        self.blockClassByID50 = self.SetClassesToBlocks(self.blocks50)
        self.blockClassByID60 = self.SetClassesToBlocks(self.blocks60)
        self.EstimateRealBlocks()

    def GetBlocks(self, size):
        blocks = []
        onlyText = re.sub(r'[^А-Яа-я0-9A-Za-z]', ' ', self.text)
        words = onlyText.split()
        blockCount = 1
        blockSize = 0
        textBlock = ''
        wordCount = 0
        BlockIDByWordCount = {}
        for word in words:
            blockSize += len(word)

            if(blockSize > size):
                block = Block(textBlock, blockCount, wordCount)
                blocks.append(block)
                blockSize = len(word)
                textBlock = ''
                if(wordCount != len(words)-1):
                    blockCount += 1

            if(blockSize <= size):
                textBlock += word + ' '
                if(wordCount == len(words)-1):
                    block = Block(textBlock, blockCount, wordCount)
                    blocks.append(block)
                    blockSize = len(word)
                    textBlock = word + ' '

            BlockIDByWordCount[wordCount] = blockCount
            wordCount += 1

           
        return blocks, BlockIDByWordCount

    def SetClassesToBlocks(self, blocks):
        maxRatio = 1.0 * max(blocks,key=attrgetter('signWordRation')).signWordRation
        minRatio = 1.0 * min(blocks,key=attrgetter('signWordRation')).signWordRation
        avgRatio = 1.0 * sum(blocks)/len(blocks)
        measure = (maxRatio - minRatio)/avgRatio
        blockClassByID = {}

        for block in blocks:
            if block.signWordRation >= maxRatio - measure:
                block.SetClass(4)
                blockClassByID[block.ID]=4
            elif block.signWordRation > avgRatio:
                block.SetClass(3)
                blockClassByID[block.ID]=3
            elif block.signWordRation == avgRatio:
                block.SetClass(2)
                blockClassByID[block.ID]=2
            elif block.signWordRation >= minRatio + measure:
                block.SetClass(1)
                blockClassByID[block.ID]=1
            else:
                block.SetClass(0)
                blockClassByID[block.ID]=0

        return blockClassByID

    def EstimateRealBlocks(self):
        onlyText = re.sub(r'[^А-Яа-я0-9A-Za-z]', ' ', self.text)
        words = onlyText.split()
        wordCount = 0
        self.blockClassByID40
        self.blockClassByID50
        self.blockClassByID60
        self.words = []
        for word in words:
            wordClass40 = self.GetClassForWord(wordCount, self.BlockIDByWordCount40, self.blockClassByID40)
            wordClass50 = self.GetClassForWord(wordCount, self.BlockIDByWordCount50, self.blockClassByID50)
            wordClass60 = self.GetClassForWord(wordCount, self.BlockIDByWordCount60, self.blockClassByID60)
            customWord = Word(word, wordCount, wordClass40, wordClass50, wordClass60)
            self.words.append(customWord)
            wordCount += 1

    def GetClassForWord(self, wordCount, BlockIDByWordCount, blockClassByID):
        blockID = BlockIDByWordCount[wordCount]
        return blockClassByID[blockID]

class Word:
    def __init__(self, word, position, class40, class50, class60):
        self.word = word
        self.position = position
        self.class40 = class40
        self.class50 = class50
        self.class60 = class60
        self.wordClass = -1
        if(self.class40 == self.class50):
            self.wordClass = self.class40
        elif(self.class40 == self.class60):
            self.wordClass = self.class40
        elif(self.class50 == self.class60):
            self.wordClass = self.class50
        

class Block:
    def __init__(self, block, blockID, startWordPosition):
        self.text = block
        self.ID = blockID
        self.startWordPosition = startWordPosition
        self.wordCount = TextProcessor.WordCount(block)
        self.signCount = TextProcessor.SignCount(block)
        self.signWordRation = self.signCount / self.wordCount
        self.EspChar = EspersanCharacteristic(block)

    def SetClass(self, blockClass):
        self.blockClass = blockClass

    def __radd__(self, other):
    	return other + self.signWordRation
    

#import matplotlib.pyplot as plt

class Output:
    def __init__(self, articles):
        self.articles = articles

    def DrawBlockClasses(self, outFolder):
        if not os.path.exists(outFolder):
            os.makedirs(outFolder)

        for article in self.articles:
            fileName = outFolder + '/' + article.title + '_blocksClasses40.png'
            title = ' BlockSize - 40'
            self.__drawBlockClasses(fileName, article.blocks40, title)
            title = ' BlockSize - 50'
            fileName = outFolder + '/' + article.title + '_blocksClasses50.png'
            self.__drawBlockClasses(fileName, article.blocks50, title)
            fileName = outFolder + '/' + article.title + '_blocksClasses60.png'
            title = ' BlockSize - 60'
            self.__drawBlockClasses(fileName, article.blocks60, title)
            
    def PrintWords(self, outFolder):
        if not os.path.exists(outFolder):
            os.makedirs(outFolder)

        for article in self.articles:
            fileName = outFolder + '/' + article.title + '_words_classes.txt'
            file = open(fileName, 'w')

            output = ''
            previousClass = -1
            currentClass = -1
            passedWords = ''
            for word in article.words:
                currentClass = word.wordClass
                if currentClass == -1:
                    continue

                if not currentClass == previousClass and not previousClass == -1:
                    output += 'class ' + str(previousClass) + '\n'
                    output += passedWords
                    output += '\n\n'
                    passedWords = ''

                passedWords += word.word + ' '

                previousClass = currentClass
            
            file.write(output)
            file.close()
    
    def __drawBlockClasses(self, filename, blocks, title):
        classes = []
        blockID = []
        for block in blocks:
            blockID.append(block.ID)
            classes.append(block.blockClass)
        plt.title(title.encode('utf-8') )
        plt.xlabel('Blocks Number'.encode('utf-8') )
        plt.ylabel('Class, 0 - ii, 1 - ie, 2 - e, 3 - ae, 4 - aa'.encode('utf-8') )
        plt.plot(blockID, classes, 'r')
        plt.savefig(filename)
        plt.clf()

    def PrintBlocks(self, outFolder):
        if not os.path.exists(outFolder):
            os.makedirs(outFolder)

        for article in self.articles:
            fileName = outFolder + '/' + article.title + '_blocks40.txt'
            self.__printBlocks(fileName, article.blocks40)
            fileName = outFolder + '/' + article.title + '_blocks50.txt'
            self.__printBlocks(fileName, article.blocks50)
            fileName = outFolder + '/' + article.title + '_blocks60.txt'
            self.__printBlocks(fileName, article.blocks60)
           

    def __printBlocks(self, fileName, blocks):
        file = open(fileName, 'w')
        output = ''

        output += 'Block ID\t'
        output += 'Text\t'
        output += 'Word Count\t'
        output += 'Sign Count\t'
        output += 'Sign Word Ratio\t'
        output += 'Class\t'
        output += '\n'
        
        for block in blocks:
            
            output += str(block.ID) + '\t'
            output += block.text + '\t'
            output += str(block.wordCount) + '\t'
            output += str(block.signCount) + '\t'
            output += str(block.signWordRation) + '\t'
            output += str(block.blockClass) + '\t'
            output += '\n'

        file.write(output)
        file.close()

    def PrintSymmetries(self, outFolder):
        

        for article in self.articles:
            matches = ''
            for block in article.blocks40:
                matches += block.EspChar.ESP3.GroupID

            fileName = outFolder + '/' + article.title + '_Symmetries40.txt'
            self.__printSymmetries(fileName, matches)

            matches = ''
            for block in article.blocks50:
                matches += block.EspChar.ESP3.GroupID
            
            fileName = outFolder + '/' + article.title + '_Symmetries50.txt'
            self.__printSymmetries(fileName, matches)

            matches = ''
            for block in article.blocks60:
                matches += block.EspChar.ESP3.GroupID
            
            fileName = outFolder + '/' + article.title + '_Symmetries60.txt'
            self.__printSymmetries(fileName, matches)
        
        


    def __printSymmetries(self, fileName, matches):
        file = open(fileName, 'w')
        output = ''
        output += str(matches) + '\n\n'
        mss = MatchesFinder.FindMatchesSubstring(matches)

        extractor = SymmetryExractor(str(matches),mss)
        symmetries = extractor.FindSimpleSymmetries()
        for sym in symmetries:
            output += str(sym.startPosition) + '\t'
            output += sym.body + '\n'
        

        
        file.write(output)
        file.close()
    
    def PrintMatches(self, outFolder):
        if not os.path.exists(outFolder):
            os.makedirs(outFolder)
            
        for article in self.articles:
            matches = ''
            for block in article.blocks40:
                matches += block.EspChar.ESP3.GroupID
                
            fileName = outFolder + '/' + article.title + '_MatchesForBlocks40.txt'
            self.__printMatches(fileName, matches)

            matches = ''
            for block in article.blocks50:
                matches += block.EspChar.ESP3.GroupID
            
            fileName = outFolder + '/' + article.title + '_MatchesForBlocks50.txt'
            self.__printMatches(fileName, matches)

            matches = ''
            for block in article.blocks60:
                matches += block.EspChar.ESP3.GroupID
            
            fileName = outFolder + '/' + article.title + '_MatchesForBlocks60.txt'
            self.__printMatches(fileName, matches)

    def __printMatches(self, fileName, matches):
        file = open(fileName, 'w')
        output = ''
        
        
            
        output += str(matches) + '\n\n'
        mss = MatchesFinder.FindMatchesSubstring(matches)
        for matchSubstring in mss:
            
            output += matchSubstring.substring + '\t'
            output += str(matchSubstring.MatchCount()) + '\t'
            output += str(matchSubstring.matches) + '\t'
            output += str(matchSubstring.startBlockID) + '\n'
            
        
        file.write(output)
        file.close()

        
if __name__ == "__main__":
    pathToFiles = "C:\AnnotationToolScripts\Data"
    pathToOutput = "C:\AnnotationToolScripts\AnnotationToolScripts\Output"
    articles = TextParser.GenerateArticlesFromFiles(pathToFiles)
    output = Output(articles)
    #output.PrintBlocks(pathToOutput)
    #output.DrawBlockClasses(pathToOutput)
    #output.PrintWords(pathToOutput)
    #output.PrintMatches(pathToOutput)
    output.PrintSymmetries(pathToOutput)
