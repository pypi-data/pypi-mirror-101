import random
from collections import namedtuple

import numpy as np
from deap import base, algorithms
from deap import creator
from deap import tools

from pykopt.Strategy import Strategy
from pykopt.operator import crossover, selection
from pykopt.stats import Stats

from pykopt.util.logger import logger


class KerasOptimizer:
    hyperparam_list = []
    hyperparam_dict = {}
    hyperparam_index_dict = {}
    hyperparam_index_dict_reverse = {}

    def __init__(self, model, dataset=None, max_iteration=100, initial_population=20, layer_size=2, classes=2,
                 input_shape=(224, 224, 3), weights=None, crossover_prob=0.7, mutation_probability=0.01,
                 train_function=None,
                 strategy=Strategy.MAXIMIZE,
                 crossover_method=crossover.one_point,
                 selection_method=selection.tournament_selection):
        self.model = model
        self.initial_population = initial_population
        self.dataset = dataset
        self.layer_size = layer_size
        self.max_iteration = max_iteration
        self.classes = classes
        self.input_shape = input_shape
        self.weights = weights
        self.toolbox = base.Toolbox()
        self.crossover_prob = crossover_prob
        self.mutation_probability = mutation_probability
        self.train_function = train_function
        self.strategy = strategy
        self.crossover_method = crossover_method
        self.selection_method = selection_method

        self.__select_optimizer_strategy(strategy)

    def __select_optimizer_strategy(self, strategy):

        if "FitnessFunc" in globals():
            del globals()["FitnessFunc"]

        if strategy == Strategy.MAXIMIZE:
            creator.create("FitnessFunc", base.Fitness, weights=(1.0,))
        else:
            creator.create("FitnessFunc", base.Fitness, weights=(-1.0,))

        if "Individual" in globals():
            del globals()["Individual"]

        creator.create("Individual", list, fitness=creator.FitnessFunc)

    def __add_hyperparameter(self, hyperparam_name, hyperparam_value):
        self.toolbox.register(hyperparam_name, random.choice, hyperparam_value)
        self.hyperparam_list.append(getattr(self.toolbox, hyperparam_name))
        self.hyperparam_dict[hyperparam_name] = hyperparam_value;
        self.hyperparam_index_dict[hyperparam_name] = len(self.hyperparam_list) - 1
        self.hyperparam_index_dict_reverse[len(self.hyperparam_list) - 1] = self.hyperparam_list[
            len(self.hyperparam_list) - 1]

    def set_hyperparameters(self, **kwargs):
        for key, value in kwargs.items():
            self.__add_hyperparameter(key, value)

    def run(self):
        if self.hyperparam_list.__len__() == 0:
            raise Exception('Hyperparameters must be set!')

        self.toolbox.register("individual", tools.initCycle, creator.Individual, self.hyperparam_list)

        # define the population to be a list of individuals
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("mate", self.crossover_method)
        self.toolbox.register("mutate", self.mutate)
        self.toolbox.register("select", self.selection_method, tournsize=3)

        population_size = self.initial_population
        number_of_generations = 4

        pop = self.toolbox.population(n=population_size)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
        pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=self.crossover_prob, stats=stats,
                                       mutpb=self.mutation_probability, ngen=number_of_generations, halloffame=hof,
                                       verbose=True)

        best_parameters = hof[0]  # save the optimal set of parameters
        best_params_named = namedtuple("HyperParams", self.hyperparam_index_dict.keys())(
            *best_parameters)
        stats = Stats(best_params=best_params_named)
        return stats

    def evaluate(self, individual):
        logger.info('START---------------------------------------------')
        logger.info('Individual:', individual)
        batch_size = individual[self.hyperparam_index_dict['batch_size']]
        epochs = individual[self.hyperparam_index_dict['epochs']]
        learning_rate = individual[self.hyperparam_index_dict['learning_rate']]

        decay = 1e-6
        hyperparams_object = namedtuple("HyperParams", self.hyperparam_index_dict.keys())(
            *individual)
        score = self.train_function(self.model, hyperparams_object)
        logger.info('Score:', score, 'Individual:', individual)
        logger.info('END--------------------------------------')
        return score

    def mutate(self, individual):
        gene = random.randint(0, individual.__len__() - 1)
        individual[gene] = self.hyperparam_index_dict_reverse[gene]()
        return individual,

    def trainModel(self, hyperparams):
        pass
