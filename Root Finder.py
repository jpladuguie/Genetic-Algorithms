import numpy as np
import random, time
from random import randint
import matplotlib.pyplot as plt

# Function to evaluate
# Current function f(x) = x^3 - 101x^2 + 3031x - 24531
# f(x) has roots at 13, 37 and 51
def f(x):
    return (x ** 3 - 101 * x ** 2 + 3031 * x - 24531)

# Breed two integers
def breed(a, b):
    # Get binary string form of integers
    a = str(bin(int(a)))[2:]
    b = str(bin(int(b)))[2:]

    # Add zeros to beginning of number to make them both length 6
    for x in range(6 - len(a)):
        a = '0' + a
    for x in range(6 - len(b)):
        b = '0' + b

    # Return the first half of a with the second half of b
    return int(str(a[:3] + b[-3:]), 2)

# Mutates integer
def mutate(x):
    # Get binary string form of integer
    x = str(bin(int(x)))[2:]

    # Add zeros to beginning of x to make it length 6
    for i in range(6 - len(x)):
        x = '0' + x

    # Turn x into a list
    x = list(x)

    # Choose a random position to mutate
    pos = randint(0, 5)

    # Mutate and return x
    if x[pos] == '0':
        x[pos] = '1'
    else:
        x[pos] = '0'
    x = ''.join(x)

    return int(x, 2)

# Evolve 10 initial chromosomes to find the root of f(x) in the range [0, 63]
def evolve(chromosomes):

    # Loop through 64 generations of 10 chromosomes
    # Starts off with 10 random chromosomes, but they will evolve over time, becoming closer to the root of the function
    # The more iterations the more accurate the result, but the longer it will take
    for i in range(64):

        # Get f(x) for first 10 chromosomes.
        # First part of each element in chromosomes is chromosome value, i.e. x, and second part is f(x)
        for i in range(10):
            x = chromosomes[i][0]
            chromosomes[i][1] = f(x)

        # Sort by distance of f(x) from zero - equivalent to absolute value
        chromosomes = np.absolute(chromosomes)
        chromosomes = chromosomes[chromosomes[:, 1].argsort()]
        chromosomes = chromosomes.astype(int)

        # Set up temp array of 15 empty chromosomes
        # Original 10 will be added later to this array, as well as 3 offspring from the most advantageous chromosomes and 2 mutated ones, hence 15 in total
        tempArray = np.zeros([15, 2])

        # Get top 6 chromosomes, i.e. closest to zero
        for i in range(0, 6):
            # Sort them into 3 pairs
            if i % 2 != 0:
                a = chromosomes[i][0]
                b = chromosomes[i+1][0]

                # Add the 3 offspring to first 3 items of temp array
                tempArray[int(i/2)] = [breed(a, b), 0]


        # Randomly mutate a chromosome, one from the bottom 4 and one from the top 6
        bottomChromosome = chromosomes[randint(0, 5)][0]
        topChromosome = chromosomes[randint(0, 5)][0]

        # Add the two mutated cells to the temp array
        tempArray[3] = [mutate(bottomChromosome), 0]
        tempArray[4] = [mutate(topChromosome), 0]

        # Add rest of chromosomes to temp array
        for i in range(5, 15):
            tempArray[i] = chromosomes[i-5]

        # Get f(x) for the first 5 chromosomes, as the last 10 have just been added and were evaluated earlier
        for i in range(5):
            x = tempArray[i][0]
            tempArray[i][1] = f(x)

        # Sort temp array by absolute value/distance from zero
        tempArray = np.absolute(tempArray)
        tempArray = tempArray[tempArray[:, 1].argsort()]

        # Take the top 10 most advantageous chromosomes from the 15 in temp array, i.e. closest to zero, and add them to the original chromosome array
        # Loop is then repeated with new generation, which should evolve over time
        for i in range(0, 9):
            chromosomes[i] = tempArray[i]

    # Return the first element of the chromosome array once it has finished iterating through the generations
    # This value will be the most advantageous/closest to zero, so will be the most accurate root
    # First part is the root, second part is absolute value of f(x), so distance from zero/error margin
    return chromosomes[0]


# Start timer
start = time.time()

# Initialise empty array for results
results = []

# Calculate root 1000 times and store in results array
for i in range(1000):
    # Set up 10 initial chromosomes to random 6 bit numbers
    chromosomes = np.zeros([10, 2])
    for i in range(10):
        chromosomes[i] = [random.getrandbits(6), 0]

    # Evolve chromosomes to find root of f(x)
    root = evolve(chromosomes)
    results.append(root[0])

# Get time taken
end = time.time()
print('Time Taken: ' + str(end - start))

# Plot histogram of results
plt.hist(results, bins=64)
plt.title("Roots of f(x)")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()