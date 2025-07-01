import random
import time
import matplotlib.pyplot as plt

# Karatsuba Multiplication Algorithm
def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2

    high_x, low_x = divmod(x, 10 ** m)
    high_y, low_y = divmod(y, 10 ** m)

    z0 = karatsuba(low_x, low_y)
    z1 = karatsuba(low_x + high_x, low_y + high_y)
    z2 = karatsuba(high_x, high_y)

    return z2 * 10 ** (2 * m) + (z1 - z2 - z0) * 10 ** m + z0

# Closest Pair of Points Algorithm
def closest_pair(points):
    def distance(p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    points = sorted(points, key=lambda p: p[0])
    return points[0], points[1], distance(points[0], points[1])

# Function to perform the empirical analysis
def plot_analysis():
    print("Starting the empirical analysis...")

    input_sizes = [100, 200, 400, 800, 1600]
    closest_times = []
    karatsuba_times = []

    for size in input_sizes:
        print(f"Processing input size {size}...")
        points = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(size)]
        
        start_time = time.time()
        closest_pair(points)  # Measuring closest pair execution time
        closest_times.append(time.time() - start_time)

        a = random.randint(10 * size, 10 * (size + 1))
        b = random.randint(10 * size, 10 * (size + 1))
        start_time = time.time()
        karatsuba(a, b)  # Measuring Karatsuba multiplication execution time
        karatsuba_times.append(time.time() - start_time)

    print("Generating the plot...")
    plt.figure(figsize=(10, 6))
    plt.plot(input_sizes, closest_times, label="Closest Pair of Points", marker='o')
    plt.plot(input_sizes, karatsuba_times, label="Karatsuba Multiplication", marker='s')
    plt.xlabel("Input Size")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Empirical Analysis of Divide and Conquer Algorithms")
    plt.legend()
    plt.grid(True)

    # Save the plot as an image
    plt.savefig('empirical_analysis_output.png')
    plt.show()
    print("Plot saved as 'empirical_analysis_output.png'")

# Run the analysis
plot_analysis()
