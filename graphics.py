from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np


def plot_graphic(x, y, title, xlabel, ylabel):
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

  # Normaliza eixo Y entre 0 e 1
  scaler = preprocessing.MinMaxScaler()
  y = scaler.fit_transform(y.reshape(-1, 1))

  return x, y

def plot_cdf_waiting_time(waiting_density, Lambda, mu):
  x, y = calculate_cdf(waiting_density)

  # Plota CDF
  plot_graphic(x, y, "CDF do tempo de espera λ = {} μ = {}".format(Lambda, mu), "Tempo de espera", "Probabilidade acumulada")

def plot_cdf_number_clients(number_clients_density, Lambda, mu):
  x, y = calculate_cdf(number_clients_density)

  # Plota CDF
  plot_graphic(x, y, "CDF do número de clientes no sistema λ = {} μ = {}".format(Lambda, mu), "Número de clientes no sistema", "Probabilidade acumulada")