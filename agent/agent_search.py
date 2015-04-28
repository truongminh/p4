# Copyright (C) 2015 Peta Masters and Sebastian Sardina
from collections import deque

class Agent(object):
    def __init__(self,**kwargs):
        self.clockface = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
        self.reset()
    
    def addStep(self, step):        
        self.steps.append(step)

    def foundTheGoal(self):
        print "Found the goal: " + str(self.total_cost)
   
    def getNext(self, mapref, current, goal, timeremaining):
        if self.reseted == True:
            self.reseted = False
            self.search(mapref, current, goal)
            self.foundTheGoal()
        return self.steps.popleft()


    def nextStep(self, mapref, current, goal):
        for move in self.clockface:
            candidate = (current[0]+ move[0],current[1] + move[1])
            if mapref.isPassable(candidate, current):
                break
        return candidate

    def reset(self, **kwargs):
        self.reseted = True
        self.steps = deque([])
        self.total_cost = 0
        pass

    def search(self, mapref, start, goal):
        """Performs command line search by calls to generator """
        gen = self.stepGenerator(mapref, start, goal)
        nextstep = start

        # keep generating next steps as long as goal not in goal & enough time
        while not nextstep == goal:
            nextstep = gen.next()
            self.addStep(nextstep)

    def stepGenerator(self, mapref, current, target):       
        while True:            
            nextreturn = self.nextStep(mapref, current, target)
            previous = current
            current = nextreturn
            
            # We now consider every door open. In fact, we are just computing the final path cost, we are not
            # searching for it. So is reasonable to assume that I have all the keys along the path.
            allkeys = [k for k in mapref.key_and_doors.keys()]
            self.total_cost += mapref.getCost(current, previous, allkeys)
            print mapref.getCost(current, previous, allkeys)
            # agent has made illegal move:
            if self.total_cost == float('inf'):
                print("infinity at ", current, ":", mapref.getCost(current))

            yield nextreturn
