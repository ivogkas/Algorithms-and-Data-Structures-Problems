import sys
from collections import deque 

# input arguments
leng=int(len(sys.argv))
firstMethod = False
if leng == 5 :
    input_filename = sys.argv[4]
    radius = int(sys.argv[2])
    komboi = int(sys.argv[3])
else:
    input_filename = sys.argv[3]
    komboi = int(sys.argv[2])
    firstMethod = True

# create graph from input file
graph = {}
with open(input_filename) as graph_input:
    for line in graph_input:
        nodes = [int(x) for x in line.split()]
        if len(nodes) != 2:
            continue
        if nodes[0] not in graph:
            graph[nodes[0]] = []
        if nodes[1] not in graph:
            graph[nodes[1]] = []
        graph[nodes[0]].append(nodes[1])
        graph[nodes[1]].append(nodes[0])

# delete nodes with max degree (first method)
def outMaxDegree():
    for _i in range(0, komboi):
        maxAdjacent = -1
        nodeOut = 0
        for nodes in graph:
            if (len(graph[nodes]) > maxAdjacent) or (len(graph[nodes]) == maxAdjacent and nodes < nodeOut):
                maxAdjacent = len(graph[nodes])
                nodeOut = nodes
        for nodes in graph:
            for value in graph[nodes]:
                if (value == nodeOut):
                    graph[nodes].remove(value)        
        graph.pop(nodeOut)
        print (nodeOut, maxAdjacent)


nmbrOfNodes = len(graph)
#method find ball and θball
def bfs(g, node, radius, allNodes):
    ballList = []  
    nodesList = []   # insert nodes abstain raduis from node
    q = deque()
    visited = [ False for k in range(0,nmbrOfNodes) ]
    inqueue = [ False for k in range(0,nmbrOfNodes) ]
    q.appendleft(node)
    inqueue[node - 1] = True
    listRadius=[[node]]
    listCurrRadius = [node] # nodes in current perimeter
    listNextRadius = [] # nodes in next perimeter
    
    for v in g[node]:
        listNextRadius.append(v)
    listRadius.append(listNextRadius)
    r=0
    while (r <= radius) and (len(q) > 0): 
        c = q.pop()
        inqueue[c - 1] = False
        visited[c - 1] = True
        ballList.append(c)
        for v in g[c]:
            if not visited[v - 1] and not inqueue[v - 1]:
                q.appendleft(v)
                inqueue[v - 1] = True
        if (c not in listCurrRadius):    # all nodes of current radius have visited
            listCurrRadius = listNextRadius
            listNextRadius = []
            r = r + 1
            if (r == radius):    # put in nodesList nodes which abstain radius=input radius
                for value in listCurrRadius:
                    if (value not in nodesList):
                        nodesList.append(value)
            for cn in listCurrRadius:
                for nd in g[cn]:
                    alreadyExist = False
                    for element in listRadius: 
                        if (nd in element):    # check if node is also adjacent of previous node
                            alreadyExist = True
                            break
                    if (not visited[nd - 1] and not alreadyExist and nd not in listNextRadius):
                        listNextRadius.append(nd)
                listRadius.append(listNextRadius)
    visited[c - 1] = False
    ballList.remove(c)
    if (node in ballList): 
        ballList.remove(node)
    # return Ball(i,r) or θBall(i,r)
    if allNodes:
        return ballList
    else:
        return nodesList


# find influence for one node
def calculateInfl(setOfNodes, i):
    sum1 = 0
    for node in setOfNodes:
        sumNode = 0
        for _neig in graph[node]:
            sumNode = sumNode + 1
        sum1 = sum1 + sumNode -1
    sum2 = 0
    for _n in graph[i]:
        sum2 = sum2 + 1
    sum2 = sum2 - 1 
    CI[i] =(sum1 * sum2)
    

# find and delete node with most influence
def deleteNode():
    maxInflNode = 0
    maxInfl = -1
    for infl in CI:
        if ((CI[infl] > maxInfl) or (CI[infl] == maxInfl and infl < maxInflNode)):
            maxInfl = CI[infl]
            maxInflNode = infl
    print(maxInflNode, maxInfl)
    ballRemoveNode = bfs(graph, maxInflNode, radius + 1, True) # Ball(i,r+1)
    graph.pop(maxInflNode)
    CI.pop(maxInflNode)
    for node in graph:
        for neig in graph[node]:
            if (neig == maxInflNode):
                graph[node].remove(neig)
    return ballRemoveNode


CI ={}
def mostInflMethod():
    for node in graph:
        thBall = bfs(graph, node, radius, False)
        calculateInfl(thBall, node)

    for _i in range(0,komboi):
        ball = deleteNode()
        for node in ball:
            thBall = bfs(graph, node, radius, False)
            calculateInfl(thBall, node)

if firstMethod:
    outMaxDegree()
else:
    mostInflMethod()
