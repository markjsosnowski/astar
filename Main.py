import random 
from datetime import datetime
import math
from MinHeap import Heap
from GridGraph import GridGraph

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
    
    #visited_nodes_count = 0 
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
    graph = GridGraph(n)
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
    graph = GridGraph(n)
    for x in range(0,n):
        for y in range(0,n):
            w = random.randint(1,6)
            graph.addNode(x,y,w)
            if(y > 0 and coinFlip()):
                graph.addEdge(graph.nodes[x][y], graph.nodes[x][y-1])
            if(x > 0 and coinFlip()):
                graph.addEdge(graph.nodes[x][y], graph.nodes[x-1][y])
    return graph

'''             
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
'''

n = 40
x1 = 0 
x2 = 39 
y1 = 0
y2 = 39 

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