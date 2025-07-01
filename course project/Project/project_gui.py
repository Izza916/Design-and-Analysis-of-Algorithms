import tkinter as tk
from tkinter import filedialog, messagebox
import random
import math
import os
import time
import matplotlib.pyplot as plt


# Function to generate input for the Closest Pair of Points Algorithm
def generate_closest_pair_input(file_name="points_input.txt", num_points=100):
    with open(file_name, 'w') as f:
        for _ in range(num_points):
            x = random.randint(0, 1000)
            y = random.randint(0, 1000)
            f.write(f"{x} {y}\n")
    print(f"Input file for closest pair generated: {file_name}")

# Function to generate input for Karatsuba Multiplication Algorithm
def generate_karatsuba_input(file_name="integers_input.txt"):
    a = random.randint(1000, 10000)
    b = random.randint(1000, 10000)
    with open(file_name, 'w') as f:
        f.write(f"{a}\n{b}\n")
    print(f"Input file for Karatsuba multiplication generated: {file_name}")

# Closest Pair of Points Algorithm
def closest_pair(points):
    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def closest_pair_recursive(px, py):
        if len(px) <= 3:
            min_dist = float('inf')
            pair = None
            for i in range(len(px)):
                for j in range(i + 1, len(px)):
                    d = distance(px[i], px[j])
                    if d < min_dist:
                        min_dist = d
                        pair = (px[i], px[j])
            return pair, min_dist

        mid = len(px) // 2
        mid_point = px[mid]

        left_px = px[:mid]
        right_px = px[mid:]
        left_py = list(filter(lambda x: x[0] <= mid_point[0], py))
        right_py = list(filter(lambda x: x[0] > mid_point[0], py))

        (p1, q1), d1 = closest_pair_recursive(left_px, left_py)
        (p2, q2), d2 = closest_pair_recursive(right_px, right_py)

        min_pair = (p1, q1) if d1 < d2 else (p2, q2)
        min_dist = min(d1, d2)

        strip = [p for p in py if abs(p[0] - mid_point[0]) < min_dist]
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 7, len(strip))):
                d = distance(strip[i], strip[j])
                if d < min_dist:
                    min_dist = d
                    min_pair = (strip[i], strip[j])

        return min_pair, min_dist

    px = sorted(points, key=lambda x: x[0])
    py = sorted(points, key=lambda x: x[1])
    return closest_pair_recursive(px, py)

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

# Plotting for Closest Pair of Points
def plot_closest_pair(points, closest_pair):
    x_points, y_points = zip(*points)
    plt.scatter(x_points, y_points, label="Points", color="blue")

    (x1, y1), (x2, y2) = closest_pair
    plt.plot([x1, x2], [y1, y2], color="red", linestyle="--", label="Closest Pair")
    plt.scatter([x1, x2], [y1, y2], color="red", zorder=5)  # Highlight closest pair

    plt.xlabel("X Coordinates")
    plt.ylabel("Y Coordinates")
    plt.title("Closest Pair of Points")
    plt.legend()

    # Save plot as image
    plt.savefig('closest_pair_output.png')
    plt.show()

# Plotting for Karatsuba Multiplication
def plot_karatsuba(a, b, result):
    labels = ['a', 'b', 'Product']
    values = [a, b, result]
    
    plt.bar(labels, values, color=['blue', 'green', 'orange'])
    plt.ylabel('Value')
    plt.title(f'Karatsuba Multiplication: {a} * {b} = {result}')
    
    # Save plot as image
    plt.savefig('karatsuba_output.png')
    plt.show()

# Function to process input file and show results
def process_file(filepath):
    if "points" in filepath:
        with open(filepath, "r") as f:
            points = [tuple(map(int, line.strip().split())) for line in f]
        pair, dist = closest_pair(points)
        messagebox.showinfo("Closest Pair of Points", f"Closest Pair: {pair}\nDistance: {dist:.2f}")
        plot_closest_pair(points, pair)  # Generate plot for closest pair

    elif "integers" in filepath:
        with open(filepath, "r") as f:
            a = int(f.readline().strip())
            b = int(f.readline().strip())
        result = karatsuba(a, b)
        messagebox.showinfo("Integer Multiplication", f"Product: {result}")
        plot_karatsuba(a, b, result)  # Generate plot for Karatsuba multiplication

# GUI to select file and show output
def select_file():
    filepath = filedialog.askopenfilename(initialdir="input_files", title="Select a File")
    if filepath:
        process_file(filepath)

# Main function to set up the GUI
def main():
    # Generate the input files when the GUI starts
    generate_closest_pair_input()  # This creates the points_input.txt file
    generate_karatsuba_input()  # This creates the integers_input.txt file

    root = tk.Tk()
    root.title("DAA Project")

    tk.Label(root, text="Select an input file:").pack(pady=10)
    tk.Button(root, text="Choose File", command=select_file).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
