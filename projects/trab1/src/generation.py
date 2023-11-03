class Generation:
  def __init__(self, population = 0):
    self.population = population
    self.offspring_by_customer = []

  @staticmethod
  def get_offspring_by_customer(self, mu, Lambda):
    return 1
  
  def get_next_generation(self, mu, Lambda):
    return sum(self.offspring_by_customer)
