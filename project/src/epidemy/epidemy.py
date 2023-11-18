import numpy as np
from generation import Generation
from tree import EpidemyTree

MAX_GENERATION_SIZE = 100

def generate_offspring(mu, Lambda, is_deterministic):
    if is_deterministic:
        service_time = 1/mu
    else:
        service_time = np.random.exponential(1 / mu)
    total_arrivals = 0
    elapsed_time = 0
    while elapsed_time < service_time:
        elapsed_time += np.random.exponential(1 / Lambda)
        total_arrivals += 1
    return service_time, total_arrivals - 1


def simulate(mu, Lambda, is_deterministic, size_initial_population, max_generations):
    generations = []
    size_last_offspring = size_initial_population

    while len(generations) < max_generations and size_last_offspring > 0:
        if size_last_offspring > MAX_GENERATION_SIZE:
            break

        current_generation = Generation(size_last_offspring)

        for i in range(current_generation.population):
            elapsed_time, offspring = generate_offspring(mu, Lambda, is_deterministic)
            current_generation.finish_node(i, elapsed_time, offspring)
        generations.append(current_generation)
        size_last_offspring = current_generation.get_total_offspring()

    return EpidemyTree(generations)
