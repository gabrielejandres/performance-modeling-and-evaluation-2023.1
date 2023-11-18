class EpidemyTree:
    def __init__(self, generations):
        self.generations = generations

    def get_total_generations(self):
        return len(self.generations)

    def get_total_offspring(self):
        return sum(
            [generation.get_total_offspring() for generation in self.generations]
        )

    def get_total_population(self):
        return sum([generation.population for generation in self.generations])

    def is_tree_extinct(self):
        return self.generations[-1].get_total_offspring() == 0

    def get_max_node_offspring(self):
        return max(
            [generation.get_max_node_offspring() for generation in self.generations]
        )

    def get_total_elapsed_time(self):
        return sum([generation.get_total_time() for generation in self.generations])
    
    def get_nodes_offspring_distribution(self):
        distribution = [0] * (self.get_max_node_offspring() + 1)
        for generation in self.generations:
            for distribution_index, node_offspring in enumerate(generation.get_nodes_offspring_density()):
                distribution[distribution_index] += node_offspring

        return distribution

    def __str__(self):
        text = ""
        text += "Árvores extinstas: " + str(self.is_tree_extinct()) + "\n"
        text += "Total de gerações: " + str(self.get_total_generations()) + "\n"
        text += "Total da população: " + str(self.get_total_population()) + "\n"
        text += "Total de filhos: " + str(self.get_total_offspring()) + "\n"
        text += (
            "Filhos da raiz: " + str(self.generations[0].get_total_offspring()) + "\n"
        )
        return text
