import math
import time
import numpy as np
import multiprocessing
import random
import matplotlib.pyplot as plt
from fitness_func import eval_fitness

# def eval_fitness(x, y):
#     return x * math.sin(4 * x) + 1.1 * y * math.sin(2 * y)


class InvWeed:
    def __init__(self, initial_size=5, pmax=200, new_seeds=100, niter=100, delta=1e-6, max_rep=10):
        self.pop = []
        for i in range(initial_size):
            x = random.uniform(0, 10)
            y = random.uniform(0, 10)
            new_plant = [x, y, eval_fitness(x, y)]
            self.pop.append(new_plant)
        self.pop.sort(key=lambda x: x[2])
        self.records = [self.pop[0][2]]
        self.runtime = time.time()
        self.niters = 0
        self.parameters = [initial_size, pmax, new_seeds, niter, delta, max_rep]
        self.iterate(pmax, new_seeds, niter, delta, max_rep)
        self.best_plant = [self.pop[0][0], self.pop[0][1]]

    def disperse(self, x, y, omega):
        new_x = random.gauss(x, omega)
        new_y = random.gauss(y, omega)
        while new_x <= 0 or new_x >= 10:
            new_x = random.gauss(x, omega)
        while new_y <= 0 or new_y >= 10:
            new_y = random.gauss(y, omega)
        return [new_x, new_y, eval_fitness(new_x, new_y)]

    def reproduce(self, seeds_gen):
        all_fitness = [x[2] * -1 + self.pop[-1][2] for x in self.pop]
        sd_iterator = iter(list(np.linspace(0.4, 2, seeds_gen)))
        for plant in sorted(random.choices(self.pop, weights=[x / max(all_fitness) for x in all_fitness], k=seeds_gen),
                            key=lambda x: x[2]):
            self.pop.append(self.disperse(plant[0], plant[1], next(sd_iterator)))
        self.pop.sort(key=lambda x: x[2])

    def summary_print(self, n):
        print("Generation:", n, '\n\tPopulation size', len(self.pop), '\n\tBest plant', self.pop[0], "\n")

    def iterate(self, pmax, new_seeds, niter, delta, max_rep):
        self.runtime = time.time()
        # self.summary_print(0)
        counter = 0
        for self.niters in range(1, niter):
            self.reproduce(new_seeds)
            if len(self.pop) > pmax:
                self.pop = self.pop[:pmax]
            self.records.append(self.pop[0][2])
            # self.summary_print(self.niters)
            if self.records[self.niters - 1] - self.records[self.niters] < delta:
                counter += 1
                if counter > max_rep:
                    break
            else:
                counter = 0
        self.runtime = time.time() - self.runtime


def grid_search(function, pars, reps=3):
    print("started")
    h = 1
    for i in pars.values():
        h *= len(i)
    print(h, "combinations to test")
    pool = multiprocessing.Pool(processes=8)
    par_list = []
    for pi in pars['initial_size']:
        for pmax in pars['pmax']:
            for new_seeds in pars['new_seeds']:
                for niter in pars['niter']:
                    for delta in pars['delta']:
                        for max_rep in pars['max_rep']:
                            for _ in range(reps):
                                par_list.append([pi, pmax, new_seeds, niter, delta, max_rep])

    models = [pool.apply_async(function, args=(x[0], x[1], x[2], x[3], x[4], x[5],)) for x in par_list]
    results = []
    dict_help = {}
    for p in models:
        if not tuple(p.get().parameters) in dict_help.keys():
            dict_help[tuple(p.get().parameters)] = [[p.get().records[-1], p.get().runtime, p.get().niters]]
        else:
            dict_help[tuple(p.get().parameters)].append([p.get().records[-1], p.get().runtime, p.get().niters])
    for k in dict_help.keys():
        rec = 0
        runt = 0
        nit = 0
        for r in dict_help[k]:
            rec += r[0] / reps
            runt += r[1] / reps
            nit += r[2] / reps
        results.append([rec, runt, nit, list(k)])
    return results


t0 = time.time()

parameters_large = {
    'initial_size': [5, 10, 100, 1000],
    'pmax': [100, 500, 1000],
    'new_seeds': [20, 100, 200],
    'niter': [20, 100, 500, 1000],
    'delta': [1e-3, 1e-6, 1e-9],
    'max_rep': [5, 10, 20, 50]
}

parameters_short = {
    'initial_size': [5, 100],
    'pmax': [200, 500, 1000],
    'new_seeds': [20, 100],
    'niter': [100, 1000],
    'delta': [1e-6, 1e-9],
    'max_rep': [1, 10]
}

best_parameters = grid_search(InvWeed, parameters_short, 3)
best_fitness = min([x[0] for x in best_parameters])
best_runtime = min([x[1] for x in best_parameters])

for c in best_parameters:
    c.append(math.sqrt((c[0] - best_fitness) ** 2 + (c[1] - best_runtime) ** 2))

best_parameters.sort(key=lambda x: x[-1])

with open('results.txt', 'wt') as file:
    for c in best_parameters:
        file.write(str(c))
        file.write("\n")


plt.scatter([x[1] for x in best_parameters], [x[0] for x in best_parameters])
plt.xlabel('Runtime (s)')
plt.ylabel('Fitness value')
plt.title('Grid search results')
plt.show()
print(time.time() - t0)
