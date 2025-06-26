import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core.directions import Directions

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***

        newPosition = successorGameState.getPacmanPosition()
        foodList = successorGameState.getFood().asList()
        ghostStates = successorGameState.getGhostStates()
        ghostPositions = [ghost.getPosition() for ghost in ghostStates]
        
        if successorGameState.isLose():
            return float('-inf')
        if successorGameState.isWin():
            return float('inf')
        
        def manhattanDistance(pos1, pos2):
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

        foodDistance = min([manhattanDistance(newPosition, food) for food in foodList]) if foodList else 0
        ghostDistance = min([manhattanDistance(newPosition, ghost) for ghost in ghostPositions]) if ghostPositions else float('inf')
        
        return successorGameState.getScore() + (1.0 / foodDistance) - (1.0 / ghostDistance)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
    
    def getAction(self, gameState):
        def minimax(state, depth, agentIndex):
            if depth == self.getTreeDepth() or state.isWin() or state.isLose():
                return self.getEvaluationFunction()(state)
            
            if agentIndex == 0:
                return max(minimax(state.generateSuccessor(agentIndex, action), depth, 1) for action in state.getLegalActions(agentIndex))
            else:
                nextAgent = agentIndex + 1 if agentIndex < state.getNumAgents() - 1 else 0
                nextDepth = depth + 1 if nextAgent == 0 else depth
                return min(minimax(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent) for action in state.getLegalActions(agentIndex))
        
        return max(gameState.getLegalActions(0), key=lambda action: minimax(gameState.generateSuccessor(0, action), 0, 1))

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
    
    def getAction(self, gameState):
        def alphabeta(state, depth, agentIndex, alpha, beta):
            if depth == self.getTreeDepth() or state.isWin() or state.isLose():
                return self.getEvaluationFunction()(state)
            
            if agentIndex == 0:
                value = float('-inf')
                for action in state.getLegalActions(agentIndex):
                    value = max(value, alphabeta(state.generateSuccessor(agentIndex, action), depth, 1, alpha, beta))
                    if value > beta:
                        return value
                    alpha = max(alpha, value)
                return value
            else:
                value = float('inf')
                nextAgent = agentIndex + 1 if agentIndex < state.getNumAgents() - 1 else 0
                nextDepth = depth + 1 if nextAgent == 0 else depth
                for action in state.getLegalActions(agentIndex):
                    value = min(value, alphabeta(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent, alpha, beta))
                    if value < alpha:
                        return value
                    beta = min(beta, value)
                return value
        
        return max(gameState.getLegalActions(0), key=lambda action: alphabeta(gameState.generateSuccessor(0, action), 0, 1, float('-inf'), float('inf')))

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
    
    def getAction(self, gameState):
        def expectimax(state, depth, agentIndex):
            if depth == self.getTreeDepth() or state.isWin() or state.isLose():
                return self.getEvaluationFunction()(state)
            
            if agentIndex == 0:
                return max(expectimax(state.generateSuccessor(agentIndex, action), depth, 1) for action in state.getLegalActions(agentIndex))
            else:
                nextAgent = agentIndex + 1 if agentIndex < state.getNumAgents() - 1 else 0
                nextDepth = depth + 1 if nextAgent == 0 else depth
                return sum(expectimax(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent) for action in state.getLegalActions(agentIndex)) / len(state.getLegalActions(agentIndex))
        
        return max(gameState.getLegalActions(0), key=lambda action: expectimax(gameState.generateSuccessor(0, action), 0, 1))

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """
    def manhattanDistance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    pacmanPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    ghostPositions = [ghost.getPosition() for ghost in ghostStates]
    ghostDistance = min([manhattanDistance(pacmanPos, ghost) for ghost in ghostPositions]) if ghostPositions else float('inf')
    foodDistance = min([manhattanDistance(pacmanPos, food) for food in foodList]) if foodList else 0
    return currentGameState.getScore() + (1.0 / (foodDistance + 1)) - (1.0 / (ghostDistance + 1))

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
    
    def getAction(self, gameState):
        return AlphaBetaAgent(self.index, **self.kwargs).getAction(gameState)
