from node import Node


class Generation:
    def __init__(self, population):
        self.population = population
        self.nodes = [Node() for _ in range(population)]

    def finish_node(self, node, elapsed_time, offspring):
        self.nodes[node].finish(elapsed_time, offspring)

    def get_total_offspring(self):
        return sum([node.offspring for node in self.nodes])

    def get_total_time(self):
        return sum([node.elapsed_time for node in self.nodes])

    def get_max_node_offspring(self):
        return max([node.offspring for node in self.nodes])
    
    def get_nodes_offspring_density(self):
        density = [0] * (self.get_max_node_offspring() + 1)
        for node in self.nodes:
            density[node.offspring] += 1

        return density

    def __str__(self):
        mean = (
            0 if self.population == 0 else self.get_total_offspring() / self.population
        )

        text = f"Generation(mean={mean}, elapsed_time={self.get_total_time()}, population={self.population})"
        return text
