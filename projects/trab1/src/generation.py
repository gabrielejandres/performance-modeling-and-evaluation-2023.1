class Generation:
    def __init__(self, population):
        self.population = population
        self.offspring = []

    def add_offspring(self, offspring_count):
        self.offspring.append(offspring_count)

    def get_total_offspring(self):
        return sum(self.offspring)

    def __str__(self):
        return f'Generation(mean={self.get_total_offspring()/self.population}, population={self.population}, offspring={self.offspring})'
