# -*- coding: cp1251 -*-
from collections import Counter

class EspersanCharacteristic:
    def __init__(self, block):
        self.block = block
        self.ESP6 = ESP6(block)
        self.ESP5 = ESP5(self.ESP6)
        self.ESP3 = ESP3(self.ESP3)

class ESP6:
    def __init__(self, text):
        c = Counter(test.lower())
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
        self.EP1, self.EP2, self.EP3 = self.GetESPIndices(self.E1, self.E2, self.E3)
        self.GroupID = self.GetESP3Group(str(self.EP1) + str(self.EP2) + str(self.EP3))

    def GetESPIndices(self, e1, e2, e3):
        ep1 = ep2 = ep3 = 0
        return ep1, ep2, ep3

    def GetESP3Group(self, esp3p):
        return 'a'

if __name__ == "__main__":
    testText = "Ополченцы сбили два украинских Су-25 в Донецкой области. Об этом сообщили в штабе антитеррористического центра. Инцидент произошел в районе Саур-Могилы, где штурмовики выполняли боевые задачи. Информации о судьбе пилотов пока нет. Ранее 23 июля о двух сбитых самолетах сообщили ополченцы."
    
