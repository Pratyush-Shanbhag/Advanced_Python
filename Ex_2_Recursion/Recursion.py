class Data:  
    def __init__(self,data):
        self.value = data  
    def __str__(self):
        return str(self.value)
class Node:
    def __init__(self,data,prevNode=None):
        self.data = Data(data)
        self.prevNode = prevNode
        
class Stack:    
    def __init__(self):
        self.head = None
    def isEmpty(self):
        return self.head == None   
    def top(self):
        try:
            return self.head.data
        except:
            return None   
    def push(self, data):
        if self.head is None:
            self.head = Node(data)
        else:
            new_node = Node(data)
            new_node.prevNode = self.head
            self.head = new_node

    def pop(self):
        if self.head is None:
            return None
        else:
            popped = self.head.data
            self.head = self.head.prevNode
            return popped
 
    def empty(self):
        return self.head == None
    
class StackFrame(Stack):
    def __init__(self):
        Stack.__init__(self)
    def push(self,t):
        Stack.push(self,t)
    def pop(self):
        return Stack.pop(self)
    def top(self):
        return Stack.top(self)
    def empty(self):
        return Stack.empty(self)
        
frames = StackFrame()
def bitshow(number):
    global frames
    if number > 0:
        frames.push(number)
        bitshow(number // 2)
        frames.pop()
        if number % 2:
            print('1', end='')
        else:
            print('0', end='')

        
def testBitshow(n):
    if n > 1:
        testBitshow(n-1)
    print(f"{n}: ", end='')
    bitshow(n)
    print()
        
def doTests():
    print("-------------------")
    testBitshow(256)
    print("-------------------")

if __name__=='__main__':
    doTests()