from problems import Node
import sys, math, random

def simulated_annealing(problem):
    def cooldown(t, T0):
        """ Logarithmical multiplicative cooling (Aarts, E.H.L. & Korst, J., 1989) """
        return T0 / (1 + 20 * math.log(1 + t)) if t < T0*10 else 0

    def probability(delta, temperature):
        """" Probability to chose the next node even if there are no improvement """
        return True if math.exp(-abs(delta)/temperature) >= random.uniform(0.0, 1.0) else False

    current = Node(problem.initial)
    for t in range(1, sys.maxsize):
        T = cooldown(t, problem.temperature)
        if T == 0:
            return current
        neighbors = current.expand(problem)
        if not neighbors:
            return current
        next = random.choice(neighbors)
        delta_e = problem.value(next.state) - problem.value(current.state)
        if delta_e < 0 or probability(delta_e, T):
            current = next