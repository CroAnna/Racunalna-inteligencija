import numpy as np

# Aktivacijske funkcije
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def linear(x):
    return x

# Težine
W1 = np.array([[0.2, 0.4, -0.5], [-0.3, 0.1, 0.2], [0.7, -0.1, -0.4]])
W2 = np.array([[0.1, -0.2, 0.3], [0.4, 0.6, -0.1]])
W3 = np.array([0.3, -0.7])

# Funkcija za izračun izlaznih vrijednosti mreže
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
    
    return output

# Funkcija za izračun pogreške
def calculate_error(expected_output, actual_output):
    return expected_output - actual_output

# Unos ulaznih ulaza
x = np.array([0.5, -0.3, 0.8])

# Unos očekivanih izlaza
expected_output = -0.21556451

# Izračun izlazne vrijednosti za dani ulaz
output = forward(x)

# Izračun pogreške
error = calculate_error(expected_output, output)

# Ispis rezultata
print("Stvarni izlaz neuronske mreže:", output)
print("Očekivani izlaz:", expected_output)
print("Pogreška:", error)
