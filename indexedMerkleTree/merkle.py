#this is the file for creating the indexed merkle tree

import update
import hashlib

class Error:
    errorStr = ""

    def __init__(self, error):
        self.errorStr = error

class routingTable:
    destinations = {}
    merkleRoot = None





class Node:
    hash = None
    update = None
    parent = None
    leftChild = None
    rightChild = None
    middleChild = None
    isLeft = False
    isRight = False
    isMiddle = False
    isRoot = True

    def __init__(self, updateObj=None):
            self.isLeft = False
            self.isRight = False
            self.isMiddle = False
            self.leftChild = None
            self.rightChild = None
            self.middleChild = None
            self.isRoot = False
            self.update = updateObj
            if updateObj == "RIGHT" or updateObj == "LEFT":
                self.hash = hashFunction(updateObj)
            elif updateObj != None:
                self.hash = hashFunction(
                    updateObj.destIP.toDecString() + str(updateObj.path) + str(updateObj.otherData) + str(
                        updateObj.randomNumber))



def hashFunction(data):
    """
    Obviously this isn't a real hash function. I just returned data for the tests so that debugging was easier. Will change to hashing and test it soon.
    :param data:
    :return:
    """
    return data



def dataOfIP(IPDecStr):
    #grab update from table
    return IPDecStr

def constructTree(UpdateList, IPstr, currentNode):

    extra1 = False
    extra0 = False
    extra1IPList = []
    extra0IPList = []
    extra1str = IPstr + "1"
    extra0str = IPstr + "0"

    if len(extra0str) > 32:
        return

    for update in UpdateList:
        if extra0str == update.destIP.toBinString()[:len(extra0str)] and update.destIP.prefix >= len(IPstr) + 1:
            extra0IPList += [update]
            if len(extra0str) == update.destIP.prefix:
                currentNode.leftChild = Node(dataOfIP(update))
                currentNode.leftChild.parent = currentNode
                currentNode.leftChild.isLeft = True
            #TODO add the possibility to add the node as a leaf when it is the only node left in the list (if len(updateList==1)). This would make the algorithm faster to the point where a condense may not even be needed.
            extra0 = True
        if extra1str == update.destIP.toBinString()[:len(extra1str)] and update.destIP.prefix >= len(IPstr) + 1:
            extra1IPList += [update]
            if len(extra1str) == update.destIP.prefix:
                currentNode.rightChild = Node(dataOfIP(update))
                currentNode.rightChild.parent = currentNode
                currentNode.rightChild.isRight = True
            extra1 = True

    if extra0 or extra1:
        if currentNode.update != None:
            currentNode.middleChild = Node(currentNode.update)
            currentNode.middleChild.isMiddle = True
            currentNode.hash = None
            currentNode.update = None
            currentNode.middleChild.parent = currentNode

    if extra0:
        if(currentNode.leftChild == None):
            currentNode.leftChild = Node()
            currentNode.leftChild.isLeft = True
            currentNode.leftChild.parent = currentNode
        constructTree(extra0IPList, extra0str, currentNode.leftChild)
    if extra1:
        if(currentNode.rightChild == None):
            currentNode.rightChild = Node()
            currentNode.rightChild.isRight = True
            currentNode.rightChild.parent = currentNode
        constructTree(extra1IPList, extra1str, currentNode.rightChild)


def condense(currNode):

    if (currNode.leftChild == None and currNode.rightChild == None and currNode.middleChild == None):
        if currNode.isLeft:
            #check if there is a right neighbor or middle neighbor
            if currNode.parent.middleChild == None and currNode.parent.rightChild == None:
                if currNode.parent.isLeft:
                    currNode.parent.parent.leftChild = currNode
                    currNode.parent = currNode.parent.parent
                elif currNode.parent.isRight:
                    currNode.parent.parent.rightChild = currNode
                    currNode.parent = currNode.parent.parent
                elif not currNode.parent.isLeft and not currNode.parent.isRight:
                    currNode.parent.update = currNode.update
                    currNode.parent.hash = currNode.hash
                    currNode.parent.leftChild = None
                    return
                condense(currNode)


        elif currNode.isRight:
            # check if there is a right neighbor or middle neighbor
            if currNode.parent.middleChild == None and currNode.parent.leftChild == None:
                if currNode.parent.isLeft:
                    currNode.parent.parent.leftChild = currNode
                    currNode.parent = currNode.parent.parent
                elif currNode.parent.isRight:
                    currNode.parent.parent.rightChild = currNode
                    currNode.parent = currNode.parent.parent
                elif not currNode.parent.isLeft and not currNode.parent.isRight:
                    currNode.parent.update = currNode.update
                    currNode.parent.hash = currNode.hash
                    currNode.parent.rightChild = None
                    return
                condense(currNode)

    #check if node should be moved up
    else:
        if currNode.leftChild != None:
            condense(currNode.leftChild)
        if currNode.rightChild != None:
            condense(currNode.rightChild)
        if currNode.middleChild is not None:
            if currNode.leftChild is None:
                currNode.leftChild = Node("LEFT")
                currNode.leftChild.parent = currNode
                currNode.leftChild.isLeft = True
            elif currNode.rightChild is None:
                currNode.leftChild = Node("RIGHT")
                currNode.rightChild.parent = currNode
                currNode.rightChild.isRight = True


def createRoot(rootNode):
    hashL = ""
    hashM = ""
    hashR = ""

    if(rootNode.leftChild != None):
        hashL = createRoot(rootNode.leftChild)
    if(rootNode.middleChild != None and rootNode.middleChild.update != None):
        hashM = rootNode.middleChild.hash
    if(rootNode.rightChild != None):
        hashR = createRoot(rootNode.rightChild)

    if(rootNode.leftChild == None and rootNode.rightChild == None and rootNode.middleChild == None and rootNode.update != None):
        return rootNode.hash

    rootNode.hash = hashL + hashM + hashR
    return rootNode.hash

def verifyInTree(route, hashList):
    pass

def hashesToVerify(root, destPrefix):


    #find predix in tree ASSUMING it is already in there
    prefix = destPrefix.prefix
    binaryIP = destPrefix.binaryIP
    currNode = root
    j = 0
    while j < len(binaryIP):
        if currNode.update is not None and currNode.update.destIP.toDecString() == destPrefix.toDecString():
            break
        if currNode.middleChild != None:
            if currNode.middleChild.update.destIP.toDecString() == destPrefix.toDecString():
                currNode = currNode.middleChild
                break
        if binaryIP[j] == 0:
            currNode = currNode.leftChild
        else:
            currNode = currNode.rightChild
        j += 1

    hashLst = []
    if currNode.isRoot:
        hashLst += [[currNode.hash]]
    else:
        #create lowest level list that contains the hash of the leaf we are verifying
        if currNode.isLeft:
            hashLst += [currNode.hash]
            if currNode.parent.middleChild != None:
                hashLst += [currNode.parent.middleChild.hash]
            if currNode.parent.rightChild != None:
                hashLst += [currNode.parent.rightChild.hash]
        elif currNode.isMiddle:
            if currNode.parent.leftChild != None:
                hashLst += [currNode.parent.leftChild.hash]
            hashLst += [currNode.hash]
            if currNode.parent.rightChild != None:
                hashLst += [currNode.parent.rightChild.hash]
        elif currNode.isRight:
            if currNode.parent.leftChild != None:
                hashLst += [currNode.parent.leftChild.hash]
            if currNode.parent.middleChild != None:
                hashLst += [currNode.parent.middleChild.hash]
            hashLst += [currNode.hash]
        if currNode.parent.isLeft:
            newNode = currNode.parent.parent.rightChild
            currNode = currNode.parent.parent
            while True:
                if newNode is None and not currNode.isRoot:
                    newNode = currNode.parent.rightChild
                    middle = ""
                    if currNode.middleChild != None:
                        middle = currNode.middleChild.hash
                    hashLst = [hashLst, middle + ""]
                    currNode = currNode.parent
                else:
                    if newNode is not None:
                        currNode = newNode
                    if currNode.isRoot:
                        hashLst = [hashLst, ""]
                    break
        else:
            newNode = currNode.parent.parent.leftChild
            currNode = currNode.parent.parent
            while True:
                if newNode is None and not currNode.isRoot:
                    newNode = currNode.parent.leftChild
                    middle = ""
                    if currNode.middleChild != None:
                        middle = currNode.middleChild.hash
                    hashLst = ["" + middle, hashLst]
                    currNode = currNode.parent
                else:
                    if newNode is not None:
                        currNode = newNode
                    if currNode.isRoot:
                        hashLst = ["", hashLst]
                    break
        #while current node is not root (while isLeft or isRight)
        while currNode.isLeft or currNode.isRight:
            if currNode.isLeft:
                middle = ""
                if currNode.parent.middleChild != None:
                    middle = currNode.parent.middleChild.hash
                hashLst = [currNode.hash + middle, hashLst]
            elif currNode.isRight:
                middle = ""
                if currNode.parent.middleChild != None:
                    middle = currNode.parent.middleChild.hash
                hashLst = [hashLst, middle + currNode.hash]
            if currNode.parent.parent != None:
                if currNode.parent.isLeft:
                    newNode = currNode.parent.parent.rightChild
                    currNode = currNode.parent.parent
                    while True:
                        if newNode is None and not currNode.isRoot:
                            newNode = currNode.parent.rightChild
                            middle = ""
                            if currNode.middleChild != None:
                                middle = currNode.middleChild.hash
                            hashLst = [hashLst, middle + ""]
                            currNode = currNode.parent
                        else:
                            if newNode is not None:
                                currNode = newNode
                            if currNode.isRoot:
                               hashLst = [hashLst, ""]
                            break
                else:
                    newNode = currNode.parent.parent.leftChild
                    currNode = currNode.parent.parent
                    while True:
                        if newNode is None and not currNode.isRoot:
                            newNode = currNode.parent.leftChild
                            middle = ""
                            if currNode.middleChild != None:
                                middle = currNode.middleChild.hash
                            hashLst = ["" + middle, hashLst]
                            currNode = currNode.parent
                        else:
                            if newNode is not None:
                                currNode = newNode
                            if currNode.isRoot:
                                hashLst = ["", hashLst]
                            break
            else:
                break

    return hashLst

def verifyLeaf(rootHash, verifyList, route):
    routeHash = Node(route).hash
    binaryIP = route.destIP.binaryIP
    newRootHash = getRootFromVerifyList(verifyList, route.destIP.binaryIP, route.destIP.prefix, routeHash, 0)
    isValid = (newRootHash == rootHash)
    return isValid

def getRootFromVerifyList(verifyList, binaryIP, prefix, routeHash, IPindex):

    bit = binaryIP[IPindex]

    end = True
    for item in verifyList:
        end = True
        if isinstance(item, list):
            end = False
            break

    if end:
        if len(verifyList) == 3 and "" not in verifyList:
            #middle
            if prefix == IPindex:
                if routeHash != verifyList[1]:
                    return Error("WRONG POSITION middle3")
            #left
            elif binaryIP[IPindex] == 0:
                if routeHash != verifyList[0]:
                    return Error("WRONG POSITION left3")
            #right
            elif binaryIP[IPindex] == 1:
                if routeHash != verifyList[2]:
                    return Error("WRONG POSITION right3")
            return hashFunction(verifyList[0] + verifyList[1] + verifyList[2])
        elif len(verifyList) == 2 and "" not in verifyList:
            # left
            if binaryIP[IPindex] == 0:
                if routeHash != verifyList[0]:
                    return Error("WRONG POSITION left2")
            # right
            if binaryIP[IPindex] == 1:
                if routeHash != verifyList[1]:
                    return Error("WRONG POSITION right2")
            return hashFunction(verifyList[0] + verifyList[1])

        else:
            Error("WRONG FORMAT")
    else:
        if isinstance(verifyList[bit], list):
            hashO = getRootFromVerifyList(verifyList[bit], binaryIP, prefix, routeHash, IPindex + 1)
            if isinstance(hashO, Error):
                return hashO
        else:
            return Error("WRONG LIST")

        if bit == 0:
            return hashFunction(hashO + verifyList[1])
        elif bit == 1:
            return hashFunction(verifyList[0] + hashO)






def testRoot():
    one = Node(1)
    two = Node(2)
    three = Node(3)
    four = Node(4)
    five = Node(5)
    six = Node(6)

    leafList = [one, two, three, four, five, six]

    merkleTree = createRoot(leafList)

def testTreeCreate():
    A = update.IP([224, 0, 0, 0], "d", 3)
    B = update.IP([128, 0, 0, 0], "d", 2)
    C = update.IP([64, 0, 0, 0], "d", 2)
    D = update.IP([32, 0, 0, 0], "d", 3)
    E = update.IP([128, 0 , 0 ,0], "d", 1)
    F = update.IP([0, 0 , 0 ,0], "d", 1)


    IPlist = [A, B, C, D, E, F]

    root = Node(None)
    constructTree(IPlist, "", root)
    print(3)

#diagram of test in red notebook labeled test2
def test2():
    A = update.IP([128, 0 , 0 ,0], "d", 1)
    B = update.IP([192, 0 , 0 ,0], "d", 2)
    C = update.IP([224, 0 , 0 ,0], "d", 3)
    D = update.IP([240, 0 , 0 ,0], "d", 4)

    E = update.IP([248, 0 , 0 ,0], "d", 5)

    F = update.IP([128, 0 , 0 ,0], "d", 2)
    G = update.IP([192, 0 , 0 ,0], "d", 3)
    H = update.IP([224, 0 , 0 ,0], "d", 4)
    I = update.IP([240, 0 , 0 ,0], "d", 5)

    J = update.IP([0, 0 , 0 ,0], "d", 3)

    IPlist = [A, B, C, D, E, F, G, H, I, J]
    IPlist = [E]

    root = Node(None)
    constructTree(IPlist, "", root)
    condense(root)
    createRoot(root)
    print(4)


#diagram of test in red notebook labeled test2
def testGetHashes():
    C = update.IP([128, 0 , 0 ,0], "d", 1)
    E = update.IP([192, 0 , 0 ,0], "d", 2)
    G = update.IP([224, 0 , 0 ,0], "d", 3)
    I = update.IP([240, 0 , 0 ,0], "d", 4)

    J = update.IP([248, 0 , 0 ,0], "d", 5)

    B = update.IP([128, 0 , 0 ,0], "d", 2)
    D = update.IP([192, 0 , 0 ,0], "d", 3)
    F = update.IP([224, 0 , 0 ,0], "d", 4)
    H = update.IP([240, 0 , 0 ,0], "d", 5)

    A = update.IP([0, 0 , 0 ,0], "d", 3)

    A = update.IP([224, 0, 0, 0], "d", 4)
    B = update.IP([128, 0, 0, 0], "d", 3)
    C = update.IP([64, 0, 0, 0], "d", 2)
    D = update.IP([32, 0, 0, 0], "d", 3)
    E = update.IP([64, 0 , 0 ,0], "d", 3)
    F = update.IP([0, 0 , 0 ,0], "d", 1)


    IPlist = [A, B, C, D, E, F, G, H, I, J]

    UA = update.Update(0, [1, 2], A, [], [], 0, [])
    UB = update.Update(1, [1, 2], B, [], [], 1, [])
    UC = update.Update(2, [1, 2], C, [], [], 2, [])
    UD = update.Update(3, [1, 2], D, [], [], 3, [])
    UE = update.Update(4, [1, 2], E, [], [], 4, [])
    UF = update.Update(5, [1, 2], F, [], [], 5, [])
    UG = update.Update(6, [1, 2], G, [], [], 6, [])
    UH = update.Update(7, [1, 2], H, [], [], 7, [])
    UI = update.Update(8, [1, 2], I, [], [], 8, [])
    UJ = update.Update(9, [1, 2], J, [], [], 9, [])

    updateList = [UA, UB, UC, UD, UE, UF, UG, UH, UI, UJ]
    # IPlist = [A, B, C, D, E, F]

    root = Node()
    constructTree(updateList, "", root)
    condense(root)
    createRoot(root)
    hashLst = hashesToVerify(root, J)
    print(4)

def test3():

    A = update.IP([224, 0, 0, 0], "d", 3)
    B = update.IP([252, 0, 0, 0], "d", 6)
    C = update.IP([254, 0, 0, 0], "d", 7)

    UA = update.Update(0, [1, 2], A, [], [], 0, [])
    UB = update.Update(1, [1, 2], B, [], [], 1, [])
    UC = update.Update(2, [1, 2], C, [], [], 2, [])


    updateList = [UA, UB, UC]
    # IPlist = [A, B, C, D, E, F]

    root = Node()
    root.isRoot = True
    constructTree(updateList, "", root)
    condense(root)
    createRoot(root)
    hashLst = hashesToVerify(root, A)
    isValid = verifyLeaf(root.hash, hashLst, UA)
    print(isValid)

def test4():
    IP1 = update.IP([0, 0, 0, 128], "d", 24)
    IP2 = update.IP([0, 0, 0, 0], "d", 1)
    IP3 = update.IP([64, 0, 0, 0], "d", 3)
    IP4 = update.IP([96, 0, 0, 0], "d", 3)
    IP5 = update.IP([112, 0, 0, 0], "d", 4)
    IP6 = update.IP([192, 0, 0, 0], "d", 3)
    IP7 = update.IP([192, 0, 0, 0], "d", 2)
    IP8 = update.IP([252, 0, 0, 0], "d", 6)
    IP9 = update.IP([254, 0, 0, 0], "d", 7)

    U1 = update.Update(1, [1, 2], IP1, [], [], 1, [])
    U2 = update.Update(2, [1, 2], IP2, [], [], 2, [])
    U3 = update.Update(3, [1, 2], IP3, [], [], 3, [])
    U4 = update.Update(4, [1, 2], IP4, [], [], 4, [])
    U5 = update.Update(5, [1, 2], IP5, [], [], 5, [])
    U6 = update.Update(6, [1, 2], IP6, [], [], 6, [])
    U7 = update.Update(7, [1, 2], IP7, [], [], 7, [])
    U8 = update.Update(8, [1, 2], IP8, [], [], 8, [])
    U9 = update.Update(9, [1, 2], IP9, [], [], 9, [])


    updateList = [U1, U2, U3, U4, U5, U6, U7, U8, U9]
    # IPlist = [A, B, C, D, E, F]

    root = Node()
    root.isRoot = True
    constructTree(updateList, "", root)
    condense(root)
    createRoot(root)

    for u1 in updateList:
        hashList = hashesToVerify(root, u1.destIP)
        for u2 in updateList:
            isValid = verifyLeaf(root.hash, hashList, u2)
            if u1 == u2:
                if not isValid:
                    #there is definitely an error
                    print("invalid verification for same update:", u1.destIP.toDecString() + ": " + str(isValid))
            else:
                if isValid:
                    #this doesn't necessarily mean there is an error
                    print("valid verification for: hashlist:", u1.destIP.toDecString() + " verifying:" + u2.destIP.toDecString() + " : " + str(isValid))



# testTreeCreate()
test4()
