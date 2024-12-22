import numpy as np

# Evolution Strategy Algorithm (mu + lam) for continuous optimization
def evolution_strategy(mu, lam, tau, dim, generations, fitness_function, bounds):

    # Population initialization
    population = np.random.uniform(bounds[0], bounds[1], (mu, dim))
    sigma = np.random.uniform(0.1, 1.0, mu)  # Initial mutation strengths for each individual
    
    # Evaluate fitness for initial population
    fitness_values = np.array([fitness_function(ind) for ind in population])

    for gen in range(generations):
        # Offspring generation
        offspring_population = []
        offspring_sigma = []
        
        for i in range(lam):
            # Select a parent at random from the population
            parent_idx = np.random.randint(0, mu)
            parent = population[parent_idx]
            parent_sigma = sigma[parent_idx]
            
            # Self-adaptation of mutation strength
            new_sigma = parent_sigma * np.exp(tau * np.random.randn())
            
            # Mutation
            offspring = parent + new_sigma * np.random.randn(dim)
            
            # Boundary constraint handling
            offspring = np.clip(offspring, bounds[0], bounds[1])
            
            offspring_population.append(offspring)
            offspring_sigma.append(new_sigma)
        
        # Evaluate fitness of the offspring
        offspring_fitness = np.array([fitness_function(ind) for ind in offspring_population])
        
        # Combine parent and offspring (mu + lam) for selection
        combined_population = np.vstack((population, offspring_population))
        combined_sigma = np.concatenate((sigma, offspring_sigma))
        combined_fitness = np.concatenate((fitness_values, offspring_fitness))
        
        # Select the top mu individuals for the next generation
        selected_indices = np.argsort(combined_fitness)[:mu]
        population = combined_population[selected_indices]
        sigma = combined_sigma[selected_indices]
        fitness_values = combined_fitness[selected_indices]
        
        # Logging progress
        best_fitness = fitness_values[0]
        print(f"Generation {gen+1}, Best Fitness: {best_fitness}")

    return population[0], fitness_values[0]  # Return the best individual and its fitness

# Example fitness function (Sphere function) for testing the ES algorithm 
def sphere_function(x):
    return np.sum(x**2)

# Ackley fitness function for testing multimodal optimization capabilities of ES algorithm 
def ackley_function(x):
    d = len(x)
    first_sum = -0.2 * np.sqrt(np.sum(x**2) / d)
    second_sum = np.sum(np.cos(2 * np.pi * x)) / d
    return -20 * np.exp(first_sum) - np.exp(second_sum) + 20 + np.e

# Hyperparameters
dim = 10 # Problem dimension
mu = 20  # Parent population size
lam = 100  # Offspring population size
tau = 0.5 / np.sqrt(dim) # Learning rate for self-adaptation of mutation strength
generations = 200 # Number of generations
bounds = (-10, 10) # Search space bounds

# Run the evolution strategy algorithm
best_solution, best_fitness = evolution_strategy(mu, lam, tau, dim, generations,ackley_function , bounds)
print(f"Best Solution: {best_solution}, Fitness: {best_fitness}")
