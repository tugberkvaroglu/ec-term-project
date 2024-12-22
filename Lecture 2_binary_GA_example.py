import numpy as np

# PARAMETERS
n_bits = 16 # chromosome length (problem size)
n_pop = 40 # population size
p_x = 0.9 # crossover probability
p_m = (1/n_bits) # mutation probability
max_iter = 500 # maximum number of iterations

# random initial population (n_pop x n_bits)
pop = np.random.randint(0, 2, size=(n_pop, n_bits))

# fitness function
def fitness(chromosome):
    return one_max(chromosome)

"""# fitness function
def fitness(chromosome):
    return mystery(chromosome)"""

# one-max problem (maximize the number of ones)
def one_max(chromosome):
    return np.sum(chromosome)

# mystery function to be maximized
def mystery(chromosome):
    return np.sum(chromosome[0::2]) + np.sum(1-chromosome[1::2])

# evaluate fitness of each individual in the population
f_values = [fitness(ind) for ind in pop]

# print initial population
print('\INITIAL POPULATION:')
for i in range(n_pop):
    print('ind_{0:2d}: {1}, fitness: {2}'.format(i, pop[i], f_values[i]))

# fitness proportionate selection (roulette wheel). Returns the indices of two selected parents
def parent_selection(f_values):
    f_sum = np.sum(f_values)
    p = f_values/f_sum
    return np.random.choice(np.arange(n_pop), size=2, p=p)

# parent selection test, select 10 parents and list them with their fitness
print('\nSELECTED PARENTS TEST:')
for i in range(10):
    parents = parent_selection(f_values)
    fitnesses = [f_values[parents[0]], f_values[parents[1]]]
    print('parents_select_{0:2d}: {1}, fitness: {2}'.format(i, parents, fitnesses))

# single-point crossover (creates two new children and returns them). Takes the indices of two parents.
def crossover(parents):
    if np.random.rand() < p_x:
        point = np.random.randint(1, n_bits)
        child1 = np.concatenate((pop[parents[0], :point], pop[parents[1], point:]))
        child2 = np.concatenate((pop[parents[1], :point], pop[parents[0], point:]))
        return child1, child2
    else:
        return pop[parents[0]], pop[parents[1]]

# crossover test with a pair of parents
print('\nCROSSOVER TEST:')
parents = parent_selection(f_values)
children = crossover(parents)
print('parents: {0}'.format(parents))
print('children: {0}'.format(children))

# bit-flip mutation (mutates the chromosome and returns it)
def bitFlipMutation(chromosome):
    for i in range(n_bits):
        if np.random.rand() < p_m:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

# mutation test with a single chromosome
print('\nMUTATION TEST:')
ind = np.random.randint(0, n_pop)
print('original: {0}'.format(pop[ind]))
pop[ind] = bitFlipMutation(pop[ind])
print('mutated:  {0}'.format(pop[ind]))

def BasicGeneticAlgorithm():
    pop = np.random.randint(0, 2, size=(n_pop, n_bits)) # random initial population
    f_values = [fitness(ind) for ind in pop] # evaluate fitness of each individual in the population

    # find maximum fitness value in the initial population
    max = np.argmax(f_values)
    best_sol = pop[max]
    best_f = f_values[max]
    print('GEN: {0}, best_f: {1}, best_sol:{2}'.format(0, best_f, best_sol))

    # main loop: repeat until max_iter is reached. New population is stored in pop_new.
    for gen in range(1, max_iter):
        pop_new = np.zeros((n_pop, n_bits), dtype=int)
        for i in range(n_pop//2):
            parents = parent_selection(f_values) # select parents
            children = crossover(parents)
            pop_new[2*i] = bitFlipMutation(children[0])
            pop_new[2*i+1] = bitFlipMutation(children[1])

        pop = pop_new # replace the old population with the new one
        f_values = [fitness(ind) for ind in pop] # evaluate fitness of each individual in the new population
        
        # find maximum fitness value in the current population
        max = np.argmax(f_values)
        if f_values[max] > best_f:
            best_sol = pop[max]
            best_f = f_values[max]
        print('GEN: {0}, best_f: {1}, best_sol:{2}'.format(gen, best_f, best_sol))

BasicGeneticAlgorithm()
