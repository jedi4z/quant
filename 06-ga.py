import numpy as np
from utils.backtester import Backtester

class Individual():

  def __init__(self, n_genes, gene_ranges):
    self.genes = [np.random.randint(gene_ranges[i][0], gene_ranges[i][1]) for i in range(n_genes)]
    self.backtester = Backtester(
      initial_balance=1000,
      leverage=10,
      traling_stop_loss=True
      )
    

class Population():

  def __init__(self, generation_size, n_genes, gene_ranges, n_best, mutation_rate):
    self.population = [Individual(n_genes, gene_ranges) for _ in range(generation_size)]
    self.generation_size = generation_size
    self.n_genes = n_genes
    self.n_best = n_best
    self.mutation_rate = mutation_rate

  def selection(self):
    return sorted(
      self.population,
      key=lambda individual: individual.backtester.report(symbol='-', start='-', end='-')['fitness_function'],
      reverse=True
      )[0:self.n_best]
  
  def crossover(self):
    selected = self.selection()

    point = 0
    father = []

    
