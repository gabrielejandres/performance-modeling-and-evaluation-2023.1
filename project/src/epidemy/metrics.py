import sys
import math
import numpy as np
from epidemy import simulate

sys.path.append('../../')
from aux.graphics import *
from aux.analytical import *

def generate_metrics(mu, Lambda, is_deterministic, size_initial_population, max_generations, total_runs):
    simulations = []
    for _ in range(total_runs):
        simulations.append(
            simulate(mu, Lambda, is_deterministic, size_initial_population, max_generations)
        )
    print(f"λ = {Lambda} & μ = {mu}")
    print("\n-- Fração de árvores finitas (epidemias extintas) --")
    print("Simulação: ", finite_tree_fraction(simulations))
    print(f"Intervalo de confiança correspondente -> {get_confidence_interval([tree.is_tree_extinct() for tree in simulations])}")
    print(f"Analítico (s = G(s)): ", finite_tree_fraction_analytical(Lambda, mu))

    print("\n-- Distribuição dos graus de saída (offspring distribution) --")
    print("Simulação: ", get_offspring_distribution(simulations))
    print(f"CDF distribuição dos graus de saída (offspring distribution): {plot_cdf_offspring_distribution(simulations, (max(get_offspring_distribution(simulations).keys()) + 1))}")

    print("\n-- Média do grau de saída da raiz --")
    print("Simulação: ", get_mean_root_offspring(simulations))
    print(f"Intervalo de confiança correspondente -> {get_confidence_interval([tree.generations[0].get_total_offspring() for tree in simulations])}")

    print("\n-- Média do grau de saída máximo --")
    print("Simulação: ", get_mean_max_offspring(simulations))
    print(f"Intervalo de confiança correspondente -> {get_confidence_interval([tree.get_max_node_offspring() for tree in simulations if tree.is_tree_extinct()])}")

    print("\n-- Média de altura da árvore --")
    print("Simulação: ", get_mean_tree_height(simulations))
    print(f"Intervalo de confiança correspondente -> {get_confidence_interval([tree.get_total_generations() - 1 for tree in simulations if tree.is_tree_extinct()])}")

    print("\n-- Média de altura dos nós --")
    print("Simulação: ", get_mean_node_height(simulations))
    print(f"Intervalo de confiança correspondente -> {get_confidence_interval(get_mean_node_height_per_round(simulations))}")

    print("\n-- Média da duração do período ocupado --")
    print("Simulação: ", get_mean_busy_period_duration(simulations))
    print(f"Intervalo de confiança correspondente -> {get_confidence_interval(get_mean_busy_period_duration_per_round(simulations))}")
    if Lambda <= mu:
        print(f"Analítico (M/M/1): ", get_mean_response_time_by_mm1_formula(Lambda, mu))

    mean_total_progeny = get_mean_total_progeny(simulations)
    print("\n-- Média do número de clientes atendidos por período ocupado (antes da extinção) --")
    print("Simulação: ", mean_total_progeny)
    if mean_total_progeny != math.inf:
        print(f"Intervalo de confiança correspondente -> {get_confidence_interval([tree.get_total_offspring() for tree in simulations if tree.is_tree_extinct()])}")
    print(f"Analítico (progenia total): ", total_progeny(get_offspring_mean(Lambda, mu), size_initial_population))

def finite_tree_fraction(simulations):
    total_extinct_simulations = 0
    for tree in simulations:
        if tree.is_tree_extinct():
            total_extinct_simulations += 1

    return total_extinct_simulations / len(simulations)


def get_offspring_distribution(simulations):
    offspring_distribution = {}
    for tree in simulations:
        for generation in tree.generations:
            for node in generation.nodes:
                if node.offspring not in offspring_distribution:
                    offspring_distribution[node.offspring] = 0
                offspring_distribution[node.offspring] += 1

    total_offspring = sum(offspring_distribution.values())
    for key in offspring_distribution.keys():
        offspring_distribution[key] /= total_offspring

    offspring_distribution = dict(
        sorted(offspring_distribution.items(), key=lambda item: item[0])
    ) 
    return offspring_distribution 


def get_mean_root_offspring(simulations):
    total_root_offspring = 0
    for tree in simulations:
        total_root_offspring += tree.generations[0].get_total_offspring()

    return total_root_offspring / len(simulations)


def get_mean_max_offspring(simulations):
    total_max_offspring = 0
    total_extinct_trees = 0
    for tree in simulations:
        if not tree.is_tree_extinct():
            continue
        total_extinct_trees += 1
        total_max_offspring += tree.get_max_node_offspring()

    return total_max_offspring / total_extinct_trees


def get_mean_tree_height(simulations):
    total_tree_height = 0
    total_extinct_trees = 0
    for tree in simulations:
        if not tree.is_tree_extinct():
            continue
        total_extinct_trees += 1
        total_tree_height += tree.get_total_generations() - 1
    if total_extinct_trees == 0:
        return None
    return total_tree_height / total_extinct_trees


def get_mean_node_height(simulations):
    total_node_height = 0
    total_extinct_trees = 0
    for tree in simulations:
        if not tree.is_tree_extinct():
            continue
        total_node_height_per_tree = 0
        total_extinct_trees += 1
        for generation_height, generation in enumerate(tree.generations):
            total_node_height_per_tree += generation.population * (
                generation_height #+ 1
            )
        total_node_height_per_tree /= tree.get_total_population()
        total_node_height += total_node_height_per_tree

    if total_extinct_trees == 0:
        return None
    return total_node_height / total_extinct_trees

def get_mean_node_height_per_round(simulations):
    total_extinct_trees = 0
    mean_node_height_per_round = []

    for tree in simulations:
        if not tree.is_tree_extinct():
            continue

        total_node_height_per_tree = 0
        total_extinct_trees += 1
        for generation_height, generation in enumerate(tree.generations):
            total_node_height_per_tree += generation.population * (
                generation_height #+ 1
            )
        total_node_height_per_tree /= tree.get_total_population()

        mean_node_height_per_round.append(total_node_height_per_tree)

    if total_extinct_trees == 0:
        return 0
    
    return mean_node_height_per_round


def get_mean_busy_period_duration(simulations):
    total_busy_period_duration = 0
    total_extinct_trees = 0
    for tree in simulations:
        if not tree.is_tree_extinct():
            continue
        total_extinct_trees += 1
        total_busy_period_duration += tree.get_total_elapsed_time()

    if total_extinct_trees == 0:
        return None
    return total_busy_period_duration / total_extinct_trees

def get_mean_busy_period_duration_per_round(simulations):
    mean_busy_period_duration_per_round = []
    total_extinct_trees = 0
    for tree in simulations:
        if not tree.is_tree_extinct():
            continue
        total_extinct_trees += 1
        mean_busy_period_duration_per_round.append(tree.get_total_elapsed_time())
        
    if total_extinct_trees == 0:
        return None
    
    return mean_busy_period_duration_per_round

def get_mean_total_progeny(simulations):
    total_progeny = 0
    total_extinct_trees = 0
    for tree in simulations:
        if not tree.is_tree_extinct():
            return math.inf
        total_extinct_trees += 1
        total_progeny += tree.get_total_offspring()

    return total_progeny / total_extinct_trees

def get_mean(mean_per_round):
    """ Obtem a media de uma distribuição """
    return np.mean(mean_per_round)


def get_variance(mean_per_round, mean_on_system):
    """ Obtem a variancia de uma distribuição """
    customers_on_system_variance = 0
    for mean in mean_per_round:
        customers_on_system_variance += pow(mean - mean_on_system, 2) / max(len(mean_per_round) - 1, 1)
    return customers_on_system_variance

# def get_confidence_interval(standard_deviation, sample_mean, sample_size):
#     """ Calcula o intervalo de confiança """
#     lowest_point = sample_mean - 1.96 * (standard_deviation / np.sqrt(sample_size))
#     highest_point = sample_mean + 1.96 * (standard_deviation / np.sqrt(sample_size))
    
#     return (lowest_point, highest_point)

def get_confidence_interval(mean_per_round):
    """ Calcula o intervalo de confiança """
    mean_on_system = get_mean(mean_per_round)
    standard_deviation = np.sqrt(get_variance(mean_per_round, mean_on_system))
    lowest_point = mean_on_system - 1.96 * (standard_deviation / np.sqrt(len(mean_per_round)))
    highest_point = mean_on_system + 1.96 * (standard_deviation / np.sqrt(len(mean_per_round)))
    
    return (lowest_point, highest_point)

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            "Usage: python3 metrics.py <max_generations> <mu> <lambda> <is_deterministic> <size_initial_population> <total_runs>"
        )
        exit(1)

    max_generations = int(sys.argv[1])
    mu = float(sys.argv[2])
    Lambda = float(sys.argv[3])
    is_deterministic = True if sys.argv[4] == "1" else False
    size_initial_population = int(sys.argv[5])
    total_runs = int(sys.argv[6])

    generate_metrics(mu, Lambda, is_deterministic, size_initial_population, max_generations, total_runs)
