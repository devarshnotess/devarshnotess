import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
hbar = 1.0545718e-34  # Reduced Planck's constant (J.s)
m = 9.10938356e-31    # Mass of the electron (kg)
L = 1e-9              # Length of the infinite potential well (m)

# Energy levels (n)
def energy(n):
    return (n**2 * np.pi**2 * hbar**2) / (2 * m * L**2)

# Wavefunction
def wavefunction(n, x, t):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L) * np.exp(-1j * energy(n) * t / hbar)

# Probability density (|psi(x,t)|^2)
def probability_density(n, x, t):
    return np.abs(wavefunction(n, x, t))**2

# Interactive streamlit interface
st.title('Quantum Mechanics - Particle in a Potential Well')

# Parameters from the user
n_max = st.slider('Number of energy levels (n)', 1, 5, 3)
L_slider = st.slider('Length of the potential well (L) in nm', 0.5, 10.0, 1.0) * 1e-9
t_slider = st.slider('Time (t) in ns', 0, 1000, 500) * 1e-9

# Update constants based on user input
L = L_slider

# Spatial grid (x positions in the well)
x = np.linspace(0, L, 1000)

# Creating the figure
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, L)
ax.set_ylim(0, 2)

# Line for probability density
line, = ax.plot([], [], lw=2)

# Initialization function for the animation
def init():
    line.set_data([], [])
    return line,

# Update function for the animation
def update(frame):
    t = frame * 1e-9  # Convert frame to time in seconds
    prob_density = np.zeros_like(x)
    
    # Add contributions from each energy level (n)
    for n in range(1, n_max + 1):
        prob_density += probability_density(n, x, t)

    # Update the plot with new data
    line.set_data(x, prob_density)
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 1000, 10), init_func=init, blit=True)

# Display the animation in Streamlit
st.pyplot(fig)