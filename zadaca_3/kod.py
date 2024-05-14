import random
import csv
import math
from podaci import had12_flows, els19_flows, tho_40_flows, had12_distances, els19_distances, tho_40_distances

# Define the MMAS algorithm
class MMAS:
    def __init__(self, instance, num_ants, alpha, rho, iterations, distances):
        self.instance = instance
        self.num_ants = num_ants
        self.alpha = alpha
        self.rho = rho
        self.iterations = iterations
        self.distances = distances
        self.num_facilities = len(instance)
        self.tau = [[1.0] * self.num_facilities for _ in range(self.num_facilities)]  # Initialize tau with 1.0
        self.best_solution = None
        self.best_fitness = float('inf')

    def run(self):
        with open('zadaca_3/solutions.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Iteration", "Best Solution", "Best Fitness"])
            for _ in range(self.iterations):
                ants = [Ant(self.instance, self.tau, self.alpha, self.distances) for _ in range(self.num_ants)]
                for ant in ants:
                    ant.construct_solution()
                    if ant.fitness < self.best_fitness:
                        self.best_solution = ant.solution
                        self.best_fitness = ant.fitness
                self.update_tau(ants[0])
                writer.writerow([_, self.best_solution, self.best_fitness])
                print("Iteration:", _, "Best Fitness:", self.best_fitness)

    def update_tau(self, ant):
        delta_tau = 1 / (ant.fitness * self.num_facilities)
        for i in range(self.num_facilities):
            for j in range(self.num_facilities):
                self.tau[i][j] = (1 - self.rho) * self.tau[i][j] + delta_tau

# Define the Ant class
class Ant:
    def __init__(self, instance, tau, alpha, distances):
        self.instance = instance
        self.tau = tau
        self.alpha = alpha
        self.distances = distances
        self.num_facilities = len(instance)
        self.solution = []
        self.fitness = float('inf')

    def construct_solution(self):
        unvisited = list(range(self.num_facilities))
        current = random.choice(unvisited)
        self.solution.append(current)
        unvisited.remove(current)

        while unvisited:
            probabilities = self.calculate_probabilities(current, unvisited)
            next_facility = self.choose_next_facility(unvisited, probabilities)
            self.solution.append(next_facility)
            unvisited.remove(next_facility)
            current = next_facility

        self.calculate_fitness()

    def calculate_probabilities(self, current, unvisited):
        total = sum((self.tau[current][j] ** self.alpha) for j in unvisited)
        probabilities = [(self.tau[current][j] ** self.alpha) / total for j in unvisited]
        return probabilities

    def choose_next_facility(self, unvisited, probabilities):
        return random.choices(unvisited, weights=probabilities)[0]

    def calculate_fitness(self):
        total = 0
        for i in range(self.num_facilities):
            for j in range(self.num_facilities):
                total += self.instance[i][j] * self.distances[self.solution[i]][self.solution[j]]
        self.fitness = total

# Define parameters
#num_ants = 12       #mijenja se ovisno o algoritmu
#num_ants = 19       #mijenja se ovisno o algoritmu
num_ants = 40       #mijenja se ovisno o algoritmu

alpha = 1.0
rho = 0.02
iterations = 1000

# odabire se instanca ovisno o algoritmu
#instance = had12_flows  # Change this to the desired instance
#instance = els19_flows  # Change this to the desired instance
instance = tho_40_flows  # Change this to the desired instance


# Create MMAS instance
#mmas = MMAS(instance, num_ants, alpha, rho, iterations, had12_distances)
#mmas = MMAS(instance, num_ants, alpha, rho, iterations, els19_distances)
mmas = MMAS(instance, num_ants, alpha, rho, iterations, tho_40_distances)


# Run MMAS algorithm
mmas.run()