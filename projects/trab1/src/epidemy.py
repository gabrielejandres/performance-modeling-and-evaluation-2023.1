"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação de Fila M/M/1
"""

import numpy as np
from generation import Generation

INITIAL_POPULATION = 1


def simulate():
  generations = []
  generations.append(Generation(INITIAL_POPULATION))

  while generations[-1].population > 0:
    for i in range(generations[-1].population):
      generations[-1].offspring_by_customer.append(Generation.get_offspring_by_customer(1, 1))
      generations.append()

      
