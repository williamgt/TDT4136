# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import sys

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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
        self.alpha = -sys.maxsize-1
        self.beta = sys.maxsize

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def max_value(self, gameState, depth):
        """
        Finds the maximum value for pacman for some given game state at a particular depth.
        """
        actions = gameState.getLegalActions(0) # Getting all of pacman's legal actions
        if not actions or gameState.isWin() or gameState.isLose() or depth == self.depth: # If no more actions, game is won/lost or at max depth, get the final score
            return (self.evaluationFunction(gameState), None)
        v, move = -sys.maxsize - 1, None # Initializing variables
        # Checking all of pacman's actions
        for a in actions:
            # Getting value and action considering what the ghosts will do
            (v2, a2) = self.min_value(gameState.generateSuccessor(0, a), 2, depth) # 2 is when the first ghost agent starts
            if v2 > v: # If the ghosts allows an action with higher value, update
                v, move = v2, a
        return (v, move)
    
    def min_value(self, gameState, agent_num, depth):
        """
        Finds the minimum value for a given ghost for some given game state at a particular depth.
        When writing agent_num-1. it's converted to its to index.
        """
        actions = gameState.getLegalActions(agent_num-1) # Getting all of the ghost's legal actions
        if not actions: # Ghost has no legal actions
            return (self.evaluationFunction(gameState), None) 
        v, move = sys.maxsize, None # Initializing variables
        # Checking all of the ghost's actions
        for a in actions:
            if agent_num == gameState.getNumAgents(): # Checking the last ghost!
                (v2, a2) = self.max_value(gameState.generateSuccessor(agent_num-1, a), depth+1) # Check next depth because last ghost
            else: # Consider the other ghosts
                (v2, a2) = self.min_value(gameState.generateSuccessor(agent_num-1, a), agent_num+1, depth) # All ghosts at same depth, check min
            if v2 < v: # If some action allows for a lower value, update
                v, move = v2, a
        return (v, move)
        

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        value, move = self.max_value(gameState, 0)
        return move

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def max_value(self, gameState, depth, alpha, beta):
        """
        Finds the maximum value for pacman for some given game state at a particular depth.
        Also does pruning.
        """
        actions = gameState.getLegalActions(0) # Getting all of pacman's legal actions
        if not actions or gameState.isWin() or gameState.isLose() or depth == self.depth: # If no more actions, game is won/lost or at max depth, get the final score
            return (self.evaluationFunction(gameState), None)
        v, move = -sys.maxsize - 1, None # Initializing variables
        # Checking all of pacman's actions
        for a in actions:
            # Getting value and action considering what the ghosts will do
            (v2, a2) = self.min_value(gameState.generateSuccessor(0, a), 2, depth, alpha, beta) # 2 is when the first ghost agent starts
            if v2 > v: # If the ghosts allows an action with higher value, update
                v, move = v2, a
            if v > beta: 
                return (v, move) # Found the most suitable move, prune!
            alpha = max(alpha, v) # Update alpha value if a higher value is found
        return (v, move)
    
    def min_value(self, gameState, agent_num, depth, alpha, beta):
        """
        Finds the minimum value for a given ghost for some given game state at a particular depth.
        Also does pruning.
        When writing agent_num-1. it's converted to its to index.
        """
        actions = gameState.getLegalActions(agent_num-1) # Getting all of the ghost's legal actions
        if not actions: # Ghost has no legal actions
            return (self.evaluationFunction(gameState), None) 
        v, move = sys.maxsize, None # Initializing variables
        # Checking all of the ghost's actions
        for a in actions:
            if agent_num == gameState.getNumAgents(): # Checking the last ghost!
                (v2, a2) = self.max_value(gameState.generateSuccessor(agent_num-1, a), depth+1, alpha, beta) # Check next depth because last ghost
            else: # Consider the other ghosts
                (v2, a2) = self.min_value(gameState.generateSuccessor(agent_num-1, a), agent_num+1, depth, alpha, beta) # All ghosts at same depth, check min
            if v2 < v: # If some action allows for a lower value, update
                v, move = v2, a
            if v < alpha:
                return (v, move) # Found the most suitable move, prune!
            beta = min(beta, v) # Update beta value if a lower value is found
        return (v, move)
    
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        value, move = self.max_value(gameState, 0, -sys.maxsize-1, sys.maxsize)
        return move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
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
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
