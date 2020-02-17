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
    def __init__(self, initial_size=5, pmax=200, new_seeds=100, niter=100, delta=1e-6, max_rep=10, verbose=False):
        self.runtime = time.time()
        self.parameters = [initial_size, pmax, new_seeds, niter, delta, max_rep]
        self.niters = 0
        self.pop = []
        for i in range(initial_size):
            x = random.uniform(0, 10)
            y = random.uniform(0, 10)
            new_plant = [x, y, eval_fitness(x, y)]
            self.pop.append(new_plant)
        self.pop.sort(key=lambda x: x[2])
        self.records = [self.pop[0][2]]
        if verbose:
            self.summary_print(0)
        self.iterate(pmax, new_seeds, niter, delta, max_rep, verbose)
        self.best_plant = [self.pop[0][0], self.pop[0][1]]

    def iterate(self, pmax, new_seeds, niter, delta, max_rep, v):
        self.runtime = time.time()
        # self.summary_print(0)
        counter = 0
        for self.niters in range(1, niter):
            self.reproduce(new_seeds)
            if len(self.pop) > pmax:
                self.pop = self.pop[:pmax]
            self.records.append(self.pop[0][2])
            if v:
                self.summary_print(self.niters)
            if self.records[self.niters - 1] - self.records[self.niters] < delta:
                counter += 1
                if counter > max_rep:
                    break
            else:
                counter = 0
        self.runtime = time.time() - self.runtime

    def reproduce(self, seeds_gen):
        all_fitness = [x[2] * -1 + self.pop[-1][2] for x in self.pop]
        sd_iterator = iter(list(np.linspace(0.4, 2, seeds_gen)))
        for plant in sorted(random.choices(self.pop, weights=[x / max(all_fitness) for x in all_fitness], k=seeds_gen),
                            key=lambda x: x[2]):
            self.pop.append(self.disperse(plant[0], plant[1], next(sd_iterator)))
        self.pop.sort(key=lambda x: x[2])

    def disperse(self, x, y, omega):
        new_x = random.gauss(x, omega)
        new_y = random.gauss(y, omega)
        while new_x <= 0 or new_x >= 10:
            new_x = random.gauss(x, omega)
        while new_y <= 0 or new_y >= 10:
            new_y = random.gauss(y, omega)
        return [new_x, new_y, eval_fitness(new_x, new_y)]

    def summary_print(self, n):
        print("Generation:", n, '\n\tPopulation size', len(self.pop), '\n\tBest plant', self.pop[0], "\n")

    def plot(self):
        plt.plot(self.records)
        plt.ylabel('Cost function')
        plt.xlabel('# Generation')
        plt.title(str(self.parameters))
        plt.show()


class GridSearch:
    def __init__(self, function, pars, reps=3):
        print('Looking for best parameters:')
        h = 1
        for x in pars.values():
            h *= len(x)
        print('\t· '+str(h), 'combinations being tested.\n\t· Results averaged using', reps, 'repetitions.')
        self.test_list = self.get_combinations(pars, reps)
        pool = multiprocessing.Pool(processes=8)
        self.models = [pool.apply_async(function, args=(x[0], x[1], x[2], x[3], x[4], x[5],)) for x in self.test_list]
        self.results = self.extract_results(self.models)
        self.best_fitness = min([x[0] for x in self.results])
        self.best_runtime = min([x[1] for x in self.results])
        self.compute_distance()
        self.write_results()
        self.best_pars = self.results[0][-2]

    def get_combinations(self, pars, reps):
        par_list = []
        for pi in pars['initial_size']:
            for pmax in pars['pmax']:
                for new_seeds in pars['new_seeds']:
                    for niter in pars['niter']:
                        for delta in pars['delta']:
                            for max_rep in pars['max_rep']:
                                for _ in range(reps):
                                    par_list.append([pi, pmax, new_seeds, niter, delta, max_rep])
        return par_list

    def extract_results(self, models):
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
                rec += r[0] / len(dict_help[k])
                runt += r[1] / len(dict_help[k])
                nit += r[2] / len(dict_help[k])
            results.append([rec, runt, nit, list(k)])
        return results

    def compute_distance(self):
        for c in self.results:
            c.append(math.sqrt((c[0] - self.best_fitness) ** 2 + (c[1] - self.best_runtime) ** 2))
        self.results.sort(key=lambda x: x[-1])

    def write_results(self):
        with open('results.txt', 'wt') as file:
            for c in self.results:
                file.write(str(c))
                file.write("\n")

    def plot(self):
        plt.scatter([x[1] for x in self.results], [x[0] for x in self.results])
        plt.xlabel('Runtime (s)')
        plt.ylabel('Fitness value')
        plt.title('Grid search results')
        plt.show()


def main(mode='short', nrep=3):
    t0 = time.time()
    if mode == 'short':
        parameters = {
            'initial_size': [5, 100],
            'pmax': [200, 500, 1000],
            'new_seeds': [20, 100],
            'niter': [100, 1000],
            'delta': [1e-6, 1e-9],
            'max_rep': [1, 10]
        }
    else:
        parameters = {
            'initial_size': [5, 10, 100, 1000],
            'pmax': [100, 200, 500, 1000],
            'new_seeds': [20, 100, 200],
            'niter': [20, 100, 500],
            'delta': [1e-6, 1e-9],
            'max_rep': [5, 10, 20]
        }
    search = GridSearch(InvWeed, parameters, nrep)
    search.plot()
    pars = search.best_pars
    print('Best parameters found:', pars, '\n\nBuilding model...')
    model = InvWeed(pars[0], pars[1], pars[2], pars[3], pars[4], pars[5], True)
    model.plot()
    print(time.time() - t0)


main()
