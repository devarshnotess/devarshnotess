#quantum particle in infinite potential well
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
hbar = 1.0545718e-34
m = 9.10938356e-31
L = 1e-9

# Energy levels
def energy(n):
    return (n**2 * np.pi**2 * hbar**2) / (2 * m * L**2)

# Wavefunction
def wavefunction(n, x, t):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L) * np.exp(-1j * energy(n) * t / hbar)

# Streamlit interface
st.title('Quantum Mechanics - Particle in a Potential Well')

n_max = st.slider('Maximum energy level (n)', 1, 5, 3)
L_slider = st.slider('Length of the potential well (L) in nm', 0.5, 10.0, 1.0) * 1e-9
t_max_ns = st.slider('Maximum time (t) in ns', 0, 1000, 500)
L = L_slider

x = np.linspace(0, L, 1000)

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, L)
ax.set_ylim(0, 2)
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,

def update(frame):
    t = frame * (t_max_ns * 1e-9 / 100)  # Time in seconds
    psi_sum = np.zeros_like(x, dtype=complex)
    for n in range(1, n_max + 1):
        psi_sum += wavefunction(n, x, t)

    prob_density = np.abs(psi_sum)**2
    line.set_data(x, prob_density)
    return line,

frames = 100  # Fixed number of frames for smoother animation
ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True)

st.pyplot(fig)
