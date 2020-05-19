from enum import IntEnum 

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

class GridGraph:

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
    16:"⯈",
    32:"⯇",
    64:"⯆",
    128:"⯅"
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
        #global symbols
        for x in range (self.n-1, -1, -1):
            for y in range(0, self.n):
                print(self.symbols[self.nodes[x][y].edges], end='')
            print("")
                