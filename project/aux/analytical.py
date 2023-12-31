"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Cálculo de métricas analíticas para o modelo M/M/1, para a ruína do apostador e processos de ramificação
"""

import math

# Lei de little para calcular a média de clientes no sistema
def get_mean_customers_on_system_by_littles_law(Lambda, mu):
    rho = Lambda/mu
    return rho / (1 - rho)


# Média do tempo de resposta = tempo de espera + tempo de atendimento (tempo total que o cliente gasta no sistema)
def get_mean_response_time_by_mm1_formula(Lambda, mu):
    return 1 / (mu - Lambda)


# Média de tempo de espera pela fórmula da M/M/1 (tempo gasto somente na fila de espera)
def get_mean_waiting_time_by_mm1_formula(Lambda, mu):
    rho = Lambda/mu
    return rho / (mu - Lambda)


# Média de períodos ocupados pela fórmula da M/M/1
# def get_mean_busy_times_by_mm1_formula(Lambda, mu):
#     return 1 / (mu - Lambda)
  

# Distribuição estacionária em i (probabilidade de estar em i) pela fórmula da M/M/1
def get_frac_times_on_i_by_mm1_formula(Lambda, mu, i):
    rho = Lambda/mu
    return (1 - rho) * pow(rho, i)


# Probabilidade de ser absorvido em 0 começando no estado k em uma fila FINITA
def get_prob_reach_zero_by_gamblers_ruin_finite(Lambda, mu, n, k):
    p = Lambda / (Lambda + mu)
    q = 1 - p

    if p == q:
        return 1 - k / n
        
    return 1 - (1 - pow(q/p, k))/(1 - pow(q/p, n))


# Probabilidade de alacançar o estado 0 em uma fila INFINITA
def get_prob_reach_zero_by_gamblers_ruin(Lambda, mu, k):
    if mu < Lambda:
        return pow(mu/Lambda, k)
    else:
        return 1.0

# Fração de árvores finitas (epidemias extintas) utilizando a transformada G(s) com tempo de serviço exponencial
def finite_tree_fraction_analytical(Lambda, mu):
    if mu < Lambda:
        return mu/Lambda
    else:
        return 1.0

# Progenia total de um processo de ramificação 
def total_progeny(mean_offspring_generation, size_initial_population):
    if mean_offspring_generation >= 1:
        return math.inf
    return abs(size_initial_population / (1 - mean_offspring_generation))

# Média de filhos em uma geração é a média de clientes que chegam durante um serviço. 
# Se lambda < mu, o serviço é mais rápido, então a média de clientes que chegam durante um serviço é 0 pois os clientes chegam mais lentamente.
def get_offspring_mean(Lambda, mu):
    if Lambda >= mu:
        return Lambda/mu
    return 0