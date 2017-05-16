# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
from game import Directions


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print( "Start:", problem.getStartState() )
    print( "Is the start a goal?", problem.isGoalState(problem.getStartState()) )
    print( "Start's successors:", problem.getSuccessors(problem.getStartState()) )
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    return findGoal(problem, stack)


def findGoal(problem, dataStructure):

    #helper function
    def getPath(child,path):
        if child == problem.getStartState():
            return []
        else:
            for c, parent, direction in path:
                if child==c:
                    return getPath(parent,path) + direction

    #initialize lists
    start = problem.getStartState()
    visited = [start]
    path = [(start,None,[])]   #tuple of child node, parent node, direction

    if problem.isGoalState(start):
        return path

    for sLocation, sDirection,sCost in problem.getSuccessors(start):
        dataStructure.push((sLocation, sDirection, sCost, sCost, start))

    while not dataStructure.isEmpty():
        location, direction, cost, totalCost, parent = dataStructure.pop()
        direction = direction if type(direction)==list else [direction] #this makes sure direction is always a list
                                                                        #necessary due to the way crossroad search is implemented
        if location not in visited:
            visited.append(location)
            path.append((location, parent, direction))
            if problem.isGoalState(location):   #check if goal state
                path = getPath(location,path)
                break
            for sLocation, sDirection, sCost in problem.getSuccessors(location):    #add successors
                newTotalCost = totalCost + sCost #accumulate costs; totalCost refers to totalCost of parent; sCost is 1 (in normal search)
                dataStructure.push((sLocation, sDirection, sCost, newTotalCost, location))

    return  path


def breadthFirstSearch(problem):
    "Search the shallowest nodes in the search tree first. [p 81]"
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    return findGoal(problem, queue)


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    def uFSHeursitic(item):
        position, direction, cost, totalCost, parent = item
        print(cost)#heuristic is just total cost
        return cost

    pQWF = util.PriorityQueueWithFunction(uFSHeursitic);
    return findGoal(problem, pQWF)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."

    "*** YOUR CODE HERE ***"
    def aStarHeuristic(item):
        position, direction, cost, totalCost, parent = item
        return totalCost + heuristic(position, problem) #combines actual cost of getting to node with cost of heuristic(manhatten)

    pQWF = util.PriorityQueueWithFunction(aStarHeuristic)
    return findGoal(problem, pQWF)

    "Bonus assignment: Adjust the getSuccessors() method in CrossroadSearchAgent class"
    "in searchAgents.py and test with:"
    "python pacman.py -l bigMaze -z .5 -p CrossroadSearchAgent -a fn=astar,heuristic=manhattanHeuristic "




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
