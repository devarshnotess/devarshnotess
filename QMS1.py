# This code simulates and visualizes the evolution of wave packet in one dimension using the Cranck-Nicolson method

import numpy as np
import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

# Constants
hbar = 1.0
m = 1.0
dx = 0.1
dt = 0.01
x_min, x_max = -10, 10
t_max = 2.0

# Space Grid
x = np.arange(x_min, x_max, dx)
N = len(x)
t_steps = int(t_max / dt)

# Initial Wave Packet Function
def initialize_wave_packet(x0, k0):
    sigma = 1.0
    psi = np.exp(-(x - x0)**2 / (2 * sigma**2)) * np.exp(1j * k0 * x)
    return psi / np.sqrt(np.sum(np.abs(psi)**2))  # Normalize

# Create Hamiltonian Matrix
diagonal = np.full(N, -2)
off_diagonal = np.full(N - 1, 1)
H = (-hbar**2 / (2 * m * dx**2)) * diags([diagonal, off_diagonal, off_diagonal], [0, -1, 1])

# Time Evolution Operators (Crank-Nicolson)
I = np.eye(N)
A = (I - 1j * dt / (2 * hbar) * H).tocsc()
B = (I + 1j * dt / (2 * hbar) * H).tocsc()

# UI Elements
x0_slider = widgets.FloatSlider(min=-8, max=8, step=0.1, value=-5, description="x0")
k0_slider = widgets.FloatSlider(min=-5, max=5, step=0.1, value=2, description="k0")
time_slider = widgets.IntSlider(min=0, max=t_steps, step=10, value=0, description="Time Step")
reset_button = widgets.Button(description="Reset")

# Function to Update the Plot
def update_plot(change):
    x0, k0 = x0_slider.value, k0_slider.value
    psi = initialize_wave_packet(x0, k0)

    # Time Evolution
    for _ in range(time_slider.value):
        psi = spsolve(A, B @ psi)
    
    # Update Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=np.abs(psi)**2, mode='lines', name="|ψ(x,t)|²"))
    fig.update_layout(title="Wavefunction Evolution", xaxis_title="Position x", yaxis_title="Probability Density")
    display(fig)

# Event Listeners
x0_slider.observe(update_plot, names='value')
k0_slider.observe(update_plot, names='value')
time_slider.observe(update_plot, names='value')
reset_button.on_click(lambda _: update_plot(None))

# Display UI
display(x0_slider, k0_slider, time_slider, reset_button)
update_plot(None)  # Initial plot
