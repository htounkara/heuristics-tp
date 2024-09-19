import numpy as np
import matplotlib.pyplot as plt
import random
import math
import time

def get_points(filepath):
    with open(filepath, 'r') as f:
        data = f.readlines()
        points = []
        for line in data[1:]:
            x, y = map(int, line.strip().split(sep=' '))
            points.append((x, y))
    return points

points = get_points('data/Pb5.txt')

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def distance_matrix(points):
    n = len(points)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j] = distance(points[i], points[j])
            matrix[j][i] = matrix[i][j]
    return matrix

matrix = distance_matrix(points)

def circuit_distance(circuit, matrix):
    return np.sum(matrix[circuit[:-1], circuit[1:]]) + matrix[circuit[-1], circuit[0]]

def greedy_hamiltonian_circuit(points):
    n = len(points)
    circuit = [random.randint(0, n - 1)]
    visited = set(circuit)
    while len(circuit) < n:
        current_point = circuit[-1]
        next_point = min([i for i in range(n) if i not in visited], key=lambda x: matrix[current_point][x])
        circuit.append(next_point)
        visited.add(next_point)
    return circuit

def best_greedy_circuit(points, iterations):
    n = len(points)
    best_circuit = greedy_hamiltonian_circuit(points)
    best_distance = circuit_distance(best_circuit, matrix)
    start = time.time()
    
    for i in range(iterations):
        circuit = greedy_hamiltonian_circuit(points)
        distance = circuit_distance(circuit, matrix)
        if distance < best_distance:
            best_circuit = circuit
            best_distance = distance
        print(f'Iteration {i+1}/{iterations} - Best distance: {best_distance}')
    end = time.time()
    return best_circuit, best_distance, end - start

def plot_circuit(points, circuit):
    plt.figure(figsize=(10, 10))
    x = [points[i][0] for i in circuit]
    y = [points[i][1] for i in circuit]
    plt.plot(x, y, 'o-')
    plt.plot(x[0], y[0], 'ro')
    plt.show()

circuit, distance, time = best_greedy_circuit(points, 400)
print(f'Best distance: {distance}')
print(f'Time: {time}')
plot_circuit(points, circuit)
