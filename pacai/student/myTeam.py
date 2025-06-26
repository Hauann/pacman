from pacai.agents.capture.capture import CaptureAgent
import random

class OffensiveAgent(CaptureAgent):
    """
    An offensive agent that seeks out and captures food of the opponents.
    """
    def registerInitialState(self, gameState):
        super().registerInitialState(gameState)

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)

        # Get food locations
        foodList = self.getFood(gameState).asList()
        if len(foodList) == 0:
            return 'Stop'

        # Compute closest food
        myPos = gameState.getAgentPosition(self.index)
        closestFood = min(foodList, key=lambda food: self.getMazeDistance(myPos, food))

        # Move toward closest food
        bestAction = None
        minDist = float('inf')
        for action in actions:
            successor = gameState.generateSuccessor(self.index, action)
            newPos = successor.getAgentPosition(self.index)
            dist = self.getMazeDistance(newPos, closestFood)

            if dist < minDist:
                minDist = dist
                bestAction = action

        return bestAction

class DefensiveAgent(CaptureAgent):
    """
    A defensive agent that protects its side and blocks opponent Pacmen.
    """
    def registerInitialState(self, gameState):
        super().registerInitialState(gameState)

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        
        # Get opponent positions
        opponents = self.getOpponents(gameState)
        enemyPacmen = [gameState.getAgentPosition(opponent) for opponent in opponents
                       if gameState.getAgentState(opponent).isPacman and gameState.getAgentPosition(opponent) is not None]

        myPos = gameState.getAgentPosition(self.index)
        
        if enemyPacmen:
            # Chase closest enemy Pacman
            closestEnemy = min(enemyPacmen, key=lambda enemy: self.getMazeDistance(myPos, enemy))
            bestAction = None
            minDist = float('inf')
            for action in actions:
                successor = gameState.generateSuccessor(self.index, action)
                newPos = successor.getAgentPosition(self.index)
                dist = self.getMazeDistance(newPos, closestEnemy)

                if dist < minDist:
                    minDist = dist
                    bestAction = action
            
            return bestAction
        
        # If no enemy is visible, patrol near food
        foodToDefend = self.getFoodYouAreDefending(gameState).asList()
        if foodToDefend:
            closestFood = min(foodToDefend, key=lambda food: self.getMazeDistance(myPos, food))
            bestAction = None
            minDist = float('inf')
            for action in actions:
                successor = gameState.generateSuccessor(self.index, action)
                newPos = successor.getAgentPosition(self.index)
                dist = self.getMazeDistance(newPos, closestFood)

                if dist < minDist:
                    minDist = dist
                    bestAction = action
            
            return bestAction

        return random.choice(actions)

def createTeam(firstIndex, secondIndex, isRed):
    """
    This function returns a team of two agents for Capture the Flag.
    """
    return [
        OffensiveAgent(firstIndex, isRed),
        DefensiveAgent(secondIndex, isRed),
    ]