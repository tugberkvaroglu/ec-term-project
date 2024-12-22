import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# HYPER-PARAMETERS
n_pop = 30  # population size
p_x = 0.9  # crossover probability
p_m = 0.1  # mutation probability
ls = False  # apply local search (2-opt) after crossover
if ls:
    max_iter = 10  # we need fewer iterations with local search
else:
    max_iter = 500  # without local search, we need more iterations

# 2D Euclidean point class
class Point:
    def __init__(self, x, y, label):
        self.x = x  # X coordinate
        self.y = y  # Y coordinate
        self.label = label

    # Representation of the point object (for printing)
    def __repr__(self):
        return f"Point({self.x}, {self.y}, Label: {self.label})"

# Chromosome (Individual) class for the genetic algorithm
class Chromosome:
    def __init__(self, order=None):
        self.order = order  # candidate solution (permutation of indices)
        self.fitness = 0

    # Representation of the chromosome object (for printing)
    def __repr__(self):
        return f"Chromosome({self.order}, Fitness: {self.fitness})"

# Calculate the Euclidean distance between two points
def distance(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

# the higher the fitness, the better the solution
def calculate_fitness(chromosome):
    total_distance = 0
    for i in range(len(chromosome.order) - 1):
        point1 = coords[chromosome.order[i] - 1]
        point2 = coords[chromosome.order[i + 1] - 1]
        total_distance += distance(point1, point2)
    # Close the loop for TSP
    total_distance += distance(coords[chromosome.order[-1] - 1], coords[chromosome.order[0] - 1])
    chromosome.fitness = 1 / total_distance if total_distance != 0 else float('inf')

# 2-opt algorithm for local search (improves the solution by swapping two edges)
def two_opt(chromosome):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(chromosome.order) - 2):
            for j in range(i + 1, len(chromosome.order)):
                if j - i == 1:
                    continue
                new_order = chromosome.order.copy()
                new_order[i:j] = chromosome.order[j - 1:i - 1:-1]  # reverse the sub-route between i and j
                new_chromosome = Chromosome(new_order)
                calculate_fitness(new_chromosome)
                if new_chromosome.fitness > chromosome.fitness:
                    chromosome.order = new_order
                    chromosome.fitness = new_chromosome.fitness
                    improved = True

# Generate the initial population of the genetic algorithm (random permutations of indices)
def generate_population(population_size):
    population = []
    for _ in range(population_size):
        order = random.sample(range(1, len(coords) + 1), len(coords))
        chr = Chromosome(order)
        calculate_fitness(chr)
        population.append(chr)
    return population

# Select 2 parents using roulette wheel selection
def selection(population):
    return random.choices(population, weights=[chromosome.fitness for chromosome in population], k=2)

# Crossover operator: Order 1 Crossover (OX1)
def crossover(parent1, parent2):
    perm1 = parent1.order
    perm2 = parent2.order
    size = len(perm1)
    start = random.randint(0, size - 1)
    end = random.randint(start + 1, size)
    child = perm1[start:end]

    # Fill the remaining slots
    insert = end
    p2_index = end

    while p2_index < size:
        gene = perm2[p2_index]
        p2_index += 1
        if gene not in child:
            child.insert(insert, gene)
            insert += 1
            if insert == size:
                insert = 0

    p2_index = 0
    while len(child) < size:
        gene = perm2[p2_index]
        p2_index += 1
        if gene not in child:
            child.insert(insert, gene)
            insert += 1
            if insert == size:
                insert = 0

    return Chromosome(child)

# Mutation operator: Swap mutation
def mutate(chromosome, mutation_rate):
    if random.random() < mutation_rate:
        index1, index2 = random.sample(range(len(chromosome.order)), 2)
        chromosome.order[index1], chromosome.order[index2] = chromosome.order[index2], chromosome.order[index1]

def genetic_algorithm(population_size, mutation_rate, crossover_rate, local_search, max_iter):
    population = generate_population(population_size)
    best_individual = None
    best_routes = []  # Store best routes for visualization
    best_fitnesses = []  # Store best fitness values for visualization

    for gen in range(1, max_iter):
        nex_gen = []

        while len(nex_gen) < population_size:
            parents = selection(population)

            # Crossover with a certain probability, otherwise copy the parents
            if random.random() < crossover_rate:
                child1 = crossover(parents[0], parents[1])
                child2 = crossover(parents[1], parents[0])
            else:
                child1 = parents[0]
                child2 = parents[1]

            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)

            # Apply 2-opt local search to improve the solution
            if local_search:
                two_opt(child1)
                two_opt(child2)

            calculate_fitness(child1)
            calculate_fitness(child2)
            nex_gen.append(child1)
            nex_gen.append(child2)

        # survivors selection: select top population_size individuals from the combined population
        population += nex_gen
        population = sorted(population, key=lambda individual: individual.fitness, reverse=True)[:population_size]
        best_individual = population[0]

        # Store the best route and its fitness for visualization
        best_routes.append(best_individual.order)
        best_fitnesses.append(best_individual.fitness)

        # print best individual in each generation
        print(f"Generation {gen}: Best Individual: {best_individual} | Total Distance: {1 / best_individual.fitness:.4f}")

    return best_individual, best_routes, best_fitnesses

# Plotting and animation functions
def plot_points_and_lines(order=None, ax=None):
    if order is None or ax is None:
        return

    ordered_points = [coords[label - 1] for label in order]

    # Plot the points
    x_coords = [point.x for point in ordered_points]
    y_coords = [point.y for point in ordered_points]
    point_labels = [point.label for point in ordered_points]
    ax.scatter(x_coords, y_coords)

    # Add labels to the points
    for i, label in enumerate(point_labels):
        if label is not None:
            ax.text(x_coords[i], y_coords[i], label)

    # Plot the lines
    start = order[0]
    for label in order[1:] + [start]:  # Close the loop
        end = label
        start_coords = coords[start - 1]
        end_coords = coords[end - 1]
        ax.plot([start_coords.x, end_coords.x], [start_coords.y, end_coords.y], color='blue')
        start = label

def animate_routes(best_routes, best_fitnesses):
    fig, ax = plt.subplots(figsize=(12, 8))

    # Set axis limits based on Berlin52 dataset range
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 1300)

    def update(frame):
        ax.clear()
        plot_points_and_lines(best_routes[frame], ax)
        fitness = best_fitnesses[frame]
        total_distance = 1 / fitness if fitness != 0 else float('inf')
        ax.set_title(f'Best Route at Generation {frame + 1} | Fitness: {fitness:.4f} | Total Distance: {total_distance:.4f}')
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.grid()

    ani = FuncAnimation(fig, update, frames=len(best_routes), interval=1, repeat=False)
    plt.show()

# Coordinates from the Berlin52 TSP problem, BKS: 7542
berlin52_coords = [
    (565.0, 575.0), (25.0, 185.0), (345.0, 750.0), (945.0, 685.0), (845.0, 655.0),
    (880.0, 660.0), (25.0, 230.0), (525.0, 1000.0), (580.0, 1175.0), (650.0, 1130.0),
    (1605.0, 620.0), (1220.0, 580.0), (1465.0, 200.0), (1530.0, 5.0), (845.0, 680.0),
    (725.0, 370.0), (145.0, 665.0), (415.0, 635.0), (510.0, 875.0), (560.0, 365.0),
    (300.0, 465.0), (520.0, 585.0), (480.0, 415.0), (835.0, 625.0), (975.0, 580.0),
    (1215.0, 245.0), (1320.0, 315.0), (1250.0, 400.0), (660.0, 180.0), (410.0, 250.0),
    (420.0, 555.0), (575.0, 665.0), (1150.0, 1160.0), (700.0, 580.0), (685.0, 595.0),
    (685.0, 610.0), (770.0, 610.0), (795.0, 645.0), (720.0, 635.0), (760.0, 650.0),
    (475.0, 960.0), (95.0, 260.0), (875.0, 920.0), (700.0, 500.0), (555.0, 815.0),
    (830.0, 485.0), (1170.0, 65.0), (830.0, 610.0), (605.0, 625.0), (595.0, 360.0),
    (1340.0, 725.0), (1740.0, 245.0)
]

# Coordinates for the Att48 TSP problem, BKS: 33522
att48_coords = [
    (6734, 1453), (2233, 10), (5530, 1424), (401, 841), (3082, 1644),
    (7608, 4458), (7573, 3716), (7265, 1268), (6898, 1885), (1112, 2049),
    (5468, 2606), (5989, 2873), (4706, 2674), (4612, 2035), (6347, 2683),
    (6107, 669), (7611, 5184), (7462, 3590), (7732, 4723), (5900, 3561),
    (4483, 3369), (6101, 1110), (5199, 2182), (1633, 2809), (4307, 2322),
    (675, 1006), (7555, 4819), (7541, 3981), (3177, 756), (7352, 4506),
    (7545, 2801), (3245, 3305), (6426, 3173), (4608, 1198), (23, 2216),
    (7248, 3779), (7762, 4595), (7392, 2244), (3484, 2829), (6271, 2135),
    (4985, 140), (1916, 1569), (7280, 4899), (7509, 3239), (10, 2676),
    (6807, 2993), (5185, 3258), (3023, 1942)
]

random.seed(42)  # Set seed for reproducibility

# Create a list of Point objects
coords = [Point(x, y, i + 1) for i, (x, y) in enumerate(att48_coords)]

# Run the genetic algorithm and animate
best_individual, best_routes, best_fitnesses = genetic_algorithm(population_size=n_pop, mutation_rate=p_m, crossover_rate=p_x, local_search=ls, max_iter=max_iter)
print("Best individual:", best_individual)
animate_routes(best_routes, best_fitnesses)
