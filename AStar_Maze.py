import random 
from datetime import datetime
from enum import IntEnum 
import math

class Directions(IntEnum):
    RIGHT = 1
    LEFT = 2 
    DOWN = 4
    UP = 8

class GraphNode:
    def __init__(self, x, y, w):
        self.x = x 
        self.y = y 
        self.weight = w
        self.edges = 0 #UP DOWN LEFT RIGHT mapped to a binary number 0000
        self.adjNodes = []
    
    #returns the direction of neighbor as compared to this node    
    def compareTo(self, neighbor):
        if(self.x == neighbor.x): #they are on the same row
            if(self.y+1 == neighbor.y):
                return Directions.RIGHT
            if(self.y-1 == neighbor.y):
                return Directions.LEFT
        if(self.y == neighbor.y): #they are on the same col 
            if(self.x+1 == neighbor.x):
                return Directions.UP
            if(self.x-1 == neighbor.x):
                return Directions.DOWN
        return -1
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
                heapifyDown(right)
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
        
class gridGraph:

    symbols = {
    -16:"?",
    -1:"█",
    0:" ",
    1:"╞",
    2:"╡",
    3:"═",
    4:"╥", 
    5:"╔", 
    6:"╗", 
    7:"╦", 
    8:"╨", 
    9:"╚",
    10:"╝", 
    11:"╩", 
    12:"║", 
    13:"╠", 
    14:"╣", 
    15:"╬",
    16:"→",
    32:"←",
    64:"↓",
    128:"↑"
    } 

    def __init__(self,n):
        self.n = n
        self.nodes  = [[None for i in range(n)] for j in range(n)]
        self.nodes_backup = []
        
    def addNode(self,x,y,w):
        self.nodes[x][y] = GraphNode(x,y,w)
        
    def addEdge(self, first, second):
        result = first.compareTo(second)
        if(result != -1):
            first.edges += result
            second.edges += second.compareTo(first)
            first.adjNodes.append(second)
            second.adjNodes.append(first)
            
    def printGraph(self):
        global symbols
        for x in range (self.n-1, -1, -1):
            for y in range(0, self.n):
                print(self.symbols[self.nodes[x][y].edges], end='')
            print("")
                
def getHeuristic(node, finish, cost):
    g = abs(node.y - finish.y) + abs(node.x - finish.x)
    return g + cost

def getPath(parent_map, current):
    path = [] 
    while current is not None:
        path.insert(0,current)
        current = parent_map[current]
        
    return path

def aStar(start, finish):
    minHeap = Heap()
    
    visited_nodes_count = 0 
    visited = set() 
    parent_map = {} #{a node: node's parent}
    cost = {} #{a node:cost to reach that node}
    
    cost[start] = 0
    minHeap.push(start, getHeuristic(start,finish,cost[start]))
    parent_map[start] = None
    
    current = minHeap.pop()
    while current is not None:
        visited.add(current)
        if current is finish:
            return getPath(parent_map, current), cost[current]
        for neighbor in current.adjNodes:
            if neighbor not in visited:
                parent_map[neighbor] = current
                cost[neighbor] = cost[current] + neighbor.weight
                minHeap.push(neighbor, getHeuristic(neighbor, finish, cost[neighbor]))
        current = minHeap.pop()
    return None, None

#graph generation
def coinFlip():
    return random.choice([True, True, False])

def getRandomGraph(n):
    graph = gridGraph(n)
    for x in range(0,n):
        for y in range(0,n):
            #should only check to add edges to previous nodes already made
            graph.addNode(x,y,1) #in this unweighted graph the weight of any node is just 1
            if(y > 0 and coinFlip()):
                graph.addEdge(graph.nodes[x][y], graph.nodes[x][y-1])
            if(x > 0 and coinFlip()):
                graph.addEdge(graph.nodes[x][y], graph.nodes[x-1][y])
    return graph
    
def getWeightedRandomGraph(n):
    graph = gridGraph(n)
    for x in range(0,n):
        for y in range(0,n):
            w = random.randint(1,6)
            graph.addNode(x,y,w)
            if(y > 0 and coinFlip()):
                graph.addEdge(graph.nodes[x][y], graph.nodes[x][y-1])
            if(x > 0 and coinFlip()):
                graph.addEdge(graph.nodes[x][y], graph.nodes[x-1][y])
    return graph
                
#driver code
n = input("Enter the size of the graph: ")
n = int(n)
x1 = input("Start x value: ")
x1 = int(x1)
y1 = input("Start y value: ")
y1 = int(y1)
x2 = input("Goal x value: ")
x2 = int(x2)
y2 = input("Goal y value: ")
y2 = int(y2)

for each in [x1,x2,y1,y2]:
    if each > n or each < 0:
        print("Start or end point exceeds the boundry of the maze.")
        quit()

graph0 = getWeightedRandomGraph(n)
print("The empty graph:")
graph0.printGraph()

startTime = datetime.now()
traversal, cost = aStar(graph0.nodes[x1][y1], graph0.nodes[x2][y2])
endTime = datetime.now()
if traversal is None:
    print ("No path.")
    quit()
else:
    print("Path Found:")
    for node in traversal:
        if traversal.index(node) == 0:
            prev = node
            continue
        prev.edges = 16 * prev.compareTo(node)
        prev = node
    traversal[-1].edges = -1
    graph0.printGraph()
    print("Path Length: ", cost)
    print("Search time: " + str(endTime-startTime))



