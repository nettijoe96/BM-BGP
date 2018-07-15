"""
This is the class for updates!
"""

import math

class IP:
    prefix = 32
    decimalIP = []
    binaryIP = []
    #we will represent IP address as a list of 0 and 1's so because bits in python suck!!


    def __init__(self, numList, type, prefix):
        self.prefix = prefix
        if type == "b":
            self.binaryIP = numList
            self.decimalIP = []
            self.IPFromBinary()
        elif type == "d":
            self.decimalIP = numList
            self.binaryIP = []
            self.IPFromDecimal()


    def toDecString(self):
        string = ""
        for num in self.decimalIP:
            numStr = str(num)
            if len(numStr) == 1:
                numStr = "00" + numStr
            elif len(numStr) == 2:
                numStr = "0" + numStr
            numStr += ","
            string += numStr
        pre = ""
        if(self.prefix < 10):
            pre = "0"
        string += (pre + str(self.prefix))

        return string

    def toBinString(self):
        string = ""
        for num in self.binaryIP:
            string += str(num)
        pre = ""
        if (self.prefix < 10):
            pre = "0"
        string += (pre + str(self.prefix))
        return string

    def getDecimalIP(self):
        return self.decimalIP

    def getBinaryIP(self):
        return self.binaryIP

    def IPFromDecimal(self):
        #initialize to 0
        for i in range(32):
            self.binaryIP.append(0)

        position0 = 0
        for num in self.decimalIP:
            remainder = num
            while(remainder != 0):
                exp = int(math.floor(math.log2(remainder)))
                self.binaryIP[7 - exp + position0] = 1
                remainder = remainder - (math.pow(2, exp))
            position0 += 8


    def IPFromBinary(self):
        byte = -1
        dec = 0

        for j in range(4):
            self.decimalIP.append(0)

        for i in range(32):
            pos = i % 8
            if pos == 0:
                if byte != -1:
                    self.decimalIP[byte] = dec
                byte += 1
                dec = 0
            if self.binaryIP[i] == 1:
                dec += (pow(2, (7-pos)))
        self.decimalIP[byte] = dec



def testIP():

    decimal = [0, 0, 255, 255]
    ipA = IP(decimal, "d", 20)
    print("**decimal to binary**")
    print("decimal: ")
    print(ipA.decimalIP)
    print("binary: ")
    print(ipA.binaryIP)

    ipB = IP(ipA.binaryIP, "b", 20)
    print("**binary to decimal**")
    print("decimal: ")
    print(ipB.decimalIP)
    print("binary: ")
    print(ipB.binaryIP)



class Update:
    path = []
    destIP = None
    merkleMatrix = []
    signatureMatrix = []
    ASN = None
    randomNumber = None
    otherData = None


    def __init__(self, ASN, path, destIP, merkleMatrix, signatureMatrix, randomNumber, otherData):
        self.otherData = otherData
        self.randomNumber = randomNumber
        self.ASN = ASN
        self.path = path
        self.destIP = destIP
        self.merkleMatrix = merkleMatrix
        self.signatureMatrix = signatureMatrix

    def possibleNewPath(self, newPath):
        #only compare hops for now. If new path has less hops, new path becomes current path
        if len(newPath) < len(self.path):
            self.path = newPath





