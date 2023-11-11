class Node:
    def __init__(self):
        self.elapsed_time = 0
        self.offspring = 0

    def finish(self, elapsed_time, offspring):
        self.elapsed_time = elapsed_time
        self.offspring = offspring

    def __str__(self):
        return f"Node(elapsed_time={self.elapsed_time}, offspring={self.offspring})"
