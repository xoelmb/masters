import random
import math
import copy
import time


def init_pop(size):
    pop = []
    for i in range(size):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        new_plant = [x, y, eval_fitness(x, y)]
        pop.append(new_plant)
    pop.sort(key=lambda x: x[2])
    return pop


def eval_fitness(x, y):
    return x * math.sin(4 * x) + 1.1 * y * math.sin(2 * y)


def disperse(x, y, omega):
    new_x, new_y = -5, -5
    while new_x <= 0 or new_x >= 10:
        new_x = random.gauss(x, omega)
    while new_y <= 0 or new_y >= 10:
        new_y = random.gauss(y, omega)
    return [new_x, new_y, eval_fitness(new_x, new_y)]


def reproduce(pop, news, omega):
    new_pop = copy.deepcopy(pop)
    all_fitness = []
    for plant in new_pop:
        plant[2] = plant[2] * -1
        all_fitness.append(plant[2])
    ad_all_fitness = []
    for plant in new_pop:
        plant[2] = plant[2] - min(all_fitness)
        ad_all_fitness.append(plant[2])
    for plant in random.choices(pop, weights=ad_all_fitness, k=news):
        pop.append(disperse(plant[0], plant[1], omega))
    pop.sort(key=lambda x: x[2])


def sum_fitness(pop):
    total = 0
    for plant in pop:
        total += plant[2]
    return total


def summary_print(pop, n):
    print("Generation:", n)
    print('\tPopulation size', len(pop))
    print('\tBest plant', pop[0])
    print('\tGlobal fitness:', sum_fitness(pop))
    print('')


def main(pi=10, pmax=500, new_seeds=50, omega=1, niter=500):
    population = init_pop(pi)
    summary_print(population, 0)
    for j in range(1, niter):
        reproduce(population, new_seeds, omega)
        if len(population) > pmax:
            population = population[:pmax]
        summary_print(population, j)


t0 = time.time()
main()
print(time.time() - t0)
