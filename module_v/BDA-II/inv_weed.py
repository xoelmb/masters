import random
import math
import copy
import time
from 


def init_pop(size):
    pop = []
    for i in range(size):
        new_plant = [random.uniform(0, 10), random.uniform(0, 10)]
        pop.append(new_plant)
    return pop


def eval_fitness(x, y):
    return x * math.sin(4 * x) + 1.1 * y * math.sin(2 * y)


def disperse(x, y, omega):
    new_x = max(0, min(10, random.gauss(x, omega)))
    new_y = max(0, min(10, random.gauss(y, omega)))
    # new_x, new_y = -5, -5
    # while new_x < 0 or new_x > 10:
    #     new_x = random.gauss(x, omega)
    # while new_y < 0 or new_y > 10:
    #     new_y = random.gauss(y, omega)    
    return [new_x, new_y, eval_fitness(new_x, new_y)]


def reproduce(pop, news, omega):
    new_pop = copy.deepcopy(pop)
    all_fitness = []
    for plant in new_pop:
        plant[2] = plant[2] * -1
        all_fitness.append(plant[2])
    # print(all_fitness)
    ad_all_fitness = []
    for plant in new_pop:
        plant[2] = plant[2] - min(all_fitness)
        ad_all_fitness.append(plant[2])
    ad_all_fitness = sum(ad_all_fitness)
    # print(ad_all_fitness)
    for i in range(len(new_pop)):
        # print(pop[i][2])
        # print(round(new_pop[i][2]/ad_all_fitness*news))
        n_seed = round(new_pop[i][2] / ad_all_fitness * news)
        for _ in range(n_seed):
            pop.append(disperse(pop[i][0], pop[i][1], omega))

        # pop.append(disperse(pop[i][0], pop[i][1], round(new_pop[i][3]/sum(all_fitness))))


def sum_fitness(pop):
    total = 0
    for plant in pop:
        total += plant[2]
    # print("")
    return total


def main(pi, pmax, new_seeds, omega, niter):
    j = 0
    print("Generation:", j)
    population = init_pop(pi)
    print(len(population))
    print(population)
    for plant in population:
        plant.append(eval_fitness(plant[0], plant[1]))
    # print("")
    new_fitness = sum_fitness(population)
    print(new_fitness)
    population.sort(key=lambda x: x[2])
    for _ in range(niter):
        reproduce(population, new_seeds, omega)
        population.sort(key=lambda x: x[2])
        if len(population) > pmax:
            population = population[:pmax]
        # print("")
        j += 1
        print("Generation:", j)
        print(len(population))
        print(population)
        print(sum_fitness(population))

    #     reproduce(population)
    #     if len(population) > pmax:
    #         sort_pop(population)
    #         prune_pop(pmax)

t0 = time.time()
main(5, 100, 50, 1, 400)
print(time.time()-t0)