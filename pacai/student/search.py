"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***
    stack = Stack()
    stack.push((problem.startingState(), [], set()))  # (state, path, visited)
    
    while not stack.isEmpty():
        state, path, visited = stack.pop()
        
        if problem.isGoal(state):
            return path
        
        if state not in visited:
            visited.add(state)
            for successor, action, _ in problem.successorStates(state):
                stack.push((successor, path + [action], visited.copy()))
    
    return []

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    queue = Queue()
    queue.push((problem.startingState(), []))  # (state, path)
    visited = set()
    
    while not queue.isEmpty():
        state, path = queue.pop()
        
        if problem.isGoal(state):
            return path
        
        if state not in visited:
            visited.add(state)
            for successor, action, _ in problem.successorStates(state):
                queue.push((successor, path + [action]))
    
    return []

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    pq = PriorityQueue()
    pq.push((problem.startingState(), [], 0), 0)  # (state, path, cost)
    visited = {}
    
    while not pq.isEmpty():
        state, path, cost = pq.pop()
        
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost
        
        if problem.isGoal(state):
            return path
        
        for successor, action, stepCost in problem.successorStates(state):
            new_cost = cost + stepCost
            pq.push((successor, path + [action], new_cost), new_cost)
    
    return []

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    pq = PriorityQueue()
    start_state = problem.startingState()
    pq.push((start_state, [], 0), heuristic(start_state, problem))  # (state, path, cost)
    visited = {}
    
    while not pq.isEmpty():
        state, path, cost = pq.pop()
        
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost
        
        if problem.isGoal(state):
            return path
        
        for successor, action, stepCost in problem.successorStates(state):
            new_cost = cost + stepCost
            priority = new_cost + heuristic(successor, problem)
            pq.push((successor, path + [action], new_cost), priority)
    
    return []
