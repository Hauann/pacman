"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    Reduced noise to encourage the agent to take a more deterministic path.
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise

def question3a():
    """
    Prefer the close exit, risking the cliff by reducing noise.
    """

    answerDiscount = 0.3
    answerNoise = 0.0
    answerLivingReward = -1.0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    Prefer the close exit, avoiding the cliff by keeping some noise.
    """

    answerDiscount = 0.3
    answerNoise = 0.2
    answerLivingReward = -1.0

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    Prefer the distant exit, risking the cliff by reducing noise.
    """

    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    Prefer the distant exit, avoiding the cliff by keeping some noise.
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    Avoid both exits and maximize living time by setting a high living reward.
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 10.0

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    Q-learning is not possible with the given constraints.
    """
    
    return NOT_POSSIBLE

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
