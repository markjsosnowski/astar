import math

class HeapNode: 
    def __init__(self, content, hValue): 
        self.content = content #a GraphNode
        self.priority = hValue

class Heap:
    def __init__(self):
        self.heap_array = []
        self.length = 0 

    def push(self, node, hValue):
        self.heap_array.append(HeapNode(node, hValue))
        self.length += 1
        self.heapifyUp(self.length-1)
    
    def heapifyUp(self, posistion):
        parent = math.floor((posistion-1)/2)
        if(posistion ==  0): #if the parent exists
            return
        if(self.heap_array[parent].priority > self.heap_array[posistion].priority):
            self.swap(parent,posistion)
            self.heapifyUp(parent)
    
    def heapifyDown(self, posistion):
        if(posistion == 0):
            return
        left = (2*posistion)+1 
        right = (2*posistion)+2
        if(right < self.length):
            if(self.heap_array[right].priority < self.heap_array[posistion].priority and self.heap_array[right].priority < self.heap_array[left].priority):
                self.swap(posistion, right)
                self.heapifyDown(right)
        elif(left < self.length and self.heap_array[left].priority < self.heap_array[posistion].priority):
            self.swap(posistion, left)
            self.heapifyDown(left)
        
    def swap(self, first, second):
        temp = self.heap_array[first]
        self.heap_array[first] = self.heap_array[second]
        self.heap_array[second] = temp

    def pop(self):
        self.length -= 1
        if( self.length == -1):
            return None
        return_node = self.heap_array.pop(0)
        self.heapifyDown(0)
        return return_node.content
        