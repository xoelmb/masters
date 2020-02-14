import random
import time
import numpy as np
import matplotlib.pyplot as plt
from progress.bar import Bar
import cython
import math
from libc.math cimport sin, sqrt
from cython.parallel import parallel, prange 

def eval_fitness(x, y):
    return x * math.sin(4 * x) + 1.1 * y * math.sin(2 * y)


class InvWeed:
    def __init__(self, initial_size=75, pmax=1000, new_seeds=200, niter=1000, delta=1e-6, max_rep=10):
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
        sd_iterator = iter(list(np.linspace(0.5, 2, seeds_gen)))
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


def grid_search(function, pars):
    print("started")
    cdef int npars
    npars = 1
    for x in pars.values():
        npars *= len(x)
    cdef int[::1] par_list = []
    
    for pi in pars['initial_size']:
        for pmax in pars['pmax']:
            for new_seeds in pars['new_seeds']:
                for niter in pars['niter']:
                    for delta in pars['delta']:
                        for max_rep in pars['max_rep']:
                            par_list.append([pi, pmax, new_seeds, niter, delta, max_rep])
    
    cdef int[::1] models  = np.empty( npars,   dtype= float )
    results = []
    with nogil, parallel():
        for i in prange(npars):
            models[i]=function(par_list[i][0], par_list[i][1], par_list[i][2], par_list[i][3], par_list[i][4], par_list[i][5])
    for model in models:
        results.append([model.records[-1], model.runtime, model.niters, model.parameters])
    return results


# parameters = {
#     'initial_size': [5, 10, 100, 1000],
#     'pmax': [100, 500, 1000, 5000],
#     'new_seeds': [20, 50, 100, 500],
#     'niter': [20, 100, 500, 10000],
#     'delta': [1e-3, 1e-6, 1e-9],
#     'max_rep': [5, 10, 20, 50]
# }
# my_model = InvWeed()
# print(best_parameters)
# for r in best_parameters:
#     if r[0] < -18.0:
#         print(r)
#         print()
#         besties.append(r[0])

t0 = time.time()

parameters = {
    'initial_size': [5, 100],
    'pmax': [200, 500, 1000],
    'new_seeds': [20, 100],
    'niter': [100, 1000],
    'delta': [1e-6, 1e-9],
    'max_rep': [1, 10]
}

best_parameters = grid_search(InvWeed, parameters)
best_parameters.sort(key=lambda x: x[1])
best_runtime = best_parameters[0][1]
best_parameters.sort(key=lambda x: x[0])
best_fitness = best_parameters[0][0]

for c in best_parameters:
    c.append(sqrt((c[0] - best_fitness) ** 2 + (c[1] - best_runtime) ** 2))
    
with open('results.txt', 'wt') as file:
    for c in sorted(best_parameters, key=lambda x: x[-1]):
        file.write(str(c))
        file.write("\n")


print(time.time() - t0)
