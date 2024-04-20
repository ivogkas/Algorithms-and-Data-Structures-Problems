import pprint
import sys

# input arguments
leng=int(len(sys.argv))
printGraph = False
if (leng == 3 and sys.argv[1] == "-p"):
    printGraph = True
    n=int(sys.argv[2])
else:
    n=int(sys.argv[1])

# create graph using dictonary 
def createGraph(n):
    dict = {}
    for x in range(2-n, n):
        for y in range(0, n):
            list = []
            if ((y>0) or (y==0) and (x>=0)) and (x+y)<=(n-1) and (-x+y)<=(n-1):
                if ((y>0) or (y==0) and (x+1>=0)) and (x+1+y)<=(n-1) and (-x-1+y)<=(n-1):
                    list.append((x+1,y))
                if ((y+1>0) or (y+1==0) and (x>=0)) and (x+y+1)<=(n-1) and (-x+y+1)<=(n-1):
                    list.append((x,y+1))
                if ((y>0) or (y==0) and (x-1>=0)) and (x-1+y)<=(n-1) and (-x+1+y)<=(n-1):
                    list.append((x-1,y))
                if ((y-1>0) or (y-1==0) and (x>=0)) and (x+y-1)<=(n-1) and (-x+y-1)<=(n-1):
                    list.append((x,y-1))
                dict [(x,y)] =  list
    return(dict)

graph = createGraph(n)
class Counter:
     x=0
untried = {(0,0)}
list = []
c = Counter()

# count fixed polyominoes
def count(dict, untried, n, list, i):
    while (len(untried) != 0):
        u = untried.pop()
        list.append(u)
        if (len(list) == n):
            c.x= c.x+1    
        else:
            new_nb = {(0,0)}
            new_nb.remove((0,0))
            for value in dict [u]:
                existUntried = False
                existList = False
                existNeig=False    
                for element in untried:
                    if (element == value):
                        existUntried = True
                        break
                for element in list:
                    if (element == value):
                        existList = True
                        break
                for otherNodes in list:
                    for neig in dict[otherNodes]:
                        if ((otherNodes!=u) and (value==neig)):
                            existNeig=True
                            break
                if (not existUntried and not existList and not existNeig):
                    new_nb.add(value)
            new_untried = set(untried).union(set(new_nb))
            v=int((c.x))
            count(dict, new_untried, n, list, v)
        list.remove(u)    
    return(c) 

p=int((c.x))
count(graph, untried, n, list, p)
if printGraph == True:
    pprint.pprint(graph)
print (c.x)