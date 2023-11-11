"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Plotagem dos gráficos
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_graphic(x, y, title, xlabel, ylabel, discrete = False):
  if discrete:
    plt.xticks(range(0, len(y)))
    plt.bar(x, y)
  else:
    plt.plot(x, y)
    
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)
  plt.show()

def calculate_cdf(density):
  pairs = list(density.items())

  # Sort pairs
  pairs.sort(key=lambda pair: pair[0])

  # Prepara eixo X
  x = np.array([param for param, _ in pairs])

  # Prepara eixo Y
  y = np.array([density for _, density in pairs])
  y = np.cumsum(y)

  # Normaliza
  y = y / y[-1]

  return x, y

def plot_cdf_waiting_time(waiting_density, Lambda, mu):
  x, y = calculate_cdf(waiting_density)

  # Plota CDF
  plot_graphic(x, y, "CDF do tempo de espera λ = {} μ = {}".format(Lambda, mu), "Tempo de espera", "Probabilidade acumulada")

def plot_cdf_number_clients(number_clients_density, Lambda, mu):
  x, y = calculate_cdf(number_clients_density)

  # Plota CDF
  plot_graphic(x, y, "CDF do número de clientes no sistema λ = {} μ = {}".format(Lambda, mu), "Número de clientes no sistema", "Probabilidade acumulada", discrete=True)