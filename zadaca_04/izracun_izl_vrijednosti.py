import numpy as np

# Aktivacijske funkcije
def sigmoid(x): # koristi se za skrivene neurone
    return 1 / (1 + np.exp(-x))

def linear(x): # koristi se za izlazni neuron
    return x

# Težine (prema skici)
W1 = np.array([[0.2, 0.4, -0.5], [-0.3, 0.1, 0.2], [0.7, -0.1, -0.4]])
W2 = np.array([[0.1, -0.2, 0.3], [0.4, 0.6, -0.1]])
W3 = np.array([0.3, -0.7])

# Ulazni podaci (primjer)
x = np.array([0.5, -0.3, 0.8])

# Izračun izlaznih vrijednosti
def forward(x): # 
    # Ulazni sloj do skrivenog sloja 1
    z1 = np.dot(W1, x)  # Ovdje se vrši matrično množenje ulaza x s matricom težina W1
    a1 = sigmoid(z1)    # Primjena sigmoidne aktivacijske funkcije na rezultirajućem vektoru
    print("Aktivacije u skrivenom sloju 1:", a1)
    
    # Skriveni sloj 1 do skrivenog sloja 2
    z2 = np.dot(W2, a1)
    a2 = sigmoid(z2)
    print("Aktivacije u skrivenom sloju 2:", a2)
    
    # Skriveni sloj 2 do izlaznog sloja
    z3 = np.dot(W3, a2)
    output = linear(z3)
    
    return output

# Izračun izlazne vrijednosti za dani ulaz
output = forward(x)
print("Izlazna vrijednost mreže:", output)
