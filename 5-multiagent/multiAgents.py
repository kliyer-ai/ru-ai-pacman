#samarpan rai (4753763) & nick stracke (4771192)

# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)

    #possible querries
    #'data', 'deepCopy', 'generatePacmanSuccessor', 'generateSuccessor', 'getCapsules', 'getFood', 'getGhostPosition', 'getGhostPositions', 'getGhostState', 'getGhostStates',
    # 'getLegalActions', 'getLegalPacmanActions', 'getNumAgents', 'getNumFood', 'getPacmanPosition', 'getPacmanState', 'getScore', 'getWalls', 'hasFood', 'hasWall', 'initialize',
    # 'isLose', 'isWin'


    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFoods = successorGameState.getFood().asList()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newGhostPositions = successorGameState.getGhostPositions()

    closestGhost = min([manhattanDistance(newPos, newGhost) for newGhost in newGhostPositions])
    #indexGhost = [i for i in range(len(newGhostPositions)) if manhattanDistance(newPos, newGhostPositions[i])==closestGhost]

    closestFood=0
    if newFoods:
      closestFood = min([manhattanDistance(newPos, newFood) for newFood in newFoods])




    if closestGhost < 2 and 0 in newScaredTimes: #newScaredTimes[indexGhost[0]]==0:
      return -9999
    elif (currentGameState.getNumFood() - successorGameState.getNumFood())==1:
      return 9999
    else:
      return -closestFood




def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent for one opponent (assignment 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    #http://artint.info/html/ArtInt_240.html
    score, action = self._maxPlayer(gameState, 1)
    print(score)
    return action



  def _maxPlayer(self, gameState, depth):
    actions = gameState.getLegalActions(0)
    bestScore = -9999
    bestAction = None
    for action in actions:
      successorState = gameState.generateSuccessor(0, action)

      if successorState.isWin() or successorState.isLose():
        successorScore = self.evaluationFunction(successorState)
      else:
        successorScore, _ = self._minPlayer(successorState, depth)

      if successorScore > bestScore:
        bestScore = successorScore
        bestAction = action
    return (bestScore, bestAction)



  def _minPlayer(self, gameState, depth):
    actions = gameState.getLegalActions(1)
    bestScore = 9999

    for action in actions:
      successorState = gameState.generateSuccessor(1, action)

      if depth == self.depth: #check if leaf node
        successorScore = self.evaluationFunction(successorState)
        if successorScore < bestScore:
          bestScore = successorScore
      else:
        successorScore, _ = self._maxPlayer(successorState, depth+1)
        if successorScore < bestScore:
          bestScore = successorScore

    return (bestScore, None)

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning for one ghost (assignment 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    alpha = -9999
    beta = 9999
    player = 0
    bestAction="Stop"

    actions = gameState.getLegalActions(player)
    for action in actions:
        successorState = gameState.generateSuccessor(player, action)
        successorScore = self._alphaBeta(successorState, alpha, beta, 1, self.depth)
        if successorScore > alpha:
            alpha = successorScore
            bestAction = action
    return bestAction


  def _alphaBeta(self, gameState, alpha, beta, player, depth):
    if gameState.isWin() or gameState.isLose() or depth==0:
      return self.evaluationFunction(gameState)

    actions = gameState.getLegalActions(player)
    if player==0:
      for action in actions:
        successorState = gameState.generateSuccessor(player, action)
        alpha = max(alpha,self._alphaBeta(successorState,alpha,beta,1,depth))
        if alpha >= beta:
            return alpha
      return alpha

    else:
      for action in actions:
        successorState = gameState.generateSuccessor(player, action)
        beta = min(beta, self._alphaBeta(successorState, alpha, beta, 0, depth-1))
        if alpha >= beta:
          return beta
      return beta





class MultiAlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning for several ghosts (Extra credit assignment B)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()    

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (not used in this course)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function for one ghost (extra credit assignment A).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest (not used in this course)
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

