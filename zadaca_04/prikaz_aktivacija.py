import numpy as np
import matplotlib.pyplot as plt

# Aktivacijske funkcije
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def linear(x):
    return x

# Težine
W1 = np.array([[0.2, 0.4, -0.5], [-0.3, 0.1, 0.2], [0.7, -0.1, -0.4]])
W2 = np.array([[0.1, -0.2, 0.3], [0.4, 0.6, -0.1]])  # Adjusted dimensions
W3 = np.array([0.3, -0.7])

# Ulazni podaci (primjer)
x = np.array([0.5, -0.3, 0.8])

# Izračun izlaznih vrijednosti
def forward(x):
    # Ulazni sloj do skrivenog sloja 1
    z1 = np.dot(W1, x)
    a1 = sigmoid(z1)
    
    # Skriveni sloj 1 do skrivenog sloja 2
    z2 = np.dot(W2, a1)
    a2 = sigmoid(z2)
    
    # Skriveni sloj 2 do izlaznog sloja
    z3 = np.dot(W3, a2)
    output = linear(z3)
    
    return z1, a1, z2, a2, z3, output

# Izračun izlazne vrijednosti za dani ulaz
z1, a1, z2, a2, z3, output = forward(x)

# Plotting the activations and outputs
layers = ['Input', 'Hidden Layer 1', 'Hidden Layer 2', 'Output']
values = [x, a1, a2, output]

# Flatten the values list for plotting
flat_values = [val if isinstance(val, np.ndarray) else np.array([val]) for val in values]

fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(15, 4))
fig.suptitle('Neural Network Forward Pass Activations and Output')

for ax, layer, val in zip(axes, layers, flat_values):
    ax.bar(range(len(val)), val)
    ax.set_title(layer)
    ax.set_xticks(range(len(val)))
    ax.set_xticklabels([f'Node {i+1}' for i in range(len(val))])
    ax.set_ylim(-1, 1)
    ax.grid(True)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
