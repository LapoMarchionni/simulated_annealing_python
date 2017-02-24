import random
import math
import numpy as np


class Node:
    """ Node of a graph """

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = parent.depth + 1 if parent else 0

    def expand(self, problem):
        "Return a list of one-step distant node"
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        "Return child node"
        next_node = problem.result(self.state, action)
        return Node(next_node, self, action, problem.path_cost(self.path_cost, self.state, action, next))


class Problem:
    """ Basic Problem """

    def __init__(self, temperature):
        self.temperature = temperature

    def path_cost(self, cost, state1, action, state2):
        return cost + 1


class NQueensProblem(Problem):
    """ N-Queens Problem """

    def __init__(self, N, temperature=1000):
        """ N = Chessboard NxN """
        super(self.__class__, self).__init__(temperature)
        self.N = N
        self.name = 'N-Queens'
        self.initial = random.sample(range(self.N), self.N)

    def __conflicts(self, state, row, col):
        """ Check how many other queens are threatening the chosen queen """
        conf = 0
        for col2, row2 in enumerate(state):
            if (row == row2 or row - col == row2 - col2 or row + col == row2 + col2) and col2 != col:
                conf += 1
        return conf

    def actions(self, state):
        """ Move every threatened queens one step up or down """
        states = []
        for col in [x for x in range(self.N) if self.__conflicts(state, state[x], x) != 0]:
            if state[col] < self.N - 1:
                states.append(
                    [x + 1 if n == col else x for n, x in enumerate(state)])
            if state[col] > 0:
                states.append(
                    [x - 1 if n == col else x for n, x in enumerate(state)])
        return states

    def value(self, state):
        """ Check how many queens are threatened in the current state """
        value = 0
        for col in range(self.N):
            value += self.__conflicts(state, state[col], col)
        return value

    def result(self, state, action):
        """ Apply the chosen action """
        return action


class MagicSquaresProblem(Problem):
    """ Magic Square Problem """

    def __init__(self, N, temperature=1000):
        """
            N: matrix NxN
            magic_const: N[(N^2+1)/2]
            initial: random generated matrix
        """
        super(self.__class__, self).__init__(temperature)
        self.N = N
        self.name = 'Magic Square'
        self.magic_const = int(N * ((N**2 + 1) / 2))
        self.initial = np.matrix(np.random.choice(
            range(1, self.N**2 + 1),
            (self.N, self.N),
            replace=False))

    def __check_repetition(self, state):
        """ Check that the matrix contains all different values """
        return len(np.unique(state.tolist())) != self.N**2

    def __best_value(self, rcd, value):
        """ Return the best value to be swapped """
        return abs(value - self.magic_const), random.choice([x for x in rcd if x != abs(value - self.magic_const)])

    def __swap_values(self, state, new, old):
        """ Swap two chosen value in the matrix """
        swap = state.copy()
        if old is None:
            return []
        a = tuple(np.argwhere(swap == new).tolist()[0])
        b = tuple(np.argwhere(swap == old).tolist()[0])
        swap[a[0], a[1]], swap[b[0], b[1]] = swap[b[0], b[1]], swap[a[0], a[1]]
        return [swap]

    def actions(self, state):
        """ Return a new state with two random values swapped """
        old = None
        for x in range(self.N):
            if np.sum(state[x]) != self.magic_const:
                old = random.choice(list(state[x].A1))
            if np.sum(state.T[x]) != self.magic_const:
                old = random.choice(list(state.T[x].A1))    
        if np.sum(state.diagonal()) != self.magic_const:
            old = random.choice(list(state.diagonal().A1))
        if np.sum(np.fliplr(state).diagonal()) != self.magic_const:
            old = random.choice(list(np.fliplr(state).diagonal().A1))
        new = random.choice([x for x in state.A1 if x != old])
        return self.__swap_values(state, new, old)

    def value(self, state):
        """
            Calculate the variance of the distances from the magic constant
        """
        sums = list(np.sum(state.A, axis=0)) + list(np.sum(state.A, axis=1))
        sums.append(np.sum(state.diagonal()))
        sums.append(np.sum(np.fliplr(state).diagonal()))
        return np.sum([abs(s - self.magic_const) for s in sums]) / len(sums)

    def result(self, state, action):
        """ Return the chosen action """
        return action


class TravellingSalesmanProblem(Problem):
    """ Travelling Salesman Problem """

    def __init__(self, cities, temperature=1000):
        super(self.__class__, self).__init__(temperature)
        self.cities = cities
        self.name = 'Travelling Salesman'
        self.initial = list(self.cities.keys())
        random.shuffle(self.initial)
        self.dist_matrix = self.__cities_distances(self.cities)

    def __calculate_distance(self, a, b):
        """ Calculates distance between two latitude-longitude coordinates. """
        earth_radius = 6378
        lat1, lon1 = math.radians(a[0]), math.radians(a[1])
        lat2, lon2 = math.radians(b[0]), math.radians(b[1])
        return math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)) * earth_radius

    def __cities_distances(self, cities):
        """ Create a dictionary with all the distances from every city """
        distances = {}
        for ka, va in self.cities.items():
            distances[ka] = {}
            for kb, vb in self.cities.items():
                if kb == ka:
                    distances[ka][kb] = 0.0
                else:
                    distances[ka][kb] = self.__calculate_distance(va, vb)
        return distances

    def actions(self, state):
        """Swaps two cities in the route."""
        next_state = state[:]
        a = random.randint(0, len(state) - 1)
        b = random.randint(0, len(state) - 1)
        next_state[a], next_state[b] = next_state[b], next_state[a]
        return [next_state]

    def value(self, state):
        """Calculates the length of the route."""
        return round(sum([self.dist_matrix[state[i - 1]][state[i]] for i in range(1, len(state))])
                     + self.dist_matrix[state[0]][state[len(state) - 1]], 4)

    def result(self, state, action):
        """ Return the chosen action """
        return action
