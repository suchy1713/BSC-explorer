import numpy as np
import random
from sklearn.model_selection import cross_val_score

class Param():
    def __init__(self, array, is_integer=False):
        self.array = array
        self.is_integer = is_integer

    def get_param(self):
        return np.random.choice(self.array, 1)

class GeneTuning():
    def __init__(self, estimator, param_grid, population_size_init=4, parents_num=2, children_num=2, generations_num=4, cv=5):
        self.population = np.empty((population_size_init, len(param_grid)))
        self.param_grid = param_grid
        self.estimator = estimator
        self.cv = cv
        self.parents_num = parents_num
        self.children_num = children_num
        self.generations_num = generations_num

        for i in range(population_size_init):
            for j, param in zip(range(len(param_grid)), param_grid.values()):
                self.population[i, j] = param.get_param()

    def fit(self, X, y):
        self.best_score = 0
        self.best_params = {}
        for i in range(self.generations_num):
            print('Generation ', i+1, '/', self.generations_num, ':')
            self.train_population(X, y)
            self.select_new_parents()
            self.crossover()
            self.mutate()

    def train_population(self, X, y):
        params = {}
        self.scores = []
        for idx, person in enumerate(self.population):
            for i, param in zip(range(len(person)), self.param_grid.items()):
                if param[1].is_integer:
                    params[param[0]] = int(person[i])
                else:
                    params[param[0]] = person[i]

            print('Fitting model', idx+1, '/', len(self.population), ': ', params, ' : ', end='')
            self.estimator.set_params(**params)
            score = np.mean(cross_val_score(self.estimator, X, y, cv=self.cv))
            self.scores.append(score)

            print(score)

            if self.best_score < score:
                self.best_score = score
                self.best_params = params

    def select_new_parents(self):
        self.new_parents = np.empty((self.parents_num, len(self.param_grid)))

        for parent in range(self.parents_num):
            best_parent_no = np.argmax(self.scores)
            self.new_parents[parent, :] = self.population[best_parent_no, :]
            self.scores[best_parent_no] = -1

    def crossover(self):
        self.new_children = np.empty((self.children_num, len(self.param_grid)))

        for child in range(self.children_num):
            parent1_no = child%len(self.new_parents)
            parent2_no = (child+1)%len(self.new_parents)
            crossover_point = int(len(self.param_grid)/2)

            for i in range(len(self.param_grid)):
                if i < crossover_point:
                    self.new_children[child, i] = self.new_parents[parent1_no, i]
                else:
                    self.new_children[child, i] = self.new_parents[parent2_no, i]

    def mutate(self):
        for child in self.new_children:
            gene_to_mutate = np.random.randint(0, len(self.param_grid))

            child[gene_to_mutate] = list(self.param_grid.values())[gene_to_mutate].get_param()

        self.population = np.vstack((self.new_children, self.new_parents))