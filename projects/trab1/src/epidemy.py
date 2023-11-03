import numpy as np
from generation import Generation

def generate_offspring(mu, lamb):
    p = mu / (mu + lamb)
    return np.random.geometric(p) - 1

def simulate(mu, lamb, initial_population = 1, max_generations = 10):
    generations = [Generation(initial_population)]
    while generations[-1].population > 0 and len(generations) < max_generations:
        current_generation = generations[-1]
        for i in range(current_generation.population):
            offspring = generate_offspring(mu, lamb)
            current_generation.add_offspring(offspring)
        total_offspring = current_generation.get_total_offspring()
        next_generation = Generation(total_offspring)
        generations.append(next_generation)
    for generation in generations:
        print(generation)

if __name__ == '__main__':
    simulate(1,2)
