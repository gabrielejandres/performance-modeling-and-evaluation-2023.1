import sys
from epidemy import simulate

def generate_metrics(mu, Lambda, is_deterministic, size_initial_population, max_generations, total_runs):
    simulations = []
    for i in range(total_runs):
        simulations.append(
            simulate(mu, Lambda, is_deterministic, size_initial_population, max_generations)
        )
    print(f"Fração de árvores finitas (epidemias extintas): {finite_tree_fraction(simulations)}")
    print(f"Distribuição dos graus de saída (Offspring distribution): {get_offspring_distribution(simulations)}")
    print(f"Média do grau de saída da raiz: {get_mean_root_offspring(simulations)}")
    print(f"Média do grau de saída máximo: {get_mean_max_offspring(simulations)}")
    print(f"Média de altura da árvore: {get_mean_tree_height(simulations)}")
    print(f"Média de altura dos nós: {get_mean_node_height(simulations)}")
    print(f"Média da duração do período ocupado: {get_mean_busy_period_duration(simulations)}")
    print(f"Média do número de clientes atendidos por período ocupado (antes da extinção): TO-DO")


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
    for tree in simulations:
        total_max_offspring += tree.get_max_node_offspring()

    return total_max_offspring / len(simulations)


def get_mean_tree_height(simulations):
    total_tree_height = 0
    total_extinct_trees = 0
    for tree in simulations:
        if not tree.is_tree_extinct():
            continue
        total_extinct_trees += 1
        total_tree_height += tree.get_total_generations()

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
                generation_height + 1
            )
        total_node_height_per_tree /= tree.get_total_population()
        total_node_height += total_node_height_per_tree

    if total_extinct_trees == 0:
        return None
    return total_node_height / total_extinct_trees


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
