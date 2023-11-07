import numpy as np
from generation import Generation
import sys
from epidemy_metrics import generate_metrics
from epidemy_tree import EpidemyTree


def generate_offspring(mu, lamb, is_deterministic):
    if is_deterministic:
        service_time = mu
    else:
        service_time = np.random.exponential(1 / mu)
    total_arrivals = 0
    elapsed_time = 0
    while elapsed_time < service_time:
        elapsed_time += np.random.exponential(1 / lamb)
        total_arrivals += 1
    return service_time, total_arrivals - 1


def simulate(mu, lamb, is_deterministic, initial_population, max_generations):
    generations = []
    last_offspring = initial_population
    while len(generations) < max_generations and last_offspring > 0:
        current_generation = Generation(last_offspring)
        for i in range(current_generation.population):
            elapsed_time, offspring = generate_offspring(mu, lamb, is_deterministic)
            current_generation.finish_node(i, elapsed_time, offspring)
        generations.append(current_generation)
        last_offspring = current_generation.get_total_offspring()

    return EpidemyTree(generations)


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            "Usage: python3 epidemy.py <max_generations> <mu> <lambda> <is_deterministic> <initial_population> <total_runs>"
        )
        exit(1)
    max_generations = int(sys.argv[1])
    mu = float(sys.argv[2])
    lamb = float(sys.argv[3])
    is_deterministic = True if sys.argv[4] == "1" else False
    initial_population = int(sys.argv[5])
    total_runs = int(sys.argv[6])

    simulations = []
    for i in range(total_runs):
        simulations.append(
            simulate(mu, lamb, is_deterministic, initial_population, max_generations)
        )

    generate_metrics(simulations)
