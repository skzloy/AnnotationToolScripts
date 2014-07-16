# -*- coding: cp1251 -*-

import os, os.path
import re


class TextProcessor:
    @staticmethod
    def SignCount(text):
        return len(text.replace(' ', ''))
    
    @staticmethod
    def WordCount(text):
        onlyText = re.sub(r'[^А-Яа-я]', ' ', text)
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
        self.blocks40 = self.GetBlocks(40)
        self.blocks50 = self.GetBlocks(50)
        self.blocks60 = self.GetBlocks(60)
        self.blockClassByID40 = self.SetClassesToBlocks(self.blocks40)
        self.blockClassByID50 = self.SetClassesToBlocks(self.blocks50)
        self.blockClassByID60 = self.SetClassesToBlocks(self.blocks60)

    def GetBlocks(self, size):
        blocks = []
        words = self.text.split(' ')
        blockCount = 1
        blockSize = 0
        textBlock = ''
        wordCount = 0
        for word in words:
            blockSize += len(word)
            
            if(blockSize <= size):
                textBlock += word + ' '
            else:
                block = Block(textBlock, blockCount, wordCount)
                blocks.append(block)
                blockSize = len(word)
                textBlock = word + ' '
                blockCount += 1
            wordCount += 1
            
            
        return blocks

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
                
        

class Block:
    def __init__(self, block, blockID, startWordPosition):
        self.text = block
        self.ID = blockID
        self.startWordPosition = startWordPosition
        self.wordCount = TextProcessor.WordCount(block)
        self.signCount = TextProcessor.SignCount(block)
        self.signWordRation = self.signCount / self.wordCount

    def SetClass(self, blockClass):
        self.blockClass = blockClass

    def __radd__(self, other):
    	return other + self.signWordRation
    

import matplotlib.pyplot as plt

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

        
if __name__ == "__main__":
    pathToFiles = "C:\AnnotationToolScripts\AnnotationToolScripts\Data"
    pathToOutput = "C:\AnnotationToolScripts\AnnotationToolScripts\Output"
    articles = TextParser.GenerateArticlesFromFiles(pathToFiles)
    output = Output(articles)
    output.PrintBlocks(pathToOutput)
    output.DrawBlockClasses(pathToOutput)
    
